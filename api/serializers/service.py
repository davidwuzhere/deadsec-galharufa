from rest_framework import serializers
from galharufa.models.service import Servico


class ServicoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Servico
        fields = ['slug', 'titulo',
                  'descricao', 'duracao', 'preco', 'usuario']
