from rest_framework.reverse import reverse
from user.serializers import AddressSerializer


def test_list_address(address_client):
    address, client = address_client
    response = client.get(reverse("user:list-address"))
    assert response.status_code == 200
    serializer = AddressSerializer([address], many=True)
    assert response.data == serializer.data


def test_get_address(address_client):
    address, client = address_client
    response = client.get(reverse("user:get-address", kwargs={"id": address.id}))
    assert response.status_code == 200
    serializer = AddressSerializer(address)
    assert response.data == serializer.data


def test_create_address(address_factory, authenticated_client):
    new_address = address_factory.build()
    payload = {
        "type": new_address.type,
        "house_number": new_address.house_number,
        "landmark": new_address.landmark,
        "address_line1": new_address.address_line1,
        "address_line2": new_address.address_line2,
        "city": new_address.city,
        "state": new_address.state,
        "country": new_address.country,
        "postal_code": new_address.postal_code,
        "is_default": new_address.is_default,
    }
    response = authenticated_client.post(reverse("user:create-address"), payload)
    assert response.status_code == 201


def test_update_address(address_client):
    address, client = address_client
    payload = {"house_number": "1234"}
    response = client.patch(
        reverse("user:update-address", kwargs={"id": address.id}), payload
    )
    assert response.status_code == 201


def test_delete_address(address_client):
    address, client = address_client
    response = client.delete(reverse("user:delete-address", kwargs={"id": address.id}))
    assert response.status_code == 204
