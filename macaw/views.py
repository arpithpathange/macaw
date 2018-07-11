from django.http import HttpResponse
from macaw import models
from django.shortcuts import render
from qrtools import QR
import os
import Cookie
import datetime
import time


def qr(request):
    campaign = request.GET.get('campaign') #Campaign name
    adSet = request.GET.get('adSet') #adset name
    ad = request.GET.get('ad') #ad creative
    adv = request.GET.get('adv') #adv name

    cookie = checkcookie(request) #check  cookie
    if(cookie == None):
        max_age = 1 * 60
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                                             "%a, %d-%b-%Y %H:%M:%S GMT")
        image_data = generateimg(campaign, adSet, ad, adv)
        response = HttpResponse(image_data, content_type="image/png")
        response.set_cookie('macaw', 'Arpith', max_age=max_age, expires=expires)
        return response


    return HttpResponse("Code generated very recently, Try after some time")



def mxcnt(request):
    campaign = request.GET.get('campaign')  # Campaign name
    adSet = request.GET.get('adSet')  # adset name
    ad = request.GET.get('ad')  # ad creative
    adv = request.GET.get('adv')  # adv name
    m2 = request.GET.get('m2')
    m3 = request.GET.get('m3')
    mxcnt = models.savemxevents()
    mxcnt.campaign= campaign
    mxcnt.adset =adSet
    mxcnt.ad =ad
    mxcnt.adv =adv
    mxcnt.time = time.time()
    mxcnt.m2 = m2
    mxcnt.m3 = m3
    mxcnt.save()

    return HttpResponse("m2 Saved")



def registration(request):
    login = request.GET.get('login')
    passwd = request.GET.get('passwd')
    phone = request.GET.get('phone')
    email = request.GET.get('email')
    adv = request.GET.get('adv')

    registration = models.registration()
    registration.login = login
    registration.passwd = passwd
    registration.adv =adv
    registration.email =email
    registration.phone =phone
    registration.save()

    return  HttpResponse("Registration done")


def checkcookie(request):
    if 'macaw' in request.COOKIES:
        value = request.COOKIES['macaw']
        return value


def generateimg(campaign,adSet,ad,adv):
    my_QR = QR(data=u'campaign=' + campaign + ' adSet=' + adSet + ' ad=' + ad +' adv='+adv, pixel_size=20)
    my_QR.encode()
    print my_QR.filename
    image_data = open(my_QR.filename, mode='r').read()
    return image_data