import base64
import pyotp
from user.models import User, OTP
from django.conf import settings
from datetime import timedelta
from django.utils import timezone
from notification.tasks import notify_by_email, notify_by_sms


class OTPHandler:
    def __init__(self, user_id, timeout, otp_for):
        self.user = User.objects.get(id=user_id)
        self.timeout = timeout
        self.otp, self.otp_status = OTP.objects.get_or_create(user=self.user)
        self.otp_for = otp_for
        self.hotp = pyotp.HOTP(
            s=self.get_secret_key_base32_encoded(),
            digits=6,
        )

    def generate_otp(self):
        self.otp.count += 1
        self.otp.save()
        otp_code = self.hotp.at(self.otp.count)
        return otp_code

    def verify_otp(self, otp):
        valid_datetime = self.otp.datetime + timedelta(minutes=self.timeout)
        if timezone.now() < valid_datetime:
            return self.hotp.verify(otp, self.otp.count)
        return False

    def get_secret_key_base32_encoded(self):
        """
        Returns secret key in base 32 encoded format
        """
        return base64.b32encode(self.get_secret_key_bytes())

    def get_secret_key_bytes(self):
        """
        Returns secret key in bytes format
        """
        return bytes(self.get_secret_key(), "utf-8")

    def get_secret_key(self):
        return f"{settings.SECRET_KEY}{self.otp_for}{self.user.pk}{self.user.password}{self.user.email}{self.user.is_email_verified}{self.user.phone_number}{self.user.is_phone_number_verified}{self.user.last_login}"


def send_email_verification_otp(otp, email):
    subject = "OTP For Email Verification"
    message = f"Your OTP for email verification is {otp}. Please do not share this OTP with anyone."
    notify_by_email.delay(subject, message, email)


def send_phone_number_verification_otp(otp, phone_number):
    message = f"Your OTP for phone number verification is {otp}. Please do not share this OTP with anyone."
    notify_by_sms.delay(message, phone_number)


def send_password_reset_otp(otp, email):
    subject = "OTP For Password Reset"
    message = f"Your OTP for password reset is {otp}. Please do not share this OTP with anyone."
    notify_by_email.delay(subject, message, email)
