from rest_framework.reverse import reverse
from category.serializers import CategoryListSerializer, CategoryDetailSerializer


def test_category_list(category, anonymous_client):
    response = anonymous_client.get(reverse("category:list"))
    assert response.status_code == 200
    serializer = CategoryListSerializer([category], many=True)
    assert response.data["results"] == serializer.data


def test_category_detail(category, anonymous_client):
    response = anonymous_client.get(
        reverse("category:detail", kwargs={"pk": category.id})
    )
    assert response.status_code == 200
    serializer = CategoryDetailSerializer(category)
    assert response.data == serializer.data
