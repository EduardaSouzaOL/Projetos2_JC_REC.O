from django.contrib import admin

# Register your models here.
from .models import Usuario, Noticia

admin.site.register(Usuario)

admin.site.register(Noticia)
