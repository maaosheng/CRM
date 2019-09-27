# from django import template
# register = template.Library()
from django import template
register = template.Library()
@register.inclusion_tag("template_menu.html")
def get_menu(request):
    title = request.session['user_title']
    # for foo in title:
    #     print(title[0],title[1])
    current_path = request.path_info
    return {'title':title,
            'current_path':current_path
            }


