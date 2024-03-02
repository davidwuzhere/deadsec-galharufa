from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from galharufa.models.casting import Casting
from ..serializers.casting import CastingAuthSerializer, CastingSerializer, FotosSerializer, UpdateCastingSerializer
from drf_yasg.utils import swagger_auto_schema
from django.contrib.auth.models import User


class FotosView(APIView):
    @swagger_auto_schema(
        responses={201: FotosSerializer(many=False),
                   400: "Bad request"},
        operation_description="Upload casting images",
        tags=['casting'],
    )
    @permission_classes([IsAuthenticated])
    def post(self, request):
        if not request.user.is_authenticated:
            return Response("Usuário não autenticado.", status=status.HTTP_401_UNAUTHORIZED)
        if request.data.get("usuario") is None:
            return Response("O campo 'usuario' é obrigatório.", status=status.HTTP_400_BAD_REQUEST)
        if int(request.data.get("usuario")) != request.user.id:
            return Response("Não autorizado.", status=status.HTTP_401_UNAUTHORIZED)
        serializer = FotosSerializer(
            data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CastingsView(APIView):
    @swagger_auto_schema(
        responses={200: CastingSerializer(many=True),
                   400: "Bad request"},
        operation_description="Obtains all castings",
        tags=['casting'],
        security=[],
    )
    def get(self, request):
        castings = Casting.objects.all()
        if request.user.is_authenticated:
            serializer = CastingAuthSerializer(castings, many=True)
        else:
            serializer = CastingSerializer(castings, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=CastingAuthSerializer(),
        responses={201: CastingAuthSerializer(many=False),
                   400: "Bad request"},
        operation_description="Obtains all castings",
        tags=['casting'],
    )
    @permission_classes([IsAuthenticated])
    def post(self, request):
        if not request.user.is_authenticated:
            return Response("Usuário não autenticado.", status=status.HTTP_401_UNAUTHORIZED)
        if request.data.get("usuario") is None:
            return Response("O campo 'usuario' é obrigatório.", status=status.HTTP_400_BAD_REQUEST)
        if int(request.data.get("usuario")) != request.user.id:
            return Response("Usuário não autenticado.", status=status.HTTP_401_UNAUTHORIZED)

        if request.data.get("dados_bancarios") is not None:
            if request.data["dados_bancarios"] == {}:
                request.data.pop("dados_bancarios")

        if request.data.get("imagens") is not None:
            if request.data["imagens"] == {}:
                request.data.pop("imagens")

        if request.data.get("videos") is not None:
            if request.data["videos"] == {}:
                request.data.pop("videos")

        if request.data.get("idiomas") is not None:
            if request.data["idiomas"] == {}:
                request.data.pop("idiomas")

        if request.data.get("veiculos") is not None:
            if request.data["veiculos"] == {}:
                request.data.pop("veiculos")

        serializer = CastingAuthSerializer(
            data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CastingView(APIView):
    @swagger_auto_schema(
        responses={200: CastingAuthSerializer(many=False),
                   400: "Bad request"},
        operation_description="Obtains all castings",
        tags=['casting'],
        security=[],
    )
    @permission_classes([IsAuthenticated])
    def get(self, request, slug):
        if request.user.is_authenticated:
            try:
                casting = Casting.objects.get(slug=slug)
            except Casting.DoesNotExist:
                return Response("Não encontrado.", status=status.HTTP_404_NOT_FOUND)
            serializer = CastingAuthSerializer(casting, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            try:
                casting = Casting.objects.get(slug=slug)
            except Casting.DoesNotExist:
                return Response("Não encontrado.", status=status.HTTP_404_NOT_FOUND)
            serializer = CastingSerializer(casting, many=False)
            return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: UpdateCastingSerializer(many=False),
                   400: "Bad request"},
        operation_description="Obtains all castings",
        tags=['casting'],
    )
    @permission_classes([IsAuthenticated])
    def patch(self, request, slug):
        if not request.user.is_authenticated:
            return Response("Usuário não autenticado.", status=status.HTTP_401_UNAUTHORIZED)
        if request.data.get("usuario") is None:
            return Response("O campo 'usuario' é obrigatório.", status=status.HTTP_400_BAD_REQUEST)
        if int(request.data.get("usuario")) != request.user.id:
            return Response("Usuário não autenticado.", status=status.HTTP_401_UNAUTHORIZED)
        try:
            casting = Casting.objects.get(slug=slug)
        except Casting.DoesNotExist:
            return Response("Não encontrado.", status=status.HTTP_404_NOT_FOUND)

        request.data["slug"] = slug

        if request.data.get("dados_bancarios") is not None:
            if request.data["dados_bancarios"] == {}:
                request.data.pop("dados_bancarios")

        if request.data.get("imagens") is not None:
            if request.data["imagens"] == {}:
                request.data.pop("imagens")

        if request.data.get("videos") is not None:
            if request.data["videos"] == {}:
                request.data.pop("videos")

        if request.data.get("idiomas") is not None:
            if request.data["idiomas"] == {}:
                request.data.pop("idiomas")

        if request.data.get("veiculos") is not None:
            if request.data["veiculos"] == {}:
                request.data.pop("veiculos")

        if request.data.get("endereco") is not None:
            if request.data["endereco"] == {}:
                request.data.pop("endereco")

        serializer = CastingAuthSerializer(
            instance=casting, data=request.data, partial=True)
        if serializer.is_valid():
            update_fields = []
            for key in request.data:
                update_fields.append(key)
            serializer.save(update_fields=update_fields)
            casting = Casting.objects.get(slug=slug)
            serializer = CastingAuthSerializer(casting)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: "No content"},
        operation_description="Obtains all castings",
        tags=['casting'],
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
            casting = Casting.objects.get(slug=slug)
        except Casting.DoesNotExist:
            return Response("Não encontrado.", status=status.HTTP_404_NOT_FOUND)
        casting.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
