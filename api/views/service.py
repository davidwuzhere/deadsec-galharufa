from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from galharufa.models.service import Servico
from ..serializers.service import ServicoSerializer
from drf_yasg.utils import swagger_auto_schema


class ServicosView(APIView):
    @swagger_auto_schema(
        responses={200: ServicoSerializer(many=True),
                   400: "Bad request"},
        operation_description="Obtains all castings",
        tags=['service'],
        security=[],
    )
    def get(self, request):
        servicos = Servico.objects.all()
        serializer = ServicoSerializer(servicos, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=ServicoSerializer(),
        responses={201: ServicoSerializer(many=False),
                   400: "Bad request"},
        operation_description="Creates service",
        tags=['service'],
    )
    @permission_classes([IsAuthenticated])
    def post(self, request):
        if not request.user.is_authenticated:
            return Response("Usuário não autenticado.", status=status.HTTP_401_UNAUTHORIZED)
        if request.data.get("usuario") is None:
            return Response("O campo 'usuario' é obrigatório.", status=status.HTTP_400_BAD_REQUEST)
        if int(request.data.get("usuario")) != request.user.id:
            return Response("Não autorizado.", status=status.HTTP_401_UNAUTHORIZED)
        serializer = ServicoSerializer(
            data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ServicoView(APIView):
    @swagger_auto_schema(
        responses={200: ServicoSerializer(),
                   400: "Bad request"},
        operation_description="Retrieve service",
        tags=['service'],
        security=[],
    )
    def get(self, request, slug):
        try:
            servico = Servico.objects.get(slug=slug)
        except Servico.DoesNotExist:
            return Response("Serviço não encontrado.", status=status.HTTP_404_NOT_FOUND)
        serializer = ServicoSerializer(servico)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: ServicoSerializer(many=False),
                   400: "Bad request"},
        operation_description="Update service",
        tags=['service'],
    )
    @permission_classes([IsAuthenticated])
    def patch(self, request, slug):
        if not request.user.is_authenticated:
            return Response("Usuário não autenticado.", status=status.HTTP_401_UNAUTHORIZED)
        if request.data.get("usuario") is None:
            return Response("O campo 'usuario' é obrigatório.", status=status.HTTP_400_BAD_REQUEST)
        if int(request.data.get("usuario")) != request.user.id:
            return Response("Não autorizado.", status=status.HTTP_401_UNAUTHORIZED)
        try:
            servico = Servico.objects.get(slug=slug)
        except Servico.DoesNotExist:
            return Response("Serviço não encontrado.", status=status.HTTP_404_NOT_FOUND)
        serializer = ServicoSerializer(
            instance=servico, data=request.data, partial=True)
        if serializer.is_valid():
            update_fields = []
            for key in request.data:
                update_fields.append(key)
            serializer.save(update_fields=update_fields)
            servico = Servico.objects.get(slug=slug)
            serializer = ServicoSerializer(servico)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: "No content"},
        operation_description="Delete service",
        tags=['service'],
    )
    @permission_classes([IsAuthenticated])
    def delete(self, request, slug):
        if not request.user.is_authenticated:
            return Response("Usuário não autenticado.", status=status.HTTP_401_UNAUTHORIZED)
        if request.data.get("usuario") is None:
            return Response("O campo 'usuario' é obrigatório.", status=status.HTTP_400_BAD_REQUEST)
        if int(request.data.get("usuario")) != request.user.id:
            return Response("Não autorizado.", status=status.HTTP_401_UNAUTHORIZED)
        try:
            servico = Servico.objects.get(slug=slug)
        except Servico.DoesNotExist:
            return Response("Serviço não encontrado.", status=status.HTTP_404_NOT_FOUND)
        servico.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
