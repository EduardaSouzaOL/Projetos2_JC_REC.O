from django.contrib import admin

# Register your models here.
from .models import Noticia,Feedback

admin.site.register(Noticia)

admin.site.register(Feedback)
