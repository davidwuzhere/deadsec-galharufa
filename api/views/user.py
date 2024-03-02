from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import permission_classes
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from django.contrib.auth.models import User
from .utils.user import get_tokens_for_user
from ..serializers.user import LoginSerializer, RegistrationSerializer, PasswordChangeSerializer, UserSerializer, GetUserSerializer
from drf_yasg.utils import swagger_auto_schema


class RegistrationView(APIView):
    @swagger_auto_schema(
        request_body=RegistrationSerializer(),
        responses={201: RegistrationSerializer(),
                   400: "Bad request"},
        operation_description="Registrates new user",
        tags=['user'],
        security=[],
    )
    def post(self, request):
        serializer = RegistrationSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LoginView(APIView):
    @swagger_auto_schema(
        request_body=LoginSerializer(),
        responses={200: 'Login Success',
                   401: 'Invalid Credentials'},
        operation_description="Login",
        tags=['user'],
        security=[],
    )
    def post(self, request):
        if 'username' not in request.data or 'password' not in request.data:
            return Response({'msg': 'Nome de usuário e/ou senha inválidos.'}, status=status.HTTP_400_BAD_REQUEST)
        username = request.data['username'].lower()
        password = request.data['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            auth_data = get_tokens_for_user(request.user)
            if user.is_active == False:
                user.is_active = True
                user.save()
            return Response({'msg': 'Login Success', 'id': user.pk, **auth_data}, status=status.HTTP_200_OK)
        return Response({'msg': 'Nome de usuário e/ou senha inválidos.'}, status=status.HTTP_401_UNAUTHORIZED)


class LogoutView(APIView):
    @swagger_auto_schema(
        responses={200: "Successfully Logged out"},
        operation_description="Logout",
        tags=['user'],
    )
    @permission_classes([IsAuthenticated])
    def post(self, request):
        logout(request)
        return Response({'msg': 'Logout feito com sucesso.'}, status=status.HTTP_200_OK)


class ChangePasswordView(APIView):
    @swagger_auto_schema(
        request_body=PasswordChangeSerializer(),
        responses={200: "Password successfully changed"},
        operation_description="Changes password",
        tags=['user'],
    )
    @permission_classes([IsAuthenticated])
    def put(self, request):
        serializer = PasswordChangeSerializer(
            context={'request': request}, data=request.data)
        serializer.is_valid(raise_exception=True)
        request.user.set_password(serializer.validated_data['new_password'])
        request.user.save()
        return Response({'msg': 'Senha modificada com sucesso.'}, status=status.HTTP_200_OK)


class DeactivateUserView(APIView):
    @swagger_auto_schema(
        responses={200: "Successfully deactivated user account"},
        operation_description="Deactivate user account",
        tags=['user'],
    )
    @permission_classes([IsAuthenticated])
    def patch(self, request):
        user = request.user
        user.is_active = False
        user.save()
        return Response({'msg': 'Conta desativada com sucesso.'}, status=status.HTTP_200_OK)


class ReactivateUserView(APIView):
    @swagger_auto_schema(
        responses={200: "Successfully reactivated user account"},
        operation_description="Reactivate user account",
        tags=['user'],
    )
    @permission_classes([IsAuthenticated])
    def patch(self, request):
        user = request.user
        user.is_active = True
        user.save()
        return Response({'msg': 'Conta reativada com sucesso.'}, status=status.HTTP_200_OK)


class GetUserView(APIView):
    @swagger_auto_schema(
        responses={200: 'Success',
                   400: 'Not Authorized'},
        operation_description="Get list of users",
        tags=['user'],
    )
    @permission_classes([IsAuthenticated])
    def get(self, request):
        if not request.user.is_authenticated:
            return Response("Usuário não autenticado.", status=status.HTTP_401_UNAUTHORIZED)
        users = User.objects.all()
        serializer = GetUserSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
