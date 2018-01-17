# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib.auth import logout
from django.http import HttpResponseRedirect  
import json
import random
import requests

# Create your views here.
def index(request):
    return render(request,'index.html', {'NumForShow': User.objects.count()+181500})

def login1(request):
    if not request.user.is_anonymous:
        return HttpResponseRedirect("/home/")
    return render(request,'login.html', {})


def register(request,invitorID=''):
    if not request.user.is_anonymous:
        return HttpResponseRedirect("/home/")
    return render(request,'register.html', {"invitorID":invitorID})

@login_required(login_url='/login/')
def home(request):
    if(request.user.is_anonymous):
        return HttpResponseRedirect("/index/")
    AmwayUsers=User.objects.filter(first_name=str(request.user.id))
    Amway=[]
    for man in AmwayUsers:
        cellphone=man.last_name
        if len(cellphone)==11:
            cellphone=cellphone[:3]+'****'+cellphone[7:]
        Amway.append(cellphone)

    num=len(Amway)

    return render(request,'user.html', {'username':request.user.username,'amwayid':request.user.id+5800,'amwayresult':Amway,'num':num})#用户id加5800为推广ID


def findpsd(request):
    if not request.user.is_anonymous:
        return HttpResponseRedirect("/home/")
    return render(request,'forgetpwd.html', {})

def learn(request):
    return render(request,'1min2ews.html', {})

#random SMS
def godsays(phone):
    x=int(phone) % 958
    b1=round(100000/x+1)
    b2=round(1000000/x+1)
    y=random.randint(b1,b2)*x
    return str(y).zfill(6)
def godjudges(phone,sms):
    x=int(phone) % 958
    a=int(sms)
    if a % x:
        return False
    else:
        return True



def SentSMS(request):
    phone = request.POST['phone']
    dic={}

    
    if phone.isdigit() and len(phone)==11:
        code=godsays(phone)
        smstext='您的验证码为'+code+'，请在5分钟内完成注册。【以太战舰】'
        resp = requests.post("http://sms-api.luosimao.com/v1/send.json",
            auth=("api", "key-442199e5d02324bc7d1ff2a2f675882e"),
            data={
            "mobile": phone,
            "message": smstext
            },timeout=3 , verify=False)
        result =  json.loads( resp.content )
        dic['msg'] = 'ok'
        dic['success'] = True
        jstr = result
        return HttpResponse(jstr, content_type='application/json')
    dic['msg'] = '手机号无效'
    dic['success'] = False
    jstr = json.dumps(dic)
    return HttpResponse(jstr, content_type='application/json')


def CheckName(request):
    username = request.POST['Username']
    dic={}
    dic['valid'] = False
    try:
        User.objects.get(username=username)
    except:
        dic['valid'] = True
    	
    jstr = json.dumps(dic)
    return HttpResponse(jstr, content_type='application/json')

def CheckPhone(request):
    username = request.POST['phone']
    dic={}
    dic['valid'] = False
    try:
        User.objects.get(last_name=phone)
    except:
        dic['valid'] = True
    	
    jstr = json.dumps(dic)
    return HttpResponse(jstr, content_type='application/json')


def test(request):
    dic={}
    uid=request.user.id
    dic['msg']=uid
    jstr = json.dumps(dic)
    return HttpResponse(jstr, content_type='application/json')



def CheckEmail(request):
    email = request.POST['email']
    dic={}
    dic['valid'] = False
    try:
        User.objects.get(email=email)
    except:
        dic['valid'] = True
    	
    jstr = json.dumps(dic)
    return HttpResponse(jstr, content_type='application/json')

def LogMeIn(request):
    username = request.POST['UserName']
    password = request.POST['Password']
    user = authenticate(request, username=username,password=password)
    dic={}
    
    
    if user is not None:
        login(request, user)
        dic['success'] = True
        dic['msg'] = user.id

    else:
    	dic['success'] = False
    	dic['msg'] = 'failed'

    jstr = json.dumps(dic)
    return HttpResponse(jstr, content_type='application/json')

def SignMeUp(request):
    username = request.POST['Username']
    password = request.POST['Password']
    email = request.POST['email']
    phone =	request.POST['phone']
    AmwayID =	request.POST['AmwayID']
    sms =   request.POST['sms']
    dic={}
    if not godjudges(phone,sms):
        dic['success'] = False
        dic['msg'] = '短信验证码错误'
        jstr = json.dumps(dic)
        return HttpResponse(jstr, content_type='application/json')

    user = User.objects.create_user(username,email,password)
    
    dic={}
    if user is not None:
        if int(AmwayID)>5799:
            user.first_name = AmwayID
        user.last_name = phone
        user.save()
        dic['success'] = True
        dic['msg'] = '注册成功'

    else:
        dic['success'] = False
        dic['msg'] = '未知错误'

    jstr = json.dumps(dic)
    return HttpResponse(jstr, content_type='application/json')



@login_required(login_url='/login/')
def logout_view(request):
    logout(request)
    # Redirect to a success page.
    return HttpResponseRedirect("/index/")