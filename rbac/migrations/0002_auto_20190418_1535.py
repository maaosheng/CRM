# Generated by Django 2.1.5 on 2019-04-18 07:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('rbac', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='PermissionGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tiele', models.CharField(max_length=25)),
            ],
        ),
        migrations.AlterModelOptions(
            name='permission',
            options={'verbose_name': '权限', 'verbose_name_plural': '权限'},
        ),
        migrations.AlterModelOptions(
            name='role',
            options={'verbose_name': '角色', 'verbose_name_plural': '角色'},
        ),
        migrations.AlterModelOptions(
            name='user',
            options={'verbose_name': '用户', 'verbose_name_plural': '用户'},
        ),
        migrations.AddField(
            model_name='permission',
            name='action',
            field=models.CharField(default='', max_length=36),
        ),
        migrations.AddField(
            model_name='permission',
            name='permission_group',
            field=models.ForeignKey(default='1', on_delete=django.db.models.deletion.CASCADE, to='rbac.PermissionGroup'),
        ),
    ]
