from django.utils.deprecation import MiddlewareMixin
from django.shortcuts import HttpResponse, redirect
import re
class ValidPermission(MiddlewareMixin):
    # -----------设置白名单---------------
    def process_request(self, request):
        valid_url_list = ['/login/', '/reg/', '/admin.*', ]
        current_path = request.path_info  # 当前访问的页面(页面url)
        # print(current_path)

        for valid in valid_url_list:
            ret = re.match(valid, current_path)
            # print('====>>',ret)
            if ret:
                return None
        # 访问查看用户时需权限

        user_id = request.session.get('user_id')
        if not user_id:
            return redirect('/login/')

        # 设置权限
        #方式一：
        # flag = False
        # permissions_list = request.session.get('permissions_list', [])
        # for field in permissions_list:
        #     new_field = '^%s$' % field
        #     ret = re.match(new_field, current_path)
        #     if ret:
        #         flag = True
        #         break
        # if not flag:
        #     return HttpResponse('无权访问！！！')
        #
        # return None

        #方拾二：
        flag = False
        permissions_list = request.session.get('permissions_list', [])
        print(permissions_list)
        for field in permissions_list.values():
            urls = field['url']
            for info in urls:
                new_info = '^%s$' % info
                ret = re.match(new_info, current_path)
                if  ret:
                    request.action= field['action']
                    return None
        return HttpResponse('无权访问！！！')



