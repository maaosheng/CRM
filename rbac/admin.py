from django.contrib.admin import site
# from rbac import models
# # Register your models here.
#
# admin.site.register(models.User)
#
#
# admin.site.register(models.Role)
# class  Role_Permission(admin.ModelAdmin):
#     list_display = ['title','url','permission_group','action']
# admin.site.register(models.Permission,Role_Permission)
# admin.site.register(models.PermissionGroup)

from rbac.models import *
# from stark.service.myadmin import  ModelXadmin
site.register(User)
site.register(Role)
# class CustomPermission(ModelXadmin):
    # list_display = ['title','url','action','permission_group']
site.register(Permission)
site.register(PermissionGroup)
