from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from network.models import NetworkObject


class NetworkObjectCreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = NetworkObject
        exclude = ('id', 'hierarchy',)


class NetworkObjectUpdateSerializer(serializers.ModelSerializer):

    class Meta:
        model = NetworkObject
        exclude = ('id',)
        read_only_fields = ('debt',)

    def update(self, instance, validated_data):

        fields = [key for key in instance.__dict__.keys()]
        for field in fields:
            instance.__dict__[field] = validated_data.get(field, instance.__dict__[field])

        if instance.object_type == 'factory' and instance.hierarchy != '0':
            raise ValidationError('Завод должен быть на 0 уровне иерархии в сети.')
        if instance.object_type != 'factory' \
                and instance.hierarchy != instance.supplier.hierarchy + 1:
            raise ValidationError('Уровень иерархии не соответствует правилу: '
                                  'поставщик - предыдущий по иерархии объект сети')
        if instance.hierarchy > 2:
            raise ValidationError('Некорректно выбран поставщик.')
        instance.save()
        return instance


class NetworkObjectViewSerializer(serializers.ModelSerializer):

    class Meta:
        model = NetworkObject
        fields = '__all__'
