from django.contrib.admin import site

# Register your models here.
from mycrm.models import *
site.register(Department)
site.register(UserInfo)
site.register(Course)
site.register(School)
site.register(ClassList)
site.register(Customer)
site.register(CourseRecord)
site.register(Student)
site.register(ConsultRecord)
site.register(StudyRecord)
site.register(CustomerDistrbute)
