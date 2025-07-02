from rest_framework import viewsets, status
from .models import Inform, InformRead
from.serializers import InformSerializer
from django.db.models import Q
from rest_framework.response import Response

class InformViewSet(viewsets.ModelViewSet):
    queryset = Inform.objects.all()
    serializer_class = InformSerializer  # 在使用视图集viewset的时候不需要显式传递context["request"]

    # 通知列表：三种情况可见
    # 1. inform.public = True
    # 2. inform.departments包含了用户所在的部门
    # 3. inform.author = request.user
    def get_queryset(self):
        return self.queryset.select_related('author').prefetch_related("reads", "departments").filter(Q(public=True) | Q(department=self.request.user.department) | Q(author=self.request.user)).distinct()

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        if instance.author.uid == request.user.uid:
            self.perform_destroy(instance)
            return Response(status=status.HTTP_204_NO_CONTENT)
        else:
            return Response(status=status.HTTP_401_UNAUTHORIZED)