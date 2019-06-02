from django.contrib import admin
from torch import models

# Register your models here.
admin.site.register(models.Permission)
admin.site.register(models.UserPermission)
