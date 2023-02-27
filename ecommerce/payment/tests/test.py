from rest_framework.reverse import reverse
from payment.serializers import PaymentReadSerializer


def test_list_payment(payment_client):
    payment, client = payment_client
    response = client.get(reverse("payment:payment-list"))
    assert response.status_code == 200
    serializer = PaymentReadSerializer([payment], many=True)
    assert response.data["results"] == serializer.data


def test_get_payment(payment_client):
    payment, client = payment_client
    response = client.get(reverse("payment:payment-detail", kwargs={"pk": payment.id}))
    assert response.status_code == 200
    serializer = PaymentReadSerializer(payment)
    assert response.data == serializer.data
