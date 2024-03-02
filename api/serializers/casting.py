from rest_framework import serializers
from galharufa.models.casting import Casting, Videos, Imagens, Fotos, Endereco, Idiomas, DadosBancarios, Veiculos
import logging
from sys import stdout

logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler(stdout))


class VideosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Videos
        fields = '__all__'


class FotosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fotos
        fields = '__all__'


class ImagensSerializer(serializers.ModelSerializer):
    class Meta:
        model = Imagens
        fields = '__all__'


class EnderecoSerializer(serializers.ModelSerializer):
    class Meta:
        model = Endereco
        fields = '__all__'


class IdiomasSerializer(serializers.ModelSerializer):
    class Meta:
        model = Idiomas
        fields = '__all__'


class DadosBancariosSerializer(serializers.ModelSerializer):
    class Meta:
        model = DadosBancarios
        fields = '__all__'


class VeiculosSerializer(serializers.ModelSerializer):
    class Meta:
        model = Veiculos
        fields = '__all__'


class UpdateCastingSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    veiculos = VeiculosSerializer(required=False)
    idiomas = IdiomasSerializer(required=False)
    imagens = ImagensSerializer(required=False)
    videos = VideosSerializer(required=False)
    dados_bancarios = DadosBancariosSerializer(required=False)
    endereco = EnderecoSerializer(required=False)

    class Meta:
        model = Casting
        fields = ['user', 'veiculos', 'idiomas', 'imagens',
                  'videos', 'videos', 'dados_bancarios', 'endereco']
        extra_kwargs = {
            'tipo': {
                'validators': []
            },
            'genero': {
                'validators': []
            },
            'nome_completo': {
                'validators': []
            },
            'nome_artistico': {
                'validators': []
            },
            'ano': {
                'validators': []
            },
            'CPF': {
                'validators': []
            },
            'data_nascimento': {
                'validators': []
            },
            'telefone': {
                'validators': []
            },
            'email': {
                'validators': []
            },
        }

    def save(self, validated_data):
        casting = Casting.objects.get(slug=validated_data['slug']).__dict__

        if validated_data.get('veiculos') is not None:
            veiculos_data = validated_data.pop('veiculos')
            veiculos_id = casting['veiculos_id']
            veiculos = VeiculosSerializer(data=veiculos_data)
            if veiculos.is_valid():
                veiculos = Veiculos.objects.get(id=veiculos_id)
                veiculos.aviao = veiculos_data.get('aviao')
                veiculos.barco = veiculos_data.get('barco')
                veiculos.carro = veiculos_data.get('carro')
                veiculos.helicoptero = veiculos_data.get('helicoptero')
                veiculos.jetski = veiculos_data.get('jetski')
                veiculos.moto = veiculos_data.get('moto')
                veiculos.trator = veiculos_data.get('trator')

                update_fields = []
                for key in veiculos_data:
                    update_fields.append(key)
                veiculos.save(update_fields=update_fields)
            else:
                raise serializers.ValidationError(
                    {'veiculos': veiculos.errors})
        else:
            veiculos = None

        if validated_data.get('idiomas') is not None:
            idiomas_data = validated_data.pop('idiomas')
            idiomas_id = casting['idiomas_id']
            idiomas = IdiomasSerializer(data=idiomas_data)
            if idiomas.is_valid():
                idiomas = Idiomas.objects.get(id=idiomas_id)
                idiomas.alemao = idiomas_data.get('alemao')
                idiomas.arabe = idiomas_data.get('arabe')
                idiomas.espanhol = idiomas_data.get('espanhol')
                idiomas.frances = idiomas_data.get('frances')
                idiomas.hungaro = idiomas_data.get('hungaro')
                idiomas.ingles = idiomas_data.get('ingles')
                idiomas.italiano = idiomas_data.get('italiano')
                idiomas.japones = idiomas_data.get('japones')
                idiomas.mandarim = idiomas_data.get('mandarim')
                idiomas.portugues = idiomas_data.get('portugues')
                idiomas.russo = idiomas_data.get('russo')

                update_fields = []
                for key in idiomas_data:
                    update_fields.append(key)
                idiomas.save(update_fields=update_fields)
            else:
                raise serializers.ValidationError({'idiomas': idiomas.errors})
        else:
            idiomas = None

        if validated_data.get('imagens') is not None:
            imagens_data = validated_data.pop('imagens')
            imagens_id = casting['imagens_id']
            imagens = ImagensSerializer(data=imagens_data)
            if imagens.is_valid():
                imagens = Imagens.objects.get(id=imagens_id)
                imagens.imagem1 = imagens_data.get('imagem1')
                imagens.imagem2 = imagens_data.get('imagem2')
                imagens.imagem3 = imagens_data.get('imagem3')
                imagens.imagem4 = imagens_data.get('imagem4')
                imagens.imagem5 = imagens_data.get('imagem5')
                imagens.imagem6 = imagens_data.get('imagem6')
                imagens.imagem7 = imagens_data.get('imagem7')
                imagens.imagem8 = imagens_data.get('imagem8')

                update_fields = []
                for key in imagens_data:
                    update_fields.append(key)
                imagens.save(update_fields=update_fields)
            else:
                raise serializers.ValidationError({'imagens': imagens.errors})
        else:
            imagens = None

        if validated_data.get('videos') is not None:
            videos_data = validated_data.pop('videos')
            videos_id = casting['videos_id']
            videos = VideosSerializer(data=videos_data)
            if videos.is_valid():
                videos = Videos.objects.get(id=videos_id)
                videos.video1 = videos_data.get('video1')
                videos.video1 = videos_data.get('video2')
                videos.video1 = videos_data.get('video3')
                videos.video1 = videos_data.get('video4')
                videos.video1 = videos_data.get('video5')
                videos.video6 = videos_data.get('video6')

                update_fields = []
                for key in videos_data:
                    update_fields.append(key)
                videos.save(update_fields=update_fields)
            else:
                raise serializers.ValidationError({'videos': videos.errors})
        else:
            videos = None

        if validated_data.get('dados_bancarios') is not None:
            dados_bancarios_data = validated_data.pop('dados_bancarios')
            dados_bancarios_id = casting['dados_bancarios_id']
            dados_bancarios = DadosBancariosSerializer(
                data=dados_bancarios_data)
            if dados_bancarios.is_valid():
                dados_bancarios = DadosBancarios.objects.get(
                    id=dados_bancarios_id)
                dados_bancarios.agencia = dados_bancarios_data.get('agencia')
                dados_bancarios.banco = dados_bancarios_data.get('banco')
                dados_bancarios.conta = dados_bancarios_data.get('conta')
                dados_bancarios.digito = dados_bancarios_data.get('digito')
                dados_bancarios.pix_CPF = dados_bancarios_data.get('pix_CPF')
                dados_bancarios.pix_email = dados_bancarios_data.get(
                    'pix_email')
                dados_bancarios.pix_telefone = dados_bancarios_data.get(
                    'pix_telefone')

                update_fields = []
                for key in dados_bancarios_data:
                    update_fields.append(key)
                dados_bancarios.save(update_fields=update_fields)
            else:
                raise serializers.ValidationError(
                    {'dados_bancarios': dados_bancarios.errors})
        else:
            dados_bancarios = None

        if validated_data.get('endereco') is not None:
            endereco_data = validated_data.pop('endereco')
            endereco_id = casting['endereco_id']
            endereco = EnderecoSerializer(data=endereco_data)
            if endereco.is_valid():
                endereco = Endereco.objects.get(id=endereco_id)
                endereco.bairro = endereco_data.get('bairro')
                endereco.CEP = endereco_data.get('CEP')
                endereco.cidade = endereco_data.get('cidade')
                endereco.complemento = endereco_data.get('complemento')
                endereco.estado = endereco_data.get('estado')
                endereco.logradouro = endereco_data.get('logradouro')
                endereco.numero = endereco_data.get('numero')

                update_fields = []
                for key in endereco_data:
                    update_fields.append(key)
                endereco.save(update_fields=update_fields)
            else:
                raise serializers.ValidationError(
                    {'endereco': endereco.errors})
        else:
            endereco = None

        casting = Casting.objects.get(slug=validated_data['slug'])

        casting.veiculos = veiculos
        casting.idiomas = idiomas
        casting.imagens = imagens
        casting.videos = videos
        casting.dados_bancarios = dados_bancarios
        casting.endereco = endereco

        update_fields = []
        for key in validated_data:
            update_fields.append(key)

        casting.save(update_fields=validated_data)

        return casting


class CastingAuthSerializer(serializers.ModelSerializer):
    user = serializers.ReadOnlyField(source='user.username')
    veiculos = VeiculosSerializer(required=False)
    idiomas = IdiomasSerializer(required=False)
    imagens = ImagensSerializer(required=False)
    videos = VideosSerializer(required=False)
    dados_bancarios = DadosBancariosSerializer(required=False)
    endereco = EnderecoSerializer()

    class Meta:
        model = Casting
        fields = '__all__'

    def create(self, validated_data):
        if validated_data.get('veiculos') is not None:
            veiculos_data = validated_data.pop('veiculos')
            veiculos = VeiculosSerializer(data=veiculos_data)
            if veiculos.is_valid():
                veiculos = veiculos.save()
                veiculos_id = veiculos.__dict__['id']
            else:
                raise serializers.ValidationError(
                    {'veiculos': veiculos.errors})
        else:
            veiculos = None
            veiculos_id = None

        if validated_data.get('idiomas') is not None:
            idiomas_data = validated_data.pop('idiomas')
            idiomas = IdiomasSerializer(data=idiomas_data)
            if idiomas.is_valid():
                idiomas = idiomas.save()
                idiomas_id = idiomas.__dict__['id']
            else:
                raise serializers.ValidationError({'idiomas': idiomas.errors})
        else:
            idiomas = None
            idiomas_id = None

        if validated_data.get('imagens') is not None:
            imagens_data = validated_data.pop('imagens')
            imagens = ImagensSerializer(data=imagens_data)
            if imagens.is_valid():
                imagens = imagens.save()
                imagens_id = imagens.__dict__['id']
            else:
                raise serializers.ValidationError({'imagens': imagens.errors})
        else:
            imagens = None
            imagens_id = None

        if validated_data.get('videos') is not None:
            videos_data = validated_data.pop('videos')
            videos = VideosSerializer(data=videos_data)
            if videos.is_valid():
                videos = videos.save()
                videos_id = videos.__dict__['id']
            else:
                raise serializers.ValidationError({'videos': videos.errors})
        else:
            videos = None
            videos_id = None

        if validated_data.get('dados_bancarios') is not None:
            dados_bancarios_data = validated_data.pop('dados_bancarios')
            dados_bancarios = DadosBancariosSerializer(
                data=dados_bancarios_data)
            if dados_bancarios.is_valid():
                dados_bancarios = dados_bancarios.save()
                dados_bancarios_id = dados_bancarios.__dict__['id']
            else:
                raise serializers.ValidationError(
                    {'dados_bancarios': dados_bancarios.errors})
        else:
            dados_bancarios = None
            dados_bancarios_id = None

        if validated_data.get('endereco') is not None:
            endereco_data = validated_data.pop('endereco')
            endereco = EnderecoSerializer(data=endereco_data)
            if endereco.is_valid():
                endereco = endereco.save()
                endereco_id = endereco.__dict__['id']
            else:
                raise serializers.ValidationError(
                    {'endereco': endereco.errors})
        else:
            endereco = None
            endereco_id = endereco_id

        casting = Casting.objects.create(veiculos_id=veiculos_id, idiomas_id=idiomas_id, imagens_id=imagens_id,
                                         videos_id=videos_id, dados_bancarios_id=dados_bancarios_id, endereco_id=endereco_id,
                                         **validated_data)

        return casting

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        representation['veiculos'] = VeiculosSerializer(instance.veiculos).data
        representation['idiomas'] = IdiomasSerializer(instance.idiomas).data
        representation['imagens'] = ImagensSerializer(instance.imagens).data
        representation['videos'] = VideosSerializer(instance.videos).data
        representation['dados_bancarios'] = DadosBancariosSerializer(
            instance.dados_bancarios).data
        representation['endereco'] = EnderecoSerializer(instance.endereco).data

        return representation

    def to_internal_value(self, data):
        for nested_field in ['veiculos', 'idiomas', 'imagens', 'videos', 'dados_bancarios', 'endereco']:
            nested_data = data.get(nested_field)
            if nested_data is not None:
                if self.instance is not None:
                    nested_instance = getattr(self.instance, nested_field)
                    for field, value in nested_data.items():
                        setattr(nested_instance, field, value)
                    nested_instance.save()
                    # assign the dictionary data
                    data[nested_field] = nested_data
        return super().to_internal_value(data)

    def update(self, instance, validated_data):
        # handle non-related fields as before
        for attr, value in validated_data.items():
            if attr not in {'veiculos', 'idiomas', 'imagens', 'videos', 'dados_bancarios', 'endereco'}:
                setattr(instance, attr, value)

        # handle related fields
        for nested_field in {'veiculos', 'idiomas', 'imagens', 'videos', 'dados_bancarios', 'endereco'}:
            nested_data = validated_data.pop(nested_field, None)
            if nested_data is not None:
                nested_instance = getattr(instance, nested_field)
                nested_serializer = self.fields[nested_field]
                nested_serializer.update(nested_instance, nested_data)

        instance.save()
        return instance


class CastingSerializer(serializers.ModelSerializer):
    veiculos = VeiculosSerializer()
    idiomas = IdiomasSerializer()
    imagens = ImagensSerializer()
    videos = VideosSerializer()

    class Meta:
        model = Casting
        fields = ['nome_completo', 'is_active', 'slug', 'nome_artistico', 'tipo', 'genero', 'ano', 'DRT', 'altura',
                  'manequim', 'sapato', 'veiculos', 'peso', 'experiencia', 'terno', 'camisa', 'data_nascimento',
                  'habilidades', 'idiomas', 'telefone', 'email', 'link_imdb', 'link_instagram', 'imagens',
                  'videos', 'nacionalidade', 'etnia']
