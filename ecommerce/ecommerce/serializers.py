from rest_framework import serializers


class HTTP4XXExceptionSerializer(serializers.Serializer):
    detail = serializers.CharField()
