from rest_framework import serializers
from galharufa.models.blog import BlogPost


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = BlogPost
        fields = ['titulo', 'texto',
                  'newsletter', 'created', 'updated', 'slug', 'usuario']
