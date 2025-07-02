from rest_framework.routers import DefaultRouter
from apps.inform.views import InformViewSet

router = DefaultRouter(trailing_slash=False)
router.register('inform', InformViewSet)

urlpatterns = [] + router.urls