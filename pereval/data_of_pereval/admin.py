from django.contrib import admin

from .models import *

admin.site.register(UserModel)
admin.site.register(PerevalCoordinate)
admin.site.register(PerevalModel)
admin.site.register(ImageModel)