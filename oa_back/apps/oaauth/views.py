from rest_framework import status
from rest_framework.views import APIView
from .serializers import LoginSerializer, UserSerializer, ResetPwdSerializer
from datetime import datetime
from .authentications import generate_jwt
from rest_framework.response import Response

class LoginView(APIView):
    def post(self, request):
        serializer = LoginSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.validated_data['user']
            user.last_login = datetime.now()
            user.save()
            token = generate_jwt(user)
            return Response({'token': token, 'user': UserSerializer(user).data})
        else:
            print(serializer.errors)
            detail = list(serializer.errors.values())[0][0]
            return Response({'detail': detail }, status=status.HTTP_400_BAD_REQUEST)

class ResetPwdView(APIView):
    def post(self, request):
        # context可以传递自己的参数
        serializer = ResetPwdSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            pwd1 = serializer.validated_data['pwd1']
            request.user.set_password(pwd1)
            request.user.save()
            return Response()
        else:
            print(serializer.errors)
            detail = list(serializer.errors.values())[0][0]
            return Response({'detail': detail}, status=status.HTTP_400_BAD_REQUEST)