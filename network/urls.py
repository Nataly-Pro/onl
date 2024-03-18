from rest_framework.routers import DefaultRouter

from network.apps import NetworkConfig
from network.views import NetworkViewSet

app_name = NetworkConfig.name

router = DefaultRouter()
router.register('network', NetworkViewSet, basename='network')
urlpatterns = router.urls
