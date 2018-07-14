from django.http import HttpResponse
from macaw import models
from django.shortcuts import render, render_to_response
from django.template import RequestContext
from qrtools import QR
import os
import Cookie
import datetime
import time
from PIL import Image, ImageDraw, ImageFont


#def qr(request, template_name="index.html"):
def qr(request):
    campaign = request.GET.get('campaign') #Campaign name
    adSet = request.GET.get('adSet') #adset name
    ad = request.GET.get('ad') #ad creative
    adv = request.GET.get('adv') #adv name
    #ll = request.GET.get('ll')qr code generator using python with some extra data
    name = request.GET.get('name')
    address = request.GET.get('address')

    cookie = checkcookie(request) #check  cookie
    if(cookie == None):
        max_age = 1 * 60
        expires = datetime.datetime.strftime(datetime.datetime.utcnow() + datetime.timedelta(seconds=max_age),
                                             "%a, %d-%b-%Y %H:%M:%S GMT")
        image_file = generateimg(campaign, adSet, ad, adv, name, address)
        response_image = open(image_file,"rb").read()
        response = HttpResponse(response_image, content_type="image/png")
        response.set_cookie('macaw', 'Arpith', max_age=max_age, expires=expires)
        return response
        #return render_to_response(template_name, locals(), RequestContext(request))

    return HttpResponse("Code generated very recently, Try after some time")


def mxcnt(request):
    campaign = request.GET.get('campaign')  # Campaign name
    adSet = request.GET.get('adSet')  # adset name
    ad = request.GET.get('ad')  # ad creative
    adv = request.GET.get('adv')  # adv name
    m2 = request.GET.get('m2')
    m3 = request.GET.get('m3')
    uuid = request.GET.get('uuid')
    mxcnt = models.savemxevents()
    mxcnt.campaign= campaign
    mxcnt.adset =adSet
    mxcnt.ad =ad
    mxcnt.adv =adv
    mxcnt.time = time.time()
    mxcnt.m2 = m2
    mxcnt.m3 = m3
    mxcnt.uuid = uuid
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


def generateimg(campaign,adSet,ad,adv,name , address):
    import uuid
    from django.conf import settings
    address_img_path = generateaddressimage(name, address)
    unique = format(str(uuid.uuid4().hex))
    print "unique "+unique
    name = "/static/images/"+unique+".png"
    filename = os.path.join(settings.BASE_DIR, 'macaw{0}'.format(name))
    print "file "+filename
    my_QR = QR(data=u'campaign=' + campaign + ' adSet=' + adSet + ' ad=' + ad +' adv='+adv +' uuid='+unique, pixel_size=20, filename=filename)
    my_QR.encode()
    image_data = open(my_QR.filename, mode='r').read()
    os.rename(my_QR.filename, filename)
    final_display_img = mergeImages(name,address_img_path)
    os.remove("macaw/"+name)
    os.remove(address_img_path)
    return final_display_img

def mergeImages(qrimg, addressimg):
    import sys
    from django.conf import settings
    from PIL import Image
    import uuid
    os.chdir(settings.BASE_DIR)
    images = map(Image.open, ['macaw/'+qrimg, addressimg])
    widths, heights = zip(*(i.size for i in images))
    total_width = sum(widths)
    max_height = max(heights)
    new_im = Image.new('RGB', (total_width, max_height))

    x_offset = 0
    for im in images:
        new_im.paste(im, (x_offset,0))
        x_offset += im.size[0]
    final_display_img = "macaw/static/images/final.png"
    new_im.save(final_display_img)
    return  final_display_img


def generateaddressimage(name, address):
    from PIL import Image, ImageDraw, ImageFont
    img = Image.new('RGB', (900, 900), color=(255, 255, 255))
    fnt = ImageFont.truetype('/Library/Fonts/Arial.ttf', 55)
    fnt1 = ImageFont.truetype('/Library/Fonts/Arial.ttf', 35)
    fnt2 = ImageFont.truetype('/Library/Fonts/Arial.ttf', 20)


    d = ImageDraw.Draw(img)
    data = address.split(",")
    d.text((10, 80), "Name :"+name, font=fnt, fill=(0, 0, 0))
    i = 240
    d.text((10, 160), "Address :" , font=fnt, fill=(0, 0, 0))
    for temp in data:
        d.text((160, i), " "+temp, font=fnt1, fill=(0, 0, 0))
        i= i+80
    d.text((10,i+80),"**Download this QRCode and present it at the shop to avail the offer**", font=fnt2, fill=(0, 0, 0))

    address_img_path = os.path.join("macaw/static/temp/address.png")
    img.save(address_img_path)
    return address_img_path


