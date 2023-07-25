from django.shortcuts import render, redirect
from account.models import Account
from argon2 import PasswordHasher, exceptions
import qrcode
import time
import os
from io import BytesIO
from django.http import HttpResponse
from .models import QRData

# Create your views here.

def mainpage(request):
    if request.method == 'GET':
        context = {}

        login_session = request.session.get('login_session','')

        if login_session == '':
            context['login_session'] = False
            return render(request, 'home/index.html')
        context['login_session'] = True
        user = Account.objects.get(user_id=login_session)
        context['userid'] = user.user_id
        context['username'] = user.user_name
        context['usernumber'] = user.user_number

        return redirect('/home/success')

    elif request.method =='POST':
        requestType = request.POST.get('request-type', '')
        
        if requestType == 'register':
            user_id = request.POST.get('userid', '')
            user_pw = PasswordHasher().hash(request.POST.get('userpw', ''))
            user_name = request.POST.get('username', '')
            user_number = request.POST.get('usernumber', '')

            if user_id == '' or user_pw == '' or user_name == '' or user_number == '':
                return redirect('/home')
            else:
                newAccount = Account(
                    user_id=user_id,
                    user_pw=user_pw,
                    user_name=user_name,
                    user_number=user_number
                )
                newAccount.save()
            return redirect('/home')
        elif requestType == 'login':
            context = dict()
            user_id = request.POST.get('userid', '')
            user_pw = request.POST.get('userpw', '')

            if user_id == '':
                context['error'] = "아이디가 비어있습니다."
                return render(request, 'home/index.html', context)
            elif user_pw == '':
                context['error'] = "비밀번호가 비어있습니다."
                return render(request, 'home/index.html', context)
            else:
                try:
                    user = Account.objects.get(user_id=user_id)
                except Account.DoesNotExist:
                    context['error'] = "입력한 아이디가 잘못되었습니다."
                    return render(request, 'home/index.html', context)
                
                try:
                    PasswordHasher().verify(user.user_pw, user_pw)
                except exceptions.VerifyMismatchError:
                    context['error']= "입력한 비밀번호가 잘못되었습니다."
                    return render(request, 'home/index.html', context)
                
                request.session['login_session']= user.user_id
                return redirect('/home/success')

def login(request):
    context = {}

    login_session = request.session.get('login_session','')

    if login_session == '':
        context['login_session'] = False
        return redirect('/home')
    
    context['login_session'] = True
    user = Account.objects.get(user_id=login_session)
    context['userid'] = user.user_id
    context['username'] = user.user_name
    context['usernumber'] = user.user_number

    qrlink = generate_qr(user.user_id)
    context['qrlink'] = qrlink

    return render(request, 'home/success.html', context)

def logout(request):
    request.session.flush()
    return redirect('/home')


def generate_qr(user_id):
    tt = time.time()
    FilePath = "C:\\Users\\hongik\\project\\example\\static\\" + user_id + ".png"

    # QR 코드 생성
    qr = qrcode.QRCode(version=1, box_size=10, border=5)
    odata1 = int(str(user_id)[2:6])
    odata2 = int(str(tt)[7:10])
    cdata1 = (odata1**931)%3233
    cdata2 = (odata2**931)%3233

    qr.add_data(cdata1)
    qr.add_data(' ')
    qr.add_data(cdata2)
    qr.make(fit=True)
    QRimage = qr.make_image(fill_color="black", back_color="white")
    QRimage.save(FilePath)

    return "/static/" + user_id + ".png"
        