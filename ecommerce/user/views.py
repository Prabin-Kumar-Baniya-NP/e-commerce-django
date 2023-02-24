from django.db.models import RestrictedError
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import status
from rest_framework.exceptions import AuthenticationFailed, PermissionDenied, NotFound
from user.models import Address
from user.utils import OTPHandler
from django.contrib.auth import get_user_model
from django.conf import settings
from user.utils import (
    send_email_verification_otp,
    send_phone_number_verification_otp,
    send_password_reset_otp,
)
from rest_framework import serializers
from ecommerce.serializers import HTTP4XXExceptionSerializer
from user.serializers import (
    UserRegistrationSerializer,
    UserDetailSerializer,
    UserUpdateSerializer,
    PasswordChangeSerializer,
    ResetPasswordSerializer,
    AddressSerializer,
)
from drf_spectacular.utils import (
    extend_schema,
    extend_schema_view,
    OpenApiParameter,
    OpenApiResponse,
    inline_serializer,
)

User = get_user_model()


@extend_schema(
    request=UserRegistrationSerializer,
    responses={
        201: UserRegistrationSerializer,
        400: OpenApiResponse(
            response=HTTP4XXExceptionSerializer, description="Data Validation Error"
        ),
    },
)
@api_view(["POST"])
def signup(request):
    """
    Creates a new user
    """
    serializer = UserRegistrationSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    request=UserUpdateSerializer,
    responses={
        201: UserUpdateSerializer,
        400: OpenApiResponse(
            response=HTTP4XXExceptionSerializer, description="Data Validation Error"
        ),
    },
)
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_user(request):
    """
    Updates the user data
    """
    serializer = UserUpdateSerializer(
        instance=request.user,
        data=request.data,
        partial=True if request.method == "PATCH" else False,
    )
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(responses={200: UserDetailSerializer})
@api_view(["GET"])
def user_detail(request):
    """
    Returns user data
    """
    serializer = UserDetailSerializer(request.user)
    return Response(serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    request=PasswordChangeSerializer,
    responses={
        201: OpenApiResponse(
            response=None, description="Password Changed Successfully"
        ),
        400: OpenApiResponse(
            response=HTTP4XXExceptionSerializer,
            description="Password Validation Failed",
        ),
    },
)
@api_view(["PUT"])
def change_password(request):
    """
    Changes the password of user
    """
    serializer = PasswordChangeSerializer(instance=request.user, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(status=status.HTTP_201_CREATED)


@extend_schema_view(
    get=extend_schema(
        description="Sends OTP to Email Address",
        responses={
            200: inline_serializer(
                name="VerifyEmailAddress",
                fields={
                    "status": serializers.CharField(),
                    "validity": serializers.CharField(),
                },
            ),
            403: OpenApiResponse(
                response=HTTP4XXExceptionSerializer,
                description="Email Address already verified",
            ),
            404: OpenApiResponse(
                response=HTTP4XXExceptionSerializer,
                description="Email Address Not Found",
            ),
        },
    ),
    post=extend_schema(
        description="Verfies OTP for user sent to email address",
        request=inline_serializer(
            name="EmailAddressOTPSerializer",
            fields={
                "otp": serializers.CharField(),
            },
        ),
        responses={
            200: OpenApiResponse(
                response=None,
                description="Email Address Verified Successfully",
            ),
            401: OpenApiResponse(
                response=HTTP4XXExceptionSerializer,
                description="OTP Verification Failed",
            ),
        },
    ),
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def verify_email(request):
    """
    Sends and verifies email through OTP
    """
    otp = OTPHandler(request.user.id, settings.OTP_LIFETIME, "email")

    if request.method == "GET":
        if not request.user.is_email_verified:
            otp = otp.generate_otp()
            send_email_verification_otp(otp, request.user.email)

            context = {
                "status": f"OTP sent to {request.user.email}",
                "validity": f"{settings.OTP_LIFETIME} minutes",
            }
            return Response(context, status=status.HTTP_200_OK)
        else:
            raise PermissionDenied("Email already verified")

    if request.method == "POST":
        otp_verified = otp.verify_otp(request.data["otp"])
        if otp_verified:
            request.user.verify_email()
            return Response(status=status.HTTP_200_OK)
        raise AuthenticationFailed("OTP is invalid or expired")


@extend_schema_view(
    get=extend_schema(
        description="Sends OTP to Phone number",
        responses={
            200: inline_serializer(
                name="VerifyPhoneNumber",
                fields={
                    "status": serializers.CharField(),
                    "validity": serializers.CharField(),
                },
            ),
            403: OpenApiResponse(
                response=HTTP4XXExceptionSerializer,
                description="Phone number already verified",
            ),
            404: OpenApiResponse(
                response=HTTP4XXExceptionSerializer,
                description="Phone Number Not Found",
            ),
        },
    ),
    post=extend_schema(
        description="Verfies OTP for user sent to phone number",
        request=inline_serializer(
            name="PhoneNumberOTPSerializer",
            fields={
                "otp": serializers.CharField(),
            },
        ),
        responses={
            200: OpenApiResponse(
                response=None,
                description="Phone Number Verified Successfully",
            ),
            401: OpenApiResponse(
                response=HTTP4XXExceptionSerializer,
                description="OTP Verification Failed",
            ),
        },
    ),
)
@api_view(["GET", "POST"])
@permission_classes([IsAuthenticated])
def verify_number(request):
    """
    Sends and verifies phone number through OTP
    """
    otp = OTPHandler(request.user.id, settings.OTP_LIFETIME, "phone_number")

    if request.method == "GET":
        if request.user.phone_number:
            if not request.user.is_phone_number_verified:
                otp = otp.generate_otp()
                send_phone_number_verification_otp(
                    otp, request.user.phone_number.as_e164
                )

                context = {
                    "status": f"OTP sent to {request.user.phone_number}",
                    "validity": f"{settings.OTP_LIFETIME} minutes",
                }
                return Response(context, status=status.HTTP_200_OK)
            raise PermissionDenied("Phone number already verified")
        raise NotFound("Phone Number Not Found")

    if request.method == "POST":
        otp_verified = otp.verify_otp(request.data["otp"])
        if otp_verified:
            request.user.verify_phone_number()
            return Response(status=status.HTTP_200_OK)
        raise AuthenticationFailed("OTP is invalid or expired")


@extend_schema_view(
    get=extend_schema(
        responses={
            200: inline_serializer(
                name="ResetPassword",
                fields={
                    "status": serializers.CharField(),
                    "validity": serializers.CharField(),
                },
            )
        }
    ),
    post=extend_schema(
        request=inline_serializer(
            name="InlineResetPassword",
            fields={
                "otp": serializers.CharField(),
                "email": serializers.EmailField(),
                "password": serializers.CharField(),
                "password2": serializers.CharField(),
            },
        ),
        responses={
            201: OpenApiResponse(response=None, description="Password Reset Completed"),
            400: OpenApiResponse(
                response=HTTP4XXExceptionSerializer, description="Data Validation Error"
            ),
            401: OpenApiResponse(
                response=HTTP4XXExceptionSerializer,
                description="OTP Verification Failed",
            ),
        },
    ),
)
@api_view(["GET", "POST"])
def reset_password(request):
    """
    Sends password reset otp to email and resets the password
    """
    email = (
        request.query_params.get("email")
        if request.method == "GET"
        else request.data["email"]
    )
    try:
        user = User.objects.get(email=email)
    except User.DoesNotExist:
        raise NotFound("Email address is not registered")

    otp = OTPHandler(user.id, settings.OTP_LIFETIME, "reset-password")

    if request.method == "GET":
        otp = otp.generate_otp()
        send_password_reset_otp(otp, user.email)

        context = {
            "status": f"Password reset OTP sent to {user.email}",
            "validity": f"{settings.OTP_LIFETIME} minutes",
        }
        return Response(context, status=status.HTTP_200_OK)

    if request.method == "POST":
        otp_verified = otp.verify_otp(request.data["otp"])
        if otp_verified:
            serializer = ResetPasswordSerializer(instance=user, data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(status=status.HTTP_201_CREATED)
        raise AuthenticationFailed("OTP is invalid or expired")


@extend_schema(responses={200: AddressSerializer})
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_address(request):
    """
    List the address of user
    """
    address_list = Address.objects.filter(user=request.user)
    serializer = AddressSerializer(address_list, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    responses={
        200: AddressSerializer,
        404: OpenApiResponse(
            response=HTTP4XXExceptionSerializer, description="Address Not Found"
        ),
    }
)
@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_address(request, id):
    """
    Get the instance of the address
    """
    try:
        address = Address.objects.get(id=id, user=request.user)
    except Address.DoesNotExist:
        raise NotFound(detail="Address Not Found")
    serializer = AddressSerializer(address)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    request=AddressSerializer,
    responses={
        201: AddressSerializer,
        400: OpenApiResponse(
            response=HTTP4XXExceptionSerializer, description="Data Validation Error"
        ),
    },
)
@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_address(request):
    """
    Create a new address for authenticated user
    """
    serializer = AddressSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user)
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@extend_schema(
    request=AddressSerializer,
    responses={
        200: AddressSerializer,
        400: OpenApiResponse(
            response=HTTP4XXExceptionSerializer, description="Data Validation Error"
        ),
        404: OpenApiResponse(
            response=HTTP4XXExceptionSerializer, description="Address Not Found"
        ),
    },
)
@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_address(request, id):
    """
    Updates the existing address of the user
    """
    try:
        address = Address.objects.get(id=id, user=request.user)
    except Address.DoesNotExist:
        raise NotFound(detail="Address Not Found")

    serializer = AddressSerializer(
        instance=address,
        data=request.data,
        partial=True if request.method == "PATCH" else False,
    )

    serializer.is_valid(raise_exception=True)
    serializer.save(user=request.user)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@extend_schema(
    responses={
        204: OpenApiResponse(response=None, description="Address Deleted Successfully"),
        403: OpenApiResponse(
            response=HTTP4XXExceptionSerializer,
            description="Object is referenced to restricted foreign key",
        ),
        404: OpenApiResponse(
            response=HTTP4XXExceptionSerializer, description="Address Not Found"
        ),
    }
)
@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_address(request, id):
    """
    Deletes the address of the user
    """
    try:
        address = Address.objects.get(id=id, user=request.user)
    except Address.DoesNotExist:
        raise NotFound(detail="Address Not Found")
    try:
        address.delete()
    except RestrictedError as e:
        raise PermissionDenied("Object is referenced to restricted foreign key")
    return Response(status=status.HTTP_204_NO_CONTENT)
