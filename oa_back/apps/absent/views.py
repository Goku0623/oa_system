from rest_framework.views import APIView
from .models import Absent,AbsentType,AbsentStatusChoices
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework import mixins
from .serializers import AbsentSerializer, AbsentTypeSerializer
from .utils import get_responder
from apps.oaauth.serializers import UserSerializer


class AbsentViewSet(mixins.CreateModelMixin,
                    mixins.UpdateModelMixin,
                    mixins.ListModelMixin,
                    viewsets.GenericViewSet):
    queryset = Absent.objects.all()
    serializer_class = AbsentSerializer

    def update(self, request, *args, **kwargs):
        # 允许修改部分数据
        kwargs['partial'] = True
        return super().update(request, *args, **kwargs)
    # 注意重写list方法后，drf的全局分页不生效，需生效则要重写
    def list(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        who = request.query_params.get('who')
        if who and who == 'sub':
            result = queryset.filter(responder=request.user)
        else:
            result = queryset.filter(requester=request.user)
        # result：符合要求的数据
        # paginate_queryset：会做分页的逻辑处理
        page = self.paginate_queryset(queryset)
        if page is not None:
            serializer = self.get_serializer(page, many=True)
            # get_paginated_response：除了返回序列化后的数据，还返回总数据量以及上一页的url
            return self.get_paginated_response(serializer.data)

        serializer = self.serializer_class(result, many=True)
        return Response(serializer.data)

# 1. 请假类型
class AbsentTypeView(APIView):
    def get(self, request):
        types = AbsentType.objects.all()
        serializer = AbsentTypeSerializer(types, many=True)
        return Response(serializer.data)

# 2. 显示审批者
class ResponsderView(APIView):
    def get(self, request):
        responder = get_responder(request)
        serializer = UserSerializer(responder)
        return Response(serializer.data)