from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.password_validation import validate_password
from phonenumber_field.modelfields import PhoneNumberField


class UserManager(BaseUserManager):
    use_in_migrations = True

    def _create_user(self, email, password, **extra_fields):
        """
        Creates and saves a User with the given email and password.
        """
        if not email:
            raise ValueError("The given username must be set")
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_superuser", False)
        return self._create_user(email, password, **extra_fields)

    def create_superuser(self, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self._create_user(email, password, **extra_fields)


GENDER_CHOICES = [("M", "Male"), ("F", "Female")]


class User(AbstractBaseUser, PermissionsMixin):
    first_name = models.CharField(max_length=32)
    middle_name = models.CharField(max_length=32, null=True, blank=True)
    last_name = models.CharField(max_length=32)
    date_of_birth = models.DateField(
        help_text="Format: Year-Month-Day",
    )
    gender = models.CharField(
        max_length=1, choices=GENDER_CHOICES
    )
    email = models.EmailField(max_length=254, unique=True)
    is_email_verified = models.BooleanField("Email Verified", default=False)
    phone_number = PhoneNumberField(unique=True, null=True, blank=True)
    is_phone_number_verified = models.BooleanField("Phone Number Verified", default=False)
    image = models.ImageField(upload_to="profileImage/", null=True, blank=True)
    date_joined = models.DateTimeField(auto_now_add=True)
    last_updated = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["first_name", "last_name", "date_of_birth", "gender"]

    class Meta:
        verbose_name = "user"
        verbose_name_plural = "users"

    def __str__(self):
        return self.get_full_name()

    def get_full_name(self):
        """
        Returns the full name of user
        """
        return f"{self.first_name} {self.middle_name} {self.last_name}"
    
    def verify_email(self):
        """
        Sets is_email_verified to true
        """
        self.is_email_verified = True
        self.save()
        return None

    def verify_phone_number(self):
        """
        Sets is_phone_number_verified to true
        """
        self.is_phone_number_verified = True
        self.save()
        return None


ADDRESS_TYPE = (
    ("H", "Home Address"),
    ("W", "Work Address"),
    ("O", "Other"),
)


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    type = models.CharField(choices=ADDRESS_TYPE, max_length=1)
    house_number = models.CharField("House Number/ Street", max_length=128)
    landmark = models.CharField("LandMark/ Building", max_length=128)
    address_line1 = models.CharField(max_length=1024)
    address_line2 = models.CharField(max_length=1024, null=True, blank=True)
    city = models.CharField(max_length=64)
    state = models.CharField(max_length=64)
    country = models.CharField(max_length=64)
    postal_code = models.CharField(max_length=12)
    is_default = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    modified_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name() + " | " + self.type



class OTP(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="otp")
    count = models.PositiveIntegerField(default=0)
    datetime = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.user.get_full_name() + " | " + str(self.count)