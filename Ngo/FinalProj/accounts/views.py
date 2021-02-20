from django.conf import settings
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy
from . import forms
from django.shortcuts import get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Ngo, NgoRequirementDetail
from django.contrib import messages
from .models import Donator, DonationDetail
from .forms import NgoRegisterForm, DonationConfirmForm
from django.views.decorators.csrf import csrf_exempt


def signup_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('accounts:accountcreate')
            # user should be logged in
    else:
        form = UserCreationForm()
    return render(request, 'accounts/signup.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # login the user
            user = form.get_user()
            login(request, user)
            if 'next' in request.POST:
                return redirect(request.POST.get('next'))
            else:
                return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'accounts/login.html', {'form': form})


def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('home')


def ngo_register(request):
    form = NgoRegisterForm()
    if request.method == 'POST':
        form = NgoRegisterForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.founder = request.user
            instance.save()
            return redirect('home')
    return render(request, 'accounts/ngoregister.html', {'form': form})


def accountcreate(request):
    return render(request, 'accounts/accountcreated.html')


def donator_view(request):
    if request.method == 'POST':
        form = forms.DonatorForm(request.POST)
        if form.is_valid():
            don = form.save()
            phone = don.phone
            return redirect('accounts:don_confirm', phone=phone)
    else:
        form = forms.DonatorForm()
    return render(request, 'accounts/donator.html', {'form': form})


@login_required(login_url='accounts:login')
def ngodetail(request):
    ngo = get_object_or_404(Ngo, founder=request.user)
    return render(request, 'accounts/ngodetail.html', {'ngo': ngo})


def donation_confirm(request, phone):
    if request.method == 'POST':
        form = DonationConfirmForm(request.POST)
        if form.is_valid():
            ins = form.save(commit=False)
            myngo = ins.ngo
            val = myngo.ngorequirementdetail_set.all().filter(req=ins.req)
            if not val:
                messages.info(request, "Selected ngo does'nt need this requirement.")
                return redirect('accounts:don_confirm', phone=phone)
            else:
                req = myngo.ngorequirementdetail_set.get(req=ins.req)
                if req.quantity == 0:
                    messages.info(request, "Selected ngo does'nt need this requirement.")
                    return redirect('accounts:don_confirm', phone=phone)
                elif req.quantity < ins.quantity:
                    messages.info(request, f'{ins.ngo} needs only {req.quantity} quantity of {ins.req}')
                    return redirect('accounts:don_confirm', phone=phone)
                else:
                    req.quantity -= ins.quantity
                    req.save()
                    dins = Donator.objects.get(phone=phone)
                    ins.donator = dins
                    ins.save()
                    return redirect('home')
    else:
        form = DonationConfirmForm()
    return render(request, 'accounts/donate_confirm.html', {'phone': phone, 'form': form})


@login_required(login_url='/accounts/login/')
def edit_view_add(request):
    if request.method == 'POST':
        form = forms.AddRequirement(request.POST)
        if form.is_valid():
            # save article to db form.save()
            instance = form.save(commit=False)
            myngo = Ngo.objects.get(founder=request.user)
            val = myngo.ngorequirementdetail_set.all().filter(req=instance.req)
            if val:
                ins = NgoRequirementDetail.objects.get(ngo=myngo, req=instance.req)
                ins.quantity = instance.quantity
                ins.save()
            else:
                instance.ngo = myngo
                instance.save()

            return redirect('home')
    else:
        form = forms.AddRequirement()
    return render(request, 'accounts/add_requirement.html', {'form': form})


@login_required(login_url='/accounts/login/')
def delete_view(request):
    if request.method == 'POST':
        req = request.POST.get('req')
        myngo = Ngo.objects.get(founder=request.user)
        val = myngo.ngorequirementdetail_set.all().filter(req=req)
        if not val:
            messages.success(request, f'You Entered the Requirement which is NOT present in your NGO, Try Again!')
            return redirect('accounts:delete_view')
        else:
            ins = NgoRequirementDetail.objects.get(ngo=myngo, req=req)
            ins.quantity = 0
            ins.save()
            return redirect('accounts:ngodetail')
    else:
        return render(request, 'accounts/delete.html')


@login_required(login_url='/accounts/login/')
def edit_view(request):
    if request.method == 'POST':
        requirement = request.POST.get('requirement')
        quantity = request.POST.get('quantity')
        myngo = Ngo.objects.get(founder=request.user)
        val = myngo.ngorequirementdetail_set.all().filter(req=requirement)
        if not val:
            messages.success(request, f'You Entered the Requirement which is NOT present in your NGO, Try Again!')
            return redirect('accounts:edit_view')
        else:
            ins = NgoRequirementDetail.objects.get(ngo=myngo, req=requirement)
            ins.quantity = quantity
            ins.save()
            return redirect('accounts:ngodetail')
    else:
        return render(request, 'accounts/edit.html')


@login_required(login_url='/accounts/login/')
def donators(request):
    dds = DonationDetail.objects.all()
    myngo = Ngo.objects.get(founder=request.user)
    return render(request, 'accounts/donators.html', {'dds': dds, 'myngo': myngo})


class MyPasswordChangeView(PasswordChangeView):
    template_name = 'accounts/resetp.html'
    success_url = reverse_lazy('home')


def d_signup(request):
    if request.method == 'POST':
        phone = request.POST.get('phone')
        val = False
        for don in Donator.objects.all():
            if don.phone == phone:
                val = True
                break
        if val:
            return redirect('accounts:don_confirm', phone=phone)
        else:
            return redirect('accounts:donator')
    else:
        return render(request, 'accounts/d_signup.html')


@csrf_exempt
def contactus(request):
    if request.method == 'POST':
        email = request.POST.get('Email')
        subject = request.POST.get('Subject')
        message = request.POST.get('Message')
        send_mail(
            subject,
            message,
            settings.EMAIL_HOST_USER,
            [email]
        )
        return render(request, 'home.html')
    return redirect('home')
