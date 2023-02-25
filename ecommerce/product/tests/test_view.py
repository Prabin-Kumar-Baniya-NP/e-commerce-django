from rest_framework.reverse import reverse
from product.models import Product

def test_product_list(multi_variant_product, anonymous_client):
    response = anonymous_client.get(reverse("product:list"))
    assert response.status_code == 200


def test_product_detail(multi_variant_product, anonymous_client):
    response = anonymous_client.get(reverse("product:detail", kwargs={"pk": multi_variant_product.id}))
    assert response.status_code == 200