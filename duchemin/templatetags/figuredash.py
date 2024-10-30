from django.template.defaultfilters import register

@register.filter(name='figuredash')
def figuredash(string):
    return str(string).replace("-", "\u2013")
