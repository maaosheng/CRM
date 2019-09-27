from stark.service.myadmin import site
from rbac.models import *
from stark.service.myadmin import  ModelXadmin
site.register(User)
site.register(Role)
class CustomPermission(ModelXadmin):
    list_display = ['title','url','action','permission_group']
    filter_list = ['title','permission_group']
    search_list = ['title','action']
    list_display_links = ['title']
    def update_info(self,queryset):
        pass
    def delete_info(self,queryset):
        queryset.delete()
    update_info.short_description='批量初始化'
    delete_info.short_description='批量删除'
    actions=[update_info,delete_info]



site.register(Permission,CustomPermission)
site.register(PermissionGroup)

