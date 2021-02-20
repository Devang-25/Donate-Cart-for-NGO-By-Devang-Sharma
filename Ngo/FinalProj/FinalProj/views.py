from django.core.mail import send_mail
from django.http import HttpResponse
from accounts.models import Ngo, DonationDetail
from django.shortcuts import render, redirect
from django.template.loader import render_to_string
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings


def home(request):
    ngos = Ngo.objects.all()
    count = 0
    for dd in DonationDetail.objects.all():
        count += dd.quantity
    dic = {}
    for dd in DonationDetail.objects.all():
        val = dic.get(dd.donator, -1)
        if val == -1:
            dic[dd.donator] = [dd.donator.first_name, dd.donator.last_name, dd.quantity]
        else:
            dic[dd.donator][2] = val[2] + dd.quantity

    array = list(dic.values())
    array.sort(reverse=True, key=lambda item: item[2])
    best_users = array[0:min(len(array), 5)]
    val=Ngo.objects.filter().first()
    return render(request, 'home.html', {'ngos': ngos, 'count': count, 'best_users': best_users,'val':val})

