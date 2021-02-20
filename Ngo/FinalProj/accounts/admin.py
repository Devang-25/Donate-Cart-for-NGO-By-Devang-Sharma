from django.contrib import admin
from .models import Ngo,NgoRequirementDetail,Donator,DonationDetail
# Register your models here.

admin.site.register(Ngo)
admin.site.register(NgoRequirementDetail)
admin.site.register(Donator)
admin.site.register(DonationDetail)