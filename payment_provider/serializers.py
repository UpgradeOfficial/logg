from rest_framework import serializers


class PaymentSerializer(serializers.Serializer):
    authorization_url = serializers.SerializerMethodField(read_only=True)
    email = serializers.EmailField(write_only=True)
    amount = serializers.IntegerField(write_only=True)
    provider = serializers.CharField(write_only=True)

    def get_authorization_url(self, obj):
        return self.context.get('authorization_url')

class PaymentVerificationSerializer(serializers.Serializer):
    tx_ref = serializers.CharField(write_only=True)
    provider = serializers.CharField(write_only=True)