from django.urls import path
from . import views
from rest_framework.routers import DefaultRouter

app_name = 'absent'
# 视图集可以利用drf自动生成路由(trailing_slash: 去掉末尾斜杠)
router = DefaultRouter(trailing_slash=False)
router.register('absent', views.AbsentViewSet, basename='absent')  # 注意absent只是针对视图集AbsentViewSet的前缀

urlpatterns = [
    path('type', views.AbsentTypeView.as_view(), name='absenttypes'),
    path('responder', views.ResponsderView.as_view(), name='getresponder'),
] + router.urls