from django.db import models
"""
一个人可以有多个角色，
一个角色可以是多个人，
一个角色可以有多个权限,
一个权限可赋予多个人,
一个权限就是一个url
"""
# Create your models here.
#----------people表-----------
class User(models.Model):
    name=models.CharField(max_length=32)
    pwd=models.CharField(max_length=32)
    roles=models.ManyToManyField(to="Role")
    def __str__(self):
        return self.name

    class Meta:
        verbose_name='用户'
        verbose_name_plural = verbose_name




#------------角色表-----------
class Role(models.Model):
    title=models.CharField(max_length=32)
    permissions=models.ManyToManyField(to="Permission")



    def __str__(self): return self.title
    class Meta:
        verbose_name='角色'
        verbose_name_plural = verbose_name


#-------------权限表-------------
class Permission(models.Model):
    title=models.CharField(max_length=32,verbose_name='权限')
    url=models.CharField(max_length=128,verbose_name='地址')
    action = models.CharField(max_length=36, default="")
    permission_group = models.ForeignKey(to='PermissionGroup',on_delete=models.CASCADE,default='1')
    def __str__(self):return self.action
    class Meta:
        verbose_name='权限'
        verbose_name_plural = verbose_name


class PermissionGroup(models.Model):
    title = models.CharField(max_length=25)

    def __str__(self): return self.title
    class Meta:
        verbose_name='权限组'
        verbose_name_plural = verbose_name
