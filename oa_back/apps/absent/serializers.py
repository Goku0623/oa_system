from rest_framework import serializers
from .models import Absent, AbsentType, AbsentStatusChoices
from apps.oaauth.serializers import UserSerializer
from rest_framework import exceptions
from .utils import get_responder

class AbsentTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = AbsentType
        fields = '__all__'

class AbsentSerializer(serializers.ModelSerializer):
    # read_only: 这个参数，只会在将0RM模型序列化成字典时会将这个字段序列化
    # write_only: 这个参数，只会在将data进行校验的时候才会用到
    absent_type = AbsentTypeSerializer(read_only=True)
    absent_type_id = serializers.IntegerField(write_only=True)
    requester = UserSerializer(read_only=True)
    responder = UserSerializer(read_only=True)
    class Meta:
        model = Absent
        fields = '__all__'

    # 验证 absent_type_id 是否在数据库中存在
    def validate_absent_type_id(self, value):
        if not AbsentType.objects.filter(pk=value).exists():
            raise exceptions.ValidationError('考情类型不存在！')
    def create(self, validated_data):
        request = self.context['request']
        user = request.user
        # 获取审批者
        responder = get_responder(request)
        if responder is None:
            validated_data['status'] = AbsentStatusChoices.PASS
        else:
            validated_data['status'] = AbsentStatusChoices.AUDITING

        return Absent.objects.create(**validated_data, requester=user, responder=responder)

    def update(self, instance, validated_data):
        if instance.status != AbsentStatusChoices.AUDITING:
            raise exceptions.APIException(detail='当前请假正在审批中！')
        request = self.context['request']
        user = request.user
        if user.uid != instance.responder.uid:
            raise exceptions.AuthenticationFailed(detail='您无权处理该考勤')
        instance.response_content = validated_data['response_content']
        instance.save()
        return instance
