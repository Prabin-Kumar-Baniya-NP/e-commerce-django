from rest_framework.reverse import reverse


def test_product_list(product, anonymous_client):
    response = anonymous_client.get(reverse("product:list"))
    assert response.status_code == 200


def test_product_detail(product, anonymous_client):
    response = anonymous_client.get(
        reverse("product:detail", kwargs={"pk": product.id})
    )
    assert response.status_code == 200
