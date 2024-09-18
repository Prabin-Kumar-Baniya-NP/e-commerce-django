import stripe
from django.conf import settings
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.reverse import reverse
from payment.serializers import PaymentReadSerializer
from payment.models import Payment
from order.models import Order
from payment.models import Payment
from cart.models import Cart, CartItem
from payment import utils
from drf_spectacular.utils import extend_schema, inline_serializer, OpenApiResponse
from rest_framework import serializers


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentReadSerializer
    queryset = Payment.objects.all()
    http_method_names = ["get"]
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return super().get_queryset().filter(order__user__id=self.request.user.id).order_by("-id")


class PaymentStatusViewSet(viewsets.ViewSet):
    """
    Viewset for payment success and cancel
    """

    @extend_schema(
        responses={
            200: inline_serializer(
                name="success", fields={"message": serializers.CharField()}
            )
        }
    )
    @action(methods=["GET"], detail=False, url_path="success", url_name="success")
    def success(self, request, *args, **kwargs):
        return Response({"message": "success"}, status=status.HTTP_200_OK)

    @extend_schema(
        responses={
            200: inline_serializer(
                name="cancel", fields={"message": serializers.CharField()}
            )
        }
    )
    @action(methods=["GET"], detail=False, url_path="cancel", url_name="cancel")
    def cancel(self, request, *args, **kwargs):
        return Response({"message": "failed"}, status=status.HTTP_200_OK)


class StripeViewSet(viewsets.ViewSet):
    """
    Payment Handler For Stripe
    """

    permission_classes = [IsAuthenticated]

    @extend_schema(
        description="Creates a stripe checkout session for user cart items",
        request=inline_serializer(name="StripeSession", fields={}),
        responses={
            200: inline_serializer(
                name="checkout", fields={"checkout_session_url": serializers.URLField()}
            ),
            400: OpenApiResponse(
                response=None, description="Error creating stripe checkout session."
            ),
        },
    )
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
        except Exception:
            return Response(
                status=status.HTTP_400_BAD_REQUEST,
            )
        return Response(
            {"checkout_session_url": f"{checkout_session.url}"},
            status=status.HTTP_200_OK,
        )


class StripeWebhookViewSet(viewsets.ViewSet):
    """
    Webhook handler for Stripe
    """

    @extend_schema(
        request=inline_serializer(name="StripeSessionSchema", fields={}),
        responses={
            200: OpenApiResponse(response=None, description="Stripe Event Captured")
        },
    )
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
                    status="COMPLETED", amount_paid=session["amount"] / 100
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
