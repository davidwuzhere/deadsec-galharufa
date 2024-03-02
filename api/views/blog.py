from rest_framework import status
from rest_framework.decorators import permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from galharufa.models.blog import BlogPost
from ..serializers.blog import BlogPostSerializer
from drf_yasg.utils import swagger_auto_schema


class BlogPostsView(APIView):
    @swagger_auto_schema(
        responses={200: BlogPostSerializer(many=True),
                   400: "Bad request"},
        operation_description="Obtains all castings",
        tags=['blog'],
        security=[],
    )
    def get(self, request):
        blogposts = BlogPost.objects.all()
        serializer = BlogPostSerializer(blogposts, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        request_body=BlogPostSerializer(),
        responses={201: BlogPostSerializer(many=False),
                   400: "Bad request"},
        operation_description="Create blog post",
        tags=['blog'],
    )
    @permission_classes([IsAuthenticated])
    def post(self, request):
        if not request.user.is_authenticated:
            return Response("Usuário não autenticado.", status=status.HTTP_401_UNAUTHORIZED)
        if request.data.get("usuario") is None:
            return Response("O campo 'usuario' é obrigatório.", status=status.HTTP_400_BAD_REQUEST)
        if int(request.data.get("usuario")) != request.user.id:
            return Response("Não autorizado.", status=status.HTTP_401_UNAUTHORIZED)
        serializer = BlogPostSerializer(
            data=request.data, many=False)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class BlogPostView(APIView):
    @swagger_auto_schema(
        responses={200: BlogPostSerializer(many=False),
                   400: "Bad request"},
        operation_description="Retrieve blog post",
        tags=['blog'],
        security=[],
    )
    def get(self, request, slug):
        try:
            blog_post = BlogPost.objects.get(slug=slug)
        except BlogPost.DoesNotExist:
            return Response("Não encontrado.", status=status.HTTP_404_NOT_FOUND)
        serializer = BlogPostSerializer(blog_post)
        return Response(serializer.data, status=status.HTTP_200_OK)

    @swagger_auto_schema(
        responses={200: BlogPostSerializer(many=False),
                   400: "Bad request"},
        operation_description="Update blog post",
        tags=['blog'],
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
            blog_post = BlogPost.objects.get(slug=slug)
        except BlogPost.DoesNotExist:
            return Response("Não encontrado.", status=status.HTTP_404_NOT_FOUND)
        serializer = BlogPostSerializer(
            instance=blog_post, data=request.data, partial=True)
        if serializer.is_valid():
            update_fields = []
            for key in request.data:
                update_fields.append(key)
            serializer.save(update_fields=update_fields)
            blog_post = BlogPost.objects.get(slug=slug)
            serializer = BlogPostSerializer(blog_post)
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @swagger_auto_schema(
        responses={204: "No content"},
        operation_description="Delete blog plost",
        tags=['blog'],
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
            blog_post = BlogPost.objects.get(slug=slug)
        except BlogPost.DoesNotExist:
            return Response("Não encontrado.", status=status.HTTP_404_NOT_FOUND)
        blog_post.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
