from django.conf.urls import url
from django.shortcuts import HttpResponse,render,redirect
from django.utils.safestring import mark_safe
from django.urls import reverse
from django.forms import ModelForm
from stark.util.mymodel import  Page
import copy
from django.db.models import Q
class  ValidPermission:
    def __init__(self,action):
        self.action = action

    def list(self):
        return 'list' in self.action
    def add(self):
        return 'add' in self.action

    def edit(self):
        return 'add' in self.action
    def delete(self):
        return 'delete' in self.action

class ShowList(object):
    def __init__(self,config,data,request):
        self.config = config
        self.obj_list = data
        self.request = request
        count = data.count()#def __init__(self, current_page, params,per_page, count, show_page,url=None):
        current_page = request.GET.get('page',1)
        params = request.GET
        url = self.config.get_list_url()
        self.page = Page(current_page,params,10,count,3,url=url)
        self.start = self.page.start()
        self.last = self.page.last()
        self.new_obj = data[self.start:self.last]


    def get_header(self):
        header_list = []

        for field in self.config.new_list_display():

            if not callable(field):
                if field == '__str__':
                    val = self.config.model._meta.model_name.upper()
                else:
                    try:
                        val = self.config.model._meta.get_field(field).verbose_name#获取字段的名字 verbose_name
                    except:
                        val = self.config.model._meta.model_name.upper()
            else:
                val = mark_safe(field(self, header=True))
            header_list.append(val)
        return header_list

    def get_body(self):
        body_list = []
        for obj in self.new_obj:
            temp = []
            for field in self.config.new_list_display():
                if isinstance(field, str):
                    if field in self.config.list_display_links:
                        _url = self.config.get_change_url(obj)
                        val = mark_safe('<a href=%s>%s</a>' % (_url, getattr(obj, field)))
                    else:
                        val = getattr(obj, field)
                else:
                    val = mark_safe(field(self.config, obj))
                temp.append(val)
            body_list.append(temp)
        return body_list

    def get_action(self):
        temp = []
        for item in self.config.actions:
            temp.append(
                {
                    'value':item.__name__,
                    'name':item.short_description
                }
            )
        return temp

    def get_filter(self):
        from django.db.models.fields.related import ForeignKey
        from django.db.models.fields.related import ManyToManyField
        params = self.request.GET
        show_temp = {}
        for filter_field in self.config.filter_list:
            temp = []
            params = copy.deepcopy(self.request.GET)
            cid = self.request.GET.get(filter_field,0)
            filter_obj = self.config.model._meta.get_field(filter_field)

            if cid:
                del params[filter_field]
                _url = params.urlencode()
                val = '<a href="?%s">ALL</a>'%(_url)
            else:
                val = '<a href="#"  class="active">ALL</a>'
            temp.append(mark_safe(val))
            if isinstance(filter_obj,ForeignKey) or isinstance(filter_obj,ManyToManyField):
                field_data = filter_obj.remote_field.model.objects.all()
            else:
                field_data = self.config.model.objects.values('pk',filter_field)
            for field in  field_data:
                if isinstance(filter_obj, ForeignKey) or isinstance(filter_obj, ManyToManyField):
                    params[filter_field] = field.pk
                    pk = field.pk
                    text = field.title
                else:
                    params[filter_field] = field.get(filter_field)
                    pk = field.get('pk')
                    text =  field.get(filter_field)
                _url = params.urlencode()
                if cid == str(pk) or cid==text:
                        val = '<a href="?%s" class="active">%s</a>'%(_url,text)
                else:
                        val = '<a href="?%s" >%s</a>' % (_url,text)
                temp.append(mark_safe(val))
                show_temp[filter_field] = temp
        return show_temp

class  ModelXadmin(object):
    list_display=["__str__"]
    list_display_links = []
    MyModelform = None
    search_list = []
    actions = []
    filter_list = []
    def __init__(self,model,site):
        self.model = model
        self.config =site




#获取各个ulr
    def get_add_url(self):
        model_name = self.model._meta.model_name
        app_name = self.model._meta.app_label
        _url = reverse('%s_%s_add'%(app_name,model_name))
        return _url

    def get_list_url(self):
        model_name = self.model._meta.model_name
        app_name = self.model._meta.app_label
        _url = reverse('%s_%s_list' % (app_name, model_name))
        return _url

    def get_change_url(self,obj):
        model_name = self.model._meta.model_name
        app_name = self.model._meta.app_label
        _url = reverse('%s_%s_change' % (app_name, model_name),args=(obj.pk,))
        return _url

    def get_delete_url(self,obj):
        model_name = self.model._meta.model_name
        app_name = self.model._meta.app_label
        _url = reverse('%s_%s_delete' % (app_name, model_name),args=(obj.pk,))
        return _url



#页面添加增加删除
    def checkbox(self,obj = None,header=False):
        if header:
            return "<input type='checkbox' class='header_check'>"
        return "<input type='checkbox' class='check' name='filter_check' value=%s>"%obj.pk

    def edit(self,obj = None,header=False):
        if header:
            return "操作"
        _url = self.get_change_url(obj)
        return "<a href=%s>编辑</a>"%_url

    def delete(self,obj = None,header=False):
        if header:
            return "操作"
        _url = self.get_delete_url(obj)
        return '<a href=%s>删除</a>'%_url

#获取新的display
    def new_list_display(self):
        temp = []
        temp.append(ModelXadmin.checkbox)
        temp.extend(self.list_display)
        if not self.list_display_links:
            temp.append(ModelXadmin.edit)
        temp.append(ModelXadmin.delete)
        return temp

 # 获取Model
    def get_modelform(self):
        if not self.MyModelform:
            class MyModels(ModelForm):
                class Meta:
                    model = self.model
                    fields = '__all__'
            MyModel = MyModels
        else:
            MyModel = self.MyModelform
        return MyModel

#添加页面
    def add_view(self,request):
        modelforms= self.get_modelform()
        if request.method=='POST':
            rels = request.GET.get('rel_name',0)
            form = modelforms(request.POST)
            if form.is_valid():
                obj = form.save()
                _url = self.get_list_url()
                if rels:
                    pk = obj.pk
                    text = str(obj)
                    rel = rels
                    return render(request, 'pop.html', locals())
                else:
                    return redirect(_url)
        else:
            form = modelforms()
        from django.forms.models import ModelChoiceField
        from django.forms.models import ModelMultipleChoiceField
        for belid in form:
            if isinstance(belid.field,ModelChoiceField):
                belid.opt = True
                connect_queryset = belid.field.queryset.model#查找属于哪个类
                connect_queryset_name = connect_queryset._meta.model_name#类名的str

                connect_queryset_app = connect_queryset._meta.app_label#所属app
                _url = reverse('%s_%s_add'%(connect_queryset_app,connect_queryset_name))
                belid.url = _url+'?rel_name=id_%s'%belid.name#url
        add_url = self.get_add_url()

        # 获取是那张表格
        model_name = self.model._meta.model_name
        return render(request,'add.html',locals())






#删除页面
    def delete_view(self,request, id):
        self.model.objects.filter(pk=id).delete()
        _url = self.get_list_url()
        return redirect(_url)

#编辑页面

    def change_view(self,request,id):
        obj = self.model.objects.filter(pk=id).first()
        modelforms = self.get_modelform()
        if request.method == 'POST':
            forms = modelforms(request.POST,instance=obj)

            if forms.is_valid():
                obj = forms.save()
                _url = self.get_list_url()
                return redirect(_url)
        else:
            forms = modelforms(instance=obj)
        change_url = self.get_change_url(obj)

        # 获取是那张表格
        model_name = self.model._meta.model_name
        return render(request,'change_view.html',locals())


    def get_search_list(self,request):
        ret = request.GET.get('select','')
        self.ret = ret
        from django.db.models import Q
        q = Q()
        q.connector="OR"
        for item in self.search_list:
            q.children.append((item+"__contains",ret))
        return q

    def get_filter_list(self,request):
        filter_data = request.GET
        print(filter_data)
        filters = Q()
        filters.connector='AND'
        for filter,index in filter_data.items():
            if  filter in self.filter_list:
                filters.children.append((filter,index))
        return filters



    # 展示页面
    def list_view(self,request):
        list_url = self.get_list_url()
        if request.method=='POST':
            actions = request.POST.get('selects')
            filter_check = request.POST.getlist('filter_check')
            if filter_check:
                queryset = self.model.objects.filter(pk__in=filter_check)
                ret = getattr(self,actions)(queryset)
                return redirect(list_url)



        select_list = self.get_search_list(request)

        filter_list = self.get_filter_list(request)

        obj_list = self.model.objects.all().filter(select_list).filter(filter_list)

        showlist = ShowList(self,obj_list,request)

        add_url = self.get_add_url()
        #获取是那张表格
        model_name =self.model._meta.model_name

        per = ValidPermission(request.action)

        return render(request,'list_view.html',locals())



    def get_url2s(self):

        model_name = self.model._meta.model_name
        app_name = self.model._meta.app_label
        temp = []
        temp.append(url(r'^(\d+)/change$', self.change_view,name='%s_%s_change'%(app_name,model_name)))
        temp.append(url(r'^delete/(\d+)$', self.delete_view,name='%s_%s_delete'%(app_name,model_name)))
        temp.append(url(r'^add/$', self.add_view,name='%s_%s_add'%(app_name,model_name)))
        temp.append(url(r'^$', self.list_view,name='%s_%s_list'%(app_name,model_name)))
        return temp


    @property
    def url2(self):
        return self.get_url2s(), None, None

class MyadminSite(object):
    def __init__(self, name='admin'):
        self._registry = {}

    def get_urls(self):
        temp = []
        for current_model, current_obj in site._registry.items():
            model = current_model._meta.model_name
            app = current_model._meta.app_label
            v = url(r'^%s/%s/' % (app, model), current_obj.url2)
            temp.append(v)
        return temp

    @property
    def urls(self):
        return self.get_urls(), None, None

    def register(self, model, admin_class=None, **options):
        if not admin_class:
            admin_class = ModelXadmin

        self._registry[model] = admin_class(model, self)  # {Book:ModelAdmin(Book),Publish:ModelAdmin(Publish)}

site = MyadminSite()