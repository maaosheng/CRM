
def initial_permission(user,request):
    # permissions_list = []
    # for i in user.roles.all().values('permissions__url','permissions__action','permissions__permission_group__id').distinct():
    #     permissions_list.append(i['permissions__url'])
    # print(permissions_list)
    # request.session['permissions_list'] = permissions_list
    # request.session['user_id'] = user.pk
    # return permissions_list


    permisssion_dic = {}
    permission_title=[]
    ret = user.roles.all().values('permissions__url','permissions__action','permissions__permission_group__id').distinct()
    res = user.roles.all().values('permissions__title','permissions__action','permissions__url').distinct()
    print(res)
    for  field in ret:
        gid = field['permissions__permission_group__id']
        if not gid in permisssion_dic:
            permisssion_dic[gid] ={
                'url':[field['permissions__url'],],
                'action':[field['permissions__action'],]
            }
        else:
            permisssion_dic[gid]['url'].append(field['permissions__url'])
            permisssion_dic[gid]['action'].append(field['permissions__action'])
    #构建菜单
    for info in res:
        if info['permissions__action']=='list':
            permission_title.append((info['permissions__url'],info['permissions__title']))
    request.session['permissions_list'] = permisssion_dic
    request.session['user_id'] = user.pk
    request.session['user_title'] =permission_title
    return permisssion_dic
