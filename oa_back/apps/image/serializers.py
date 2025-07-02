from rest_framework import serializers
from django.core.validators import FileExtensionValidator

class UploadImageSerializer(serializers.Serializer):
    image = serializers.ImageField(
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'jpeg', 'png', 'gif'])],
        error_messages={"required": "请上传图片！", "invalid_image": "请上传正确格式的图片！"}
    )

    def validate_image(self, value):
        max_size = 5 * 1024 * 1024
        if value.size > max_size:
            raise serializers.ValidationError("图片最大不能超过5MB！")