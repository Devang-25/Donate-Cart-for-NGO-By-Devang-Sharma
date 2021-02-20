from django import template
from accounts.models import Ngo

register=template.Library()

@register.filter(name='register_or_profile')
def tell(request):
    myngo=Ngo.objects.all().filter(founder=request.user)
    return myngo
