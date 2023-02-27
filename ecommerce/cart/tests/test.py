from rest_framework.reverse import reverse
from cart.models import CartItem
from cart.serializers import CartSerializer, CartItemSerializer


def test_get_cart(cart_client):
    cart, client = cart_client
    response = client.get(reverse("cart:cart-get"))
    assert response.status_code == 200
    serializer = CartSerializer(cart)
    assert response.data == serializer.data


def test_clear_cart(cart_client):
    cart, client = cart_client
    response = client.delete(reverse("cart:cart-clear"))
    assert response.status_code == 204
    assert CartItem.objects.filter(cart=cart).exists() == False


def test_list_cart_item(cart_item_client):
    cart_item, client = cart_item_client
    response = client.get(reverse("cart:item-list"))
    assert response.status_code == 200
    serializer = CartItemSerializer([cart_item], many=True)
    assert response.data["results"] == serializer.data


def test_get_cart_item(cart_item_client):
    cart_item, client = cart_item_client
    response = client.get(reverse("cart:item-detail", kwargs={"pk": cart_item.id}))
    assert response.status_code == 200
    serializer = CartItemSerializer(cart_item)
    assert response.data == serializer.data


def test_create_cart_item(cart_client, product_variant_factory):
    variant = product_variant_factory.create()
    cart, client = cart_client
    payload = {
        "cart": cart.id,
        "variant": variant.id,
        "quantity": 2,
    }
    response = client.post(reverse("cart:item-list"), payload)
    assert response.status_code == 201


def test_update_cart_item(cart_item_client):
    cart_item, client = cart_item_client
    payload = {
        "quantity": 10,
    }
    response = client.patch(
        reverse("cart:item-detail", kwargs={"pk": cart_item.id}), payload
    )
    assert response.status_code == 200
    cart_item.refresh_from_db()
    assert cart_item.quantity == payload["quantity"]


def test_delete_cart_item(cart_item_client):
    cart_item, client = cart_item_client
    response = client.delete(reverse("cart:item-detail", kwargs={"pk": cart_item.id}))
    assert response.status_code == 204
