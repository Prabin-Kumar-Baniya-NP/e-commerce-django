import pytest
import re
from rest_framework.reverse import reverse
from django.core import mail


@pytest.mark.django_db
def test_user_can_signup(user_factory, anonymous_client):
    new_user = user_factory.build()
    payload = {
        "first_name": new_user.first_name,
        "last_name": new_user.last_name,
        "email": new_user.email,
        "gender": new_user.gender,
        "date_of_birth": "2000-01-01",
        "password": new_user.password,
        "password2": new_user.password,
    }
    response = anonymous_client.post(reverse("user:signup"), payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_user_can_update_date_of_birth(authenticated_client):
    payload = {
        "date_of_birth": "2001-11-11",
    }
    response = authenticated_client.patch(reverse("user:update"), payload)
    assert response.status_code == 201


@pytest.mark.django_db
def test_user_can_view_user_details(authenticated_client):
    response = authenticated_client.get(reverse("user:detail"))
    assert response.status_code == 200


@pytest.mark.django_db
def test_user_can_change_password(authenticated_client):
    payload = {
        "password": "new_password@12345",
        "password2": "new_password@12345",
    }
    response = authenticated_client.put(reverse("user:change-password"), payload)
    assert response.status_code == 201

@pytest.mark.django_db
def test_user_can_get_email_verification_otp(authenticated_client):
    response = authenticated_client.get(reverse("user:verify-email"))
    assert len(mail.outbox) == 1
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_can_verify_email(authenticated_client):
    authenticated_client.get(reverse("user:verify-email"))
    email_body = mail.outbox[0].body
    otp = re.findall(r'\b\d{6}\b', email_body)
    payload = {
        "otp": otp[0],
    }
    response = authenticated_client.post(reverse("user:verify-email"), payload)
    assert response.status_code == 200

@pytest.mark.django_db
def test_user_can_get_password_reset_otp(authenticated_client):
    pass
