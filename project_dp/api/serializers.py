from rest_framework import serializers
from telecom.models import PhoneNumber

class PhoneNumberSerializer(serializers.ModelSerializer):
    operator_name = serializers.CharField(source='operator.name', read_only=True)

    class Meta:
        model = PhoneNumber
        fields = ('operator_name', 'region')
