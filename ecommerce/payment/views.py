import stripe
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.reverse import reverse
from payment import serializers
from payment.models import Payment
from order.models import Order
from payment.models import Payment
from cart.models import Cart, CartItem
from payment import utils


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.PaymentReadSerializer
    queryset = Payment.objects.all()
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]


class PaymentStatusViewSet(viewsets.ViewSet):
    """
    Viewset for payment success and cancel
    """

    @action(methods=["GET"], detail=False, url_path="success", url_name="success")
    def success(self, request, *args, **kwargs):
        return Response({"message": "success"}, status=status.HTTP_200_OK)

    @action(methods=["GET"], detail=False, url_path="cancel", url_name="cancel")
    def cancel(self, request, *args, **kwargs):
        return Response({"message": "failed"}, status=status.HTTP_200_OK)


class StripeViewSet(viewsets.ViewSet):
    """
    Payment Handler For Stripe
    """

    permission_classes = [IsAuthenticated]

    @action(
        methods=["POST"],
        detail=False,
        url_path="create-session",
        url_name="create-session",
    )
    def create_session(self, request, *args, **kwargs):
        try:
            order = Order.objects.prefetch_related("payment").get(
                id=request.data["order_id"]
            )
        except Order.DoesNotExist:
            raise NotFound("Order Not Found")

        if Payment.objects.filter(order=order, status="COMPLETED").exists():
            raise PermissionDenied("Payment completed for given order id")

        payment, created = Payment.objects.get_or_create(
            order=order,
            provider="STRIPE",
            status="REQUESTED",
            amount_requested=order.total_price,
        )

        try:
            stripe.api_key = settings.STRIPE_SECRET_KEY
            checkout_session = stripe.checkout.Session.create(
                line_items=[
                    {
                        "price_data": {
                            "currency": item.currency,
                            "unit_amount": int(item.final_price * 100),
                            "product_data": {
                                "name": item.variant.product.name,
                            },
                        },
                        "quantity": item.quantity,
                    }
                    for item in order.order_item.all()
                ],
                mode="payment",
                success_url=reverse("payment:status-success", request=request),
                cancel_url=reverse("payment:status-cancel", request=request),
                metadata={
                    "user_id": request.user.id,
                    "order_id": order.id,
                    "payment_id": payment.id,
                },
                payment_intent_data={
                    "metadata": {
                        "user_id": request.user.id,
                        "order_id": order.id,
                        "payment_id": payment.id,
                    }
                },
            )
        except Exception as e:
            return Response(
                {"message": f"{e}"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response({"url": f"{checkout_session.url}"}, status=status.HTTP_200_OK)


class StripeWebhookViewSet(viewsets.ViewSet):
    """
    Webhook handler for Stripe
    """

    @action(
        methods=["POST"],
        detail=False,
        url_path="events-handler",
        url_name="events-handler",
    )
    def events_handler(self, request, *args, **kwargs):
        payload = request.body
        sig_header = request.META["HTTP_STRIPE_SIGNATURE"]
        event = None

        try:
            event = stripe.Webhook.construct_event(
                payload, sig_header, settings.STRIPE_WEBHOOK_SIGNING_SECRET_KEY
            )
        except ValueError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        except stripe.error.SignatureVerificationError:
            return Response(status=status.HTTP_400_BAD_REQUEST)

        session = event["data"]["object"]

        metadata = session["metadata"]
        user_id = int(metadata["user_id"])
        order_id = int(metadata["order_id"])
        paymend_id = int(metadata["payment_id"])

        match event["type"]:
            case "payment_intent.succeeded":
                Payment.objects.filter(id=paymend_id).update(
                    status="COMPLETED", amount_paid=session["amount"]/100
                )
                utils.send_payment_succeeded_email(
                    user_id, paymend_id, session["amount"] / 100, session["currency"]
                )

            case "checkout.session.completed":
                Order.objects.filter(id=metadata["order_id"]).update(status="PLACED")
                CartItem.objects.filter(
                    cart=Cart.objects.only("id").get(user=metadata["user_id"])
                ).delete()
                utils.send_order_confirmation_email(user_id, order_id)

            case "payment_intent.payment_failed":
                Payment.objects.filter(id=paymend_id).update(status="FAILED")
                utils.send_payment_failed_email(
                    user_id,
                    session["amount"] * 100,
                    session["currency"],
                    error_message=session["last_payment_error"]["message"],
                )

        return Response(status=status.HTTP_200_OK)
