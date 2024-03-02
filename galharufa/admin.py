from django.contrib import admin
from .models.casting import Endereco, Idiomas, Veiculos, DadosBancarios, Imagens, Videos, Casting
from .models.blog import BlogPost
from .models.service import Servico

# Register your models here.

admin.site.register(Endereco)
admin.site.register(Idiomas)
admin.site.register(Veiculos)
admin.site.register(DadosBancarios)
admin.site.register(Imagens)
admin.site.register(Videos)
admin.site.register(Casting)
admin.site.register(BlogPost)
admin.site.register(Servico)
