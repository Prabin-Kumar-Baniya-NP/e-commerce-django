from rest_framework import serializers


class HTTP4XXExceptionSerializer(serializers.Serializer):
    detail = serializers.CharField()

class InvalidDataResponseSerializer(serializers.Serializer):
    error = serializers.CharField()
    details = serializers.DictField(child=serializers.ListField(child=serializers.CharField()))