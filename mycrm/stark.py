from stark.service.myadmin import  site
from mycrm.models import *
from stark.service.myadmin import *
site.register(Department)
site.register(UserInfo)
site.register(Course)
site.register(School)
site.register(ClassList)


class   MyCustomer(ModelXadmin):
    list_display = ['id','qq','name']
site.register(Customer,MyCustomer)

site.register(CourseRecord)
site.register(Student)
site.register(ConsultRecord)
site.register(StudyRecord)
site.register(CustomerDistrbute)
