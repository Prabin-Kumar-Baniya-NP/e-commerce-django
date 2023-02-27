from rest_framework.reverse import reverse
from order.serializers import OrderReadSerializer, OrderItemSerializer


def test_list_order(order_client):
    order, client = order_client
    response = client.get(reverse("order:order-list"))
    assert response.status_code == 200
    serializer = OrderReadSerializer([order], many=True)
    assert response.data["results"] == serializer.data


def test_get_order(order_client):
    order, client = order_client
    response = client.get(reverse("order:order-detail", kwargs={"pk": order.id}))
    assert response.status_code == 200
    serializer = OrderReadSerializer(order)
    assert response.data == serializer.data


def test_create_order(user_client, address_factory, cart_factory, cart_item_factory):
    user, client = user_client
    address = address_factory.create(user=user)
    cart = cart_factory.create(user=user)
    cart_item = cart_item_factory.create(cart=cart)
    payload = {
        "user": user.id,
        "shipping_address": address.id,
    }
    response = client.post(reverse("order:order-list"), payload)
    assert response.status_code == 201


def test_delete_order(order_client):
    order, client = order_client
    response = client.delete(reverse("order:order-detail", kwargs={"pk": order.id}))
    assert response.status_code == 204


def test_list_order_item(order_client):
    order, client = order_client
    order_item = order.order_item.all()[0]
    response = client.get(
        reverse("order:item-list", kwargs={"order_id": order.id})
    )
    assert response.status_code == 200
    serializer = OrderItemSerializer([order_item], many=True)
    assert response.data["results"] == serializer.data


def test_delete_order_item(order_client):
    order, client = order_client
    order_item = order.order_item.all()[0]
    response = client.delete(
        reverse(
            "order:item-detail",
            kwargs={"order_id": order.id, "pk": order_item.id},
        )
    )
    assert response.status_code == 204
