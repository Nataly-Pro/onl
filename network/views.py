from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.exceptions import ValidationError

from network.models import NetworkObject
from network.permissions import UserPermissions
from network.serializers import NetworkObjectCreateSerializer, NetworkObjectUpdateSerializer, \
    NetworkObjectViewSerializer


class NetworkViewSet(viewsets.ModelViewSet):
    queryset = NetworkObject.objects.all()
    permission_classes = [UserPermissions]
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['country']

    def perform_create(self, serializer):
        new_object = serializer.save()
        if new_object.object_type == 'factory':
            new_object.hierarchy = 0
        else:
            if new_object.supplier:
                new_object.hierarchy = new_object.supplier.hierarchy + 1
            else:
                raise ValidationError('Не указан поставщик.')
        new_object.save()

    def get_serializer_class(self):
        if self.action == 'create':
            self.serializer_class = NetworkObjectCreateSerializer
        elif self.action in ['update', 'partial_update']:
            self.serializer_class = NetworkObjectUpdateSerializer
        elif self.action in ['retrieve', 'list', 'delete']:
            self.serializer_class = NetworkObjectViewSerializer

        return self.serializer_class
