from datetime import datetime
from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator, RegexValidator, FileExtensionValidator, validate_image_file_extension, BaseValidator
from django.utils.text import slugify
from django.core.exceptions import ValidationError
from django.contrib.postgres.fields import ArrayField
from ..helpers.cnpj import format_cnpj
from ..helpers.cpf import format_cpf
import datetime
import uuid


class MaxSizeValidator(BaseValidator):
    def __init__(self, max_size):
        self.max_size = max_size

    def __call__(self, file):
        if file.size > self.max_size:
            raise ValidationError(
                f'A imagem não pode exceder {self.max_size / 1024 / 1024} MB.')


class Endereco(models.Model):
    ESTADO = (
        ('AC', 'Acre - AC'),
        ('AL', 'Alagoas - AL'),
        ('AP', 'Amapá - AP'),
        ('AM', 'Amazonas - AM'),
        ('BA', 'Bahia - BA'),
        ('CE', 'Ceará - CE'),
        ('DF', 'Distrito Federal - DF'),
        ('ES', 'Espírito Santo - ES'),
        ('GO', 'Goiás - GO'),
        ('MA', 'Maranhão - MA'),
        ('MT', 'Mato Grosso - MT'),
        ('MS', 'Mato Grosso do Sul - MS'),
        ('MG', 'Minas Gerais - MG'),
        ('PA', 'Pará - PA'),
        ('PB', 'Paraíba - PB'),
        ('PR', 'Paraná - PR'),
        ('PE', 'Pernambuco - PE'),
        ('PI', 'Piauí - PI'),
        ('RJ', 'Rio de Janeiro - RJ'),
        ('RN', 'Rio Grande do Norte - RN'),
        ('RS', 'Rio Grande do Sul - RS'),
        ('RO', 'Rondônia - RO'),
        ('RR', 'Roraima - RR'),
        ('SC', 'Santa Catarina - SC'),
        ('SP', 'São Paulo - SP'),
        ('SE', 'Sergipe - SE'),
        ('TO', 'Tocantins - TO'),
    )

    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    CEP = models.CharField(validators=[RegexValidator(
        regex='^.{8}$', message='O CEP necessita ter 8 caracteres!', code='nomatch')], max_length=8)
    estado = models.CharField(
        max_length=19, choices=ESTADO, null=True, blank=True)
    cidade = models.CharField(max_length=100, null=True, blank=True)
    bairro = models.CharField(max_length=100, null=True, blank=True)
    logradouro = models.CharField(max_length=100, null=True, blank=True)
    numero = models.PositiveIntegerField(null=True, blank=True)
    complemento = models.CharField(max_length=100, null=True, blank=True)

    def __str__(self):
        return f"{self.CEP}"

    class Meta:
        verbose_name_plural = "Endereços"


class Idiomas(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    ingles = models.BooleanField(default=False)
    portugues = models.BooleanField(default=False)
    espanhol = models.BooleanField(default=False)
    frances = models.BooleanField(default=False)
    italiano = models.BooleanField(default=False)
    alemao = models.BooleanField(default=False)
    mandarim = models.BooleanField(default=False)
    japones = models.BooleanField(default=False)
    russo = models.BooleanField(default=False)
    italiano = models.BooleanField(default=False)
    arabe = models.BooleanField(default=False)
    hungaro = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Idiomas"


class Veiculos(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    carro = models.BooleanField(default=False)
    moto = models.BooleanField(default=False)
    trator = models.BooleanField(default=False)
    jetski = models.BooleanField(default=False)
    helicoptero = models.BooleanField(default=False)
    aviao = models.BooleanField(default=False)
    barco = models.BooleanField(default=False)

    class Meta:
        verbose_name_plural = "Veículos"


class DadosBancarios(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    banco = models.CharField(max_length=100)
    agencia = models.PositiveIntegerField()
    conta = models.PositiveIntegerField()
    digito = models.PositiveIntegerField()
    pix_telefone = models.CharField(validators=[RegexValidator(
        regex='^\(?(?:[14689][1-9]|2[12478]|3[1234578]|5[1345]|7[134579])\)? ?(?:[2-8]|9[1-9])[0-9]{3}\-?[0-9]{4}$', message='Por favor, insira um número válido.', code='nomatch')], max_length=11, blank=True, null=True)
    pix_CPF = models.CharField(validators=[RegexValidator(
        regex='^.{11}$', message='O CPF necessita ter 11 caracteres!', code='nomatch')], max_length=11, blank=True, null=True)
    pix_email = models.EmailField(blank=True, null=True)

    def __str__(self):
        return f"{self.banco}, {self.agencia} - {self.conta}"

    class Meta:
        verbose_name_plural = "Dados Bancários"


class Fotos(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE)
    foto1 = models.ImageField(
        upload_to=f'static/images/foto1/', null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg']), validate_image_file_extension, MaxSizeValidator(4 * 1024 * 1024)])
    foto2 = models.ImageField(
        upload_to=f'static/images/foto2/', null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg']), validate_image_file_extension, MaxSizeValidator(4 * 1024 * 1024)])
    foto3 = models.ImageField(
        upload_to=f'static/images/foto3/', null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg']), validate_image_file_extension, MaxSizeValidator(4 * 1024 * 1024)])
    foto4 = models.ImageField(
        upload_to=f'static/images/foto4/', null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg']), validate_image_file_extension, MaxSizeValidator(4 * 1024 * 1024)])
    foto5 = models.ImageField(
        upload_to=f'static/images/foto5/', null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg']), validate_image_file_extension, MaxSizeValidator(4 * 1024 * 1024)])
    foto6 = models.ImageField(
        upload_to=f'static/images/foto6/', null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg']), validate_image_file_extension, MaxSizeValidator(4 * 1024 * 1024)])
    foto7 = models.ImageField(
        upload_to=f'static/images/foto7/', null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg']), validate_image_file_extension, MaxSizeValidator(4 * 1024 * 1024)])
    foto8 = models.ImageField(
        upload_to=f'static/images/foto8/', null=True, blank=True, validators=[FileExtensionValidator(['png', 'jpg', 'jpeg']), validate_image_file_extension, MaxSizeValidator(4 * 1024 * 1024)])

    class Meta:
        verbose_name_plural = "Fotos"


class Imagens(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    imagem1 = models.URLField(null=True, blank=True)
    imagem2 = models.URLField(null=True, blank=True)
    imagem3 = models.URLField(null=True, blank=True)
    imagem4 = models.URLField(null=True, blank=True)
    imagem5 = models.URLField(null=True, blank=True)
    imagem6 = models.URLField(null=True, blank=True)
    imagem7 = models.URLField(null=True, blank=True)
    imagem8 = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Imagens"


class Videos(models.Model):
    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    video1 = models.URLField(null=True, blank=True)
    video2 = models.URLField(null=True, blank=True)
    video3 = models.URLField(null=True, blank=True)
    video4 = models.URLField(null=True, blank=True)
    video5 = models.URLField(null=True, blank=True)
    video6 = models.URLField(null=True, blank=True)

    class Meta:
        verbose_name_plural = "Vídeos"


class Casting(models.Model):
    GENERO = (
        ('masculino', 'Masculino'),
        ('feminino', 'Feminino'),
        ('nao_binario', 'Não-binário')
    )
    TIPO = (
        ('ator_exclusivo', 'Ator exclusivo'),
        ('ator_nao_exclusivo', 'Ator não-exclusivo'),
        ('influencer', 'Influencer'),
        ('talento', 'Talento'),
        ('infantil', 'Infantil'),
        ('criativo', 'Criativo'),
    )

    id = models.UUIDField(default=uuid.uuid4, unique=True,
                          primary_key=True, editable=False)
    created = models.DateTimeField(auto_now_add=True, editable=False)
    updated = models.DateTimeField(auto_now=True, editable=False)
    is_active = models.BooleanField(default=True)
    usuario = models.ForeignKey(
        User, on_delete=models.CASCADE)
    slug = models.SlugField(default="", db_index=True,
                            editable=False, unique=True)
    tipo = models.CharField(max_length=18, choices=TIPO)
    genero = models.CharField(max_length=11, choices=GENERO)
    nome_completo = models.CharField(max_length=200)
    nome_artistico = models.CharField(max_length=200)
    ano = models.PositiveIntegerField(validators=[MinValueValidator(
        1900), MaxValueValidator(datetime.date.today().year)])
    DRT = models.CharField(blank=True, max_length=8, validators=[RegexValidator(
        regex='[0-9]{5}[\/]?[A-Za-z]{2}', message='O DRT necessita ter 8 caracteres!', code='nomatch')])
    altura = models.FloatField(null=True, blank=True)
    manequim = models.FloatField(null=True, blank=True)
    sapato = models.FloatField(null=True, blank=True)
    CNH = models.CharField(max_length=11, null=True, blank=True)
    veiculos = models.OneToOneField(
        Veiculos, on_delete=models.CASCADE, null=True, blank=True)
    imagens = models.OneToOneField(
        Imagens, on_delete=models.CASCADE, null=True, blank=True)
    videos = models.OneToOneField(
        Videos, on_delete=models.CASCADE, null=True, blank=True)
    peso = models.FloatField(null=True, blank=True)
    endereco = models.OneToOneField(
        Endereco, on_delete=models.CASCADE, null=True)
    RG = models.CharField(max_length=14, null=True, blank=True)
    CPF = models.CharField(validators=[RegexValidator(
        regex='([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})', message='Por favor, insira um CPF válido.', code='nomatch')], max_length=14)
    CNPJ = models.CharField(validators=[RegexValidator(
        regex='([0-9]{2}[\.]?[0-9]{3}[\.]?[0-9]{3}[\/]?[0-9]{4}[-]?[0-9]{2})|([0-9]{3}[\.]?[0-9]{3}[\.]?[0-9]{3}[-]?[0-9]{2})', message='Por favor, insira um CNPJ válido', code='nomatch')], max_length=18, null=True, blank=True)
    razao_social = models.CharField(max_length=200, null=True, blank=True)
    experiencia = models.TextField(null=True, blank=True)
    terno = models.PositiveIntegerField(null=True, blank=True)
    camisa = models.PositiveIntegerField(null=True, blank=True)
    data_nascimento = models.DateField()
    habilidades = ArrayField(models.CharField(
        max_length=200, null=True, blank=True), default=list)
    dados_bancarios = models.OneToOneField(
        DadosBancarios, on_delete=models.CASCADE, null=True, blank=True)
    idiomas = models.OneToOneField(
        Idiomas, on_delete=models.CASCADE, null=True, blank=True)
    telefone = models.CharField(validators=[RegexValidator(
        regex='^\(?(?:[14689][1-9]|2[12478]|3[1234578]|5[1345]|7[134579])\)? ?(?:[2-8]|9[1-9])[0-9]{3}\-?[0-9]{4}$', message='Por favor, insira um número válido.', code='nomatch')], max_length=11)
    email = models.EmailField()
    link_imdb = models.URLField(null=True, blank=True)
    link_instagram = models.URLField(null=True, blank=True)
    nacionalidade = models.CharField(max_length=200, null=True)
    etnia = models.CharField(max_length=200, null=True)

    def save(self, *args, **kwargs):
        self.CPF = format_cpf(self.CPF)
        self.CNPJ = format_cnpj(self.CNPJ)
        if self.slug is None or self.slug == "":
            self.slug = slugify(self.nome_artistico)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.nome_completo} ({self.tipo})"
