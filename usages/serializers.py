from django.shortcuts import get_object_or_404

from rest_framework import serializers

from .models import Usage, UsageType
from .utils import get_calculated_emissions


class UsageTypeSerializer(serializers.ModelSerializer):

    class Meta:
        fields = ('id', 'name', 'unit', 'factor')
        model = UsageType


class UsageCreateUpdateSerializer(serializers.ModelSerializer):
    name = serializers.CharField(max_length=100, write_only=True)
    unit = serializers.CharField(max_length=10, write_only=True)

    class Meta:
        fields = (
            'id', 'user', 'amount', 'usage_at', 'name', 'unit'
        )
        model = Usage
        read_only_fields = ['user', 'calculated_emissions']

    def _get_usage_type(self, name, unit):
        usage_type = UsageType.objects.filter(name=name, unit=unit).first()
        if not usage_type:
            raise serializers.ValidationError(
                f'The option {name} with the unit {unit} does not exist.\
                    Check the available options.'
            )
        return usage_type

    def create(self, validated_data):
        user = self.context['request'].user
        name = validated_data.pop('name')
        unit = validated_data.pop('unit')
        usage_type = self._get_usage_type(name, unit)
        calculated_emissions = get_calculated_emissions(
            validated_data.get('amount'), usage_type.factor)

        return Usage.objects.create(
            user=user,
            usage_type=usage_type,
            calculated_emissions=calculated_emissions,
            **validated_data
        )

    def update(self, instance, validated_data):
        name = validated_data.pop('name', instance.usage_type.name)
        unit = validated_data.pop('unit', instance.usage_type.unit)
        usage_type = self._get_usage_type(name, unit)
        amount = validated_data.pop('amount', instance.amount)

        instance.calculated_emissions = get_calculated_emissions(
            amount, usage_type.factor)
        instance.amount = amount
        instance.usage_type = usage_type
        instance.usage_at = validated_data.get('usage_at', instance.usage_at)
        instance.save()
        return instance


class UsageSerializer(serializers.ModelSerializer):
    usage_type = UsageTypeSerializer(read_only=True)

    class Meta:
        fields = (
            'id', 'user', 'calculated_emissions', 'amount', 'usage_at',
            'usage_type'
        )
        model = Usage
