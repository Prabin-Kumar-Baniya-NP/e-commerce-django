from rest_framework.reverse import reverse
from reviews.serializers import ReviewsReadSerializer


def test_reviews_list(reviews, anonymous_client):
    response = anonymous_client.get(reverse("reviews:list"))
    assert response.status_code == 200
    serializer = ReviewsReadSerializer([reviews], many=True)
    assert response.data["results"] == serializer.data


def test_reviews_detail(reviews, anonymous_client):
    response = anonymous_client.get(
        reverse("reviews:detail", kwargs={"pk": reviews.id})
    )
    assert response.status_code == 200
    serializer = ReviewsReadSerializer(reviews)
    assert response.data == serializer.data


def test_reviews_create(reviews, user_client):
    user, client = user_client
    payload = {
        "user": user.id,
        "product": reviews.product.id,
        "rating": 4,
        "comment": "good product",
    }
    response = client.post(reverse("reviews:create"), payload)
    assert response.status_code == 201


def test_reviews_update(reviews_client):
    reviews, client = reviews_client
    payload = {
        "comment": "new review comment",
    }
    response = client.patch(
        reverse("reviews:update", kwargs={"pk": reviews.id}), payload
    )
    assert response.status_code == 200


def test_reviews_delete(reviews_client):
    reviews, client = reviews_client
    response = client.delete(reverse("reviews:delete", kwargs={"pk": reviews.id}))
    assert response.status_code == 204


def test_user_reviews_list(reviews_client):
    reviews, client = reviews_client
    response = client.get(reverse("reviews:user-reviews-list"))
    assert response.status_code == 200
    serializer = ReviewsReadSerializer([reviews], many=True)
    assert response.data["results"] == serializer.data


def test_user_reviews_detail(reviews_client):
    reviews, client = reviews_client
    response = client.get(
        reverse("reviews:user-reviews-detail", kwargs={"pk": reviews.id})
    )
    assert response.status_code == 200
    serializer = ReviewsReadSerializer(reviews)
    assert response.data == serializer.data
