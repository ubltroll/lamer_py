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
import requests,datetime

from milicien.models import assistance,Profile
# Create your views here.
def index(request):
    return render(request,'index.html', {'NumForShow': User.objects.count()+5800})

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
    AmwayUsers=User.objects.filter(first_name=str(request.user.id+5800))
    Amway=[]
    for man in AmwayUsers:
        cellphone=man.last_name
        if len(cellphone)==11:
            cellphone=cellphone[:3]+'****'+cellphone[7:]
        Amway.append(cellphone)

    num=len(Amway)
    strships=request.user.profile.ships
    ships=[]
    shipsnum=0
    for i in range(0,5):
        ships.append(int(strships[i]))
        shipsnum+=ships[i]
    recent=[]
    msgs=assistance.objects.filter(touser=request.user.profile.uid)
    for msg in msgs:
        if msg.fromuser==0:
            temp=((datetime.datetime.now()-msg.time.replace(tzinfo=None)).days)
            if temp:
                recent.append(str(temp)+'天: 邀请好友注册碎片+10')
            else:
                recent.append('今天: 邀请好友注册碎片+10')
        else:
            try:
                name=User.objects.get(id=(msg.fromuser-5800)).username
            except:
                name='?'
            temp=((datetime.datetime.now()-msg.time.replace(tzinfo=None)).days)
            if temp:
                recent.append(str(temp)+'天: ID:'+str(msg.fromuser)+'<'+name+'>为您助攻，碎片+3')
            else:
                recent.append('今天: ID:'+str(msg.fromuser)+'<'+name+'>为您助攻，碎片+3')


    return render(request,'user.html', {'username':request.user.username,'amwayid':request.user.id+5800,
        'amwayresult':Amway,'num':num,'nickname':request.user.profile.nickname,'checkin':request.user.profile.checkin,'credits':request.user.profile.credits,
        'ships':ships,"shipsnum":shipsnum,'assistance':request.user.profile.assistance,'recent':recent
        })#用户id加5800为推广ID


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
    
    dic={}
    #debug mode on 
    luotest=request.POST['luotest_response']
    resp = requests.post("https://captcha.luosimao.com/api/site_verify",
            #auth=("api_key", "9667e877e20e6380832f6abd6642cfda"),
            data={
            "api_key": '9667e877e20e6380832f6abd6642cfda',
            "response": luotest
            },timeout=3 , verify=False)
    result =  json.loads( resp.content.decode('utf-8') )
    dic['msg'] = 'wrong captcha'
    dic['success'] = False
    jstr = json.dumps(result)
    if result['res']!='success':
        return HttpResponse(jstr, content_type='application/json')
    #debug mode------------------------


    phone = request.POST['phone']
    if phone.isdigit() and len(phone)==11:
        code=godsays(phone)
        smstext='您的验证码为'+code+'，请在5分钟内完成注册。【以太战舰】'
        resp = requests.post("http://sms-api.luosimao.com/v1/send.json",
            auth=("api", "key-442199e5d02324bc7d1ff2a2f675882e"),
            data={
            "mobile": phone,
            "message": smstext
            },timeout=3 , verify=False)
        #result =  json.loads( resp.content )
        dic['msg'] = 'ok'
        dic['success'] = True
        jstr = json.dumps(dic)
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
    phone = request.POST['phone']
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
    nickname = request.POST['nickname']
    dic={}

    UniquePhone=False
    try:
        User.objects.get(last_name=phone)
    except:
        UniquePhone = True


    if not UniquePhone:
        dic['success'] = False
        dic['msg'] = '手机号已经被注册'
        jstr = json.dumps(dic)
        return HttpResponse(jstr, content_type='application/json')

    if not godjudges(phone,sms):
        dic['success'] = False
        dic['msg'] = '短信验证码错误'
        jstr = json.dumps(dic)
        return HttpResponse(jstr, content_type='application/json')

    dic={}
    if AmwayID:
        try:
            frienduser=User.objects.get(id=(int(AmwayID)-5800))
            frienduser.profile.credits+=10  #邀请+10
            frienduser.profile.save()
            assistancedata=assistance.objects.create(fromuser=0,touser=frienduser.profile.uid)
            assistancedata.save()
        except:
            dic['bug']=1
            
    user = User.objects.create_user(username,email,password)  
    
    if user is not None:
        if int(AmwayID)>5799:
            user.first_name = str(int(AmwayID)-5800)
        user.last_name = phone
        #user.profile.uid = int(user.id)
        user.profile.assistance = 3
        user.profile.checkin = False
        user.profile.ships = '00000'
        user.profile.friend1=0
        user.profile.friend2=0
        user.profile.credits=0
        user.profile.nickname=nickname
        #user.profile.cooldowntime=datetime.datetime.strptime('1815-06-18 17:41:20', '%Y-%m-%d %H:%M:%S')
        
        user.save()
        dic['success'] = True
        dic['msg'] = '注册成功'
        login(request, user)

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


@login_required(login_url='/login/')   #签到获得战舰碎片并刷新邀请次数
def checkin(request):
    dic={}
    if (datetime.datetime.now() - request.user.profile.cooldowntime).days :
        dic['success'] = True
        dic['msg'] = '签到成功,战舰碎片+3'
        request.user.profile.cooldowntime=datetime.datetime.now()
        request.user.profile.credits+=3
        request.user.profile.friend1=0
        request.user.profile.friend2=0
        request.user.profile.assistance=3
        request.user.save()
    else:
        dic['success'] = False
        dic['msg'] = '冷却时间未到'

    jstr = json.dumps(dic)
    return HttpResponse(jstr, content_type='application/json')


@login_required(login_url='/login/')   #助攻他人获得战舰碎片
def assist(request):
    friend = int(request.POST['friend'])
    dic={}
    try:
        frienduser=User.objects.get(uid=friend)
    except:
        dic['success'] = False
        dic['msg'] = '错误的id'
        jstr = json.dumps(dic)
        return HttpResponse(jstr, content_type='application/json')
    if friend==request.user.profile.uid or friend==request.user.profile.friend1 or friend==request.user.profile.friend2:
        dic['success'] = False
        dic['msg'] = 'ID重复或是自己'
    else:
        dic['success'] = True
        dic['msg'] = '成功'
        if request.user.profile.assistance == 0 :
            dic['success'] = False
            dic['msg'] = '次数用尽'
        else:
            assistancedata=assistance.objects.create(fromuser=request.user.profile.uid,touser=friend)
            assistancedata.save()
            frienduser.profile.credits+=3   #一次3点
            frienduser.save()
            if request.user.profile.assistance == 3:
                request.user.profile.friend1=friend
            elif request.user.profile.assistance == 2:
                request.user.profile.friend3=friend
            request.user.profile.assistance-=1
            request.user.save()

    jstr = json.dumps(dic)
    return HttpResponse(jstr, content_type='application/json')