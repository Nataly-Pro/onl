from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, \
    TokenRefreshView

from users.apps import UsersConfig
from users.views import UserListCreateView

app_name = UsersConfig.name

urlpatterns = [
    path('', UserListCreateView.as_view(), name='users'),

    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
]
