from rest_framework.reverse import reverse
from inventory.serializers import InventorySerializer

def test_inventory_detail(inventory, anonymous_client):
    response = anonymous_client.get(reverse("inventory:detail", kwargs={"variant": inventory.variant.id}))
    assert response.status_code == 200
    serializer = InventorySerializer(inventory)
    assert response.data == serializer.data