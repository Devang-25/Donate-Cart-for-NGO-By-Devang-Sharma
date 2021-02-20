from django import forms
from .models import Ngo, NgoRequirementDetail, Donator, DonationDetail


class NgoRegisterForm(forms.ModelForm):
    class Meta:
        model = Ngo
        fields = ['name', 'email', 'phone']


class AddRequirement(forms.ModelForm):
    class Meta:
        model = NgoRequirementDetail
        fields = ['req', 'quantity']


class DonatorForm(forms.ModelForm):
    class Meta:
        model = Donator
        fields = ['first_name', 'last_name', 'phone']


class DonationConfirmForm(forms.ModelForm):
    class Meta:
        model = DonationDetail
        fields = ['ngo', 'req', 'quantity']
