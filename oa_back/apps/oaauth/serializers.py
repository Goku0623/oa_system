from .models import OAUser, UserStatusChoices, OADepartment
from rest_framework import serializers

class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, max_length=20, min_length=6)

    def validate(self, data):
        email = data.get('email')
        password = data.get('password')
        if email and password:
            user = OAUser.objects.get(email=email)
            if not user:
                raise serializers.ValidationError('请输入正确的邮箱！')
            if not user.check_password(password):
                raise serializers.ValidationError('请输入正确的密码！')
            if user.status != UserStatusChoices.UNACTIVE:
                raise serializers.ValidationError('该用户尚未激活！')
            if user.status != UserStatusChoices.LOCKED:
                raise serializers.ValidationError('该用户已被锁定，请联系管理员')
            # 为节省sql查询次数，直接把user放到校验的data中，方便在视图中查询
            data['user'] = user
        else:
            raise serializers.ValidationError('请传入邮箱和密码')
        return data

class DepartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = OADepartment
        fields = '__all__'

class UserSerializer(serializers.ModelSerializer):
    # 重写部分对象，返回的不只是部门id，而是整个部门对象
    department = DepartmentSerializer()
    class Meta:
        model = OAUser
        exclude = ('password', 'groups', 'user_permissions')

