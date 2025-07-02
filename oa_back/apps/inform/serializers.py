from apps.oaauth.models import OADepartment
from rest_framework import serializers
from .models import Inform, InformRead
from apps.oaauth.serializers import UserSerializer, DepartmentSerializer

class InformSerializer(serializers.ModelSerializer):
    author = UserSerializer(read_only=True)
    departments = DepartmentSerializer(read_only=True, many=True)
    # 如果后端需要接受列表，那么就要用到ListField
    departments_id = serializers.ListField(write_only=True)
    class Meta:
        model = Inform
        fields = "__all__"
        read_only_fields = ("public",)

        def create(self, validated_data):
            request = self.context["request"]
            departments_id = validated_data.pop("departments_id")
            # 对列表中的每个元素都做相同的操作，使用map函数
            departments_id = list(map(lambda value: int(value), departments_id))
            if 0 in departments_id:
                inform = Inform.objects.create(public=True, author=request.user, **validated_data)
            else:
                departments = OADepartment.objects.filter(id__in=departments_id).all()
                inform = Inform.objects.create(public=False, author=request.user, **validated_data)
                inform.departments.set(departments)
                inform.save()
            return inform