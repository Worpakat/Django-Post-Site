# Register your models here.

from django.contrib import admin
from .models import ImgPost, Comment

#source link: https://docs.djangoproject.com/en/4.1/ref/contrib/admin/

admin.site.register([ImgPost, Comment])