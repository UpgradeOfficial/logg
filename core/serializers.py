from rest_framework import serializers

class ContactUsSerializer(serializers.Serializer):
    subject = serializers.CharField()
    email = serializers.EmailField()
    name = serializers.CharField()
    text = serializers.CharField()