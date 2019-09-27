from django.shortcuts import render,HttpResponse,redirect
from rest_framework.views import APIView
from rbac.models import *
from rbac.services.permission_check import initial_permission
import time
import datetime
# Create your views here.

# class Login(APIView):
#     def get(self,request):
#         return render(request,'login.html',locals())
#     def post(self,request):
#         user = request.POST.get('user')
#         pawd = request.POST.get('pawd')
#         user_obj = User.objects.filter(name=user,pwd=pawd)
#         if user_obj:
#             request.session['user_id'] = user_obj.pk
#             request.session['permissions_list'] = initial_permission(user_obj,request)
#             return HttpResponse('登陆成功')

def login(request):
    if request.method=='POST':
        user = request.POST.get('user')
        pawd = request.POST.get('pawd')
        user_obj = User.objects.filter(name=user,pwd=pawd).first()
        date = datetime.date.today()
        print(date)
        if user_obj:
            ret = initial_permission(user_obj,request)
            return render(request,'muban.html',locals())
    return render(request,'login.html',locals())

# def nase(request):
#     if request.method=='GET':
#         return render()