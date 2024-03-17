from rest_framework import viewsets, generics
from rest_framework.permissions import IsAdminUser, IsAuthenticated

from users.models import User
from users.serializer import UserSerializer


class UserListCreateView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]

    def perform_create(self, serializer):
        user = serializer.save()
        user.set_password(user.password)
        user.save()




