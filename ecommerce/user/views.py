from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.exceptions import NotFound
from rest_framework import status
from user.models import User, Address
from user.serializers import AddressSerializer, AddressUpdateSerializer


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def list_address(request):
    """
    List the address of user
    """
    address_list = Address.objects.filter(user=request.user.id)
    serializer = AddressSerializer(address_list, many=True)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_address(request, id):
    """
    Get the instance of the address
    """
    try:
        address = Address.objects.get(id=id, user=request.user.id)
    except Address.DoesNotExist:
        raise NotFound(detail="Address Not Found")
    serializer = AddressSerializer(address)
    return Response(data=serializer.data, status=status.HTTP_200_OK)


@api_view(["POST"])
@permission_classes([IsAuthenticated])
def create_address(request):
    """
    Create a new address for authenticated user
    """
    serializer = AddressSerializer(data=request.data, context={"user": request.user})
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(["PUT", "PATCH"])
@permission_classes([IsAuthenticated])
def update_address(request, id):
    """
    Updates the existing address of the user
    """
    try:
        address = Address.objects.get(id=id, user=request.user.id)
    except Address.DoesNotExist:
        raise NotFound(detail="Address Not Found")

    if request.method == "PATCH":
        serializer = AddressUpdateSerializer(
            instance=address, data=request.data, partial=True
        )
    else:
        serializer = AddressUpdateSerializer(instance=address, data=request.data)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    return Response(data=serializer.data, status=status.HTTP_201_CREATED)


@api_view(["DELETE"])
@permission_classes([IsAuthenticated])
def delete_address(request, id):
    """
    Deletes the address of the user
    """
    try:
        address = Address.objects.get(id=id)
    except Address.DoesNotExist:
        raise NotFound(detail="Address Not Found")
    address.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)
