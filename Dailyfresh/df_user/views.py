# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponseRedirect
from django.http import HttpResponse
from models import *
from hashlib import sha1
# from django.http import JsonResponse
from .islogin import islogin

# Create your views here.
def register(request):
    return render(request, 'df_user/register.html')


# 登入处理
def register_handle(requst):
    response = HttpResponse()
    # 接收用户输入
    post = requst.POST
    uname = post.get('user_name')
    upwd = post.get('pwd')
    ucpwd = post.get('cpwd')
    uemail = post.get('email')

    if upwd != ucpwd:
        return redirect('/user/register/')
    s1 = sha1()
    s1.update(upwd)
    upwd3 = s1.hexdigest()

    user = UserInfo()
    user.uname = uname
    user.upwd = upwd3
    user.uemail = uemail
    user.save()

    return redirect('/user/login/')

# 判断用户是否已经存在
def register_exist(requset):
    uname = requset.GET.get('uname')
    count = UserInfo.objects.filter(uname=uname).count()
    return JsonResponse({'count': count})


# 登录界面
def login(request):
    uname = request.COOKIES.get('uname', '')
    context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 0, 'uname': uname}
    return render(request, 'df_user/login.html', context)

# 登录处理
def login_handle(request):
    # 接收请求信息
    get = request.POST
    uname = get.get('username')
    upwd = get.get('pwd')
    jizhu = get.get('jizhu', 0)
    # 根据用户名查询对象
    users = UserInfo.objects.filter(uname=uname)
    # print uname
    # 判断如果未查到则用户名错，查到再判断密码是否正确，正确则转到用户中心
    if len(users) == 1:
        s1 = sha1()
        s1.update(upwd)
        #登录带cookie值   必须 red = HttpResponseRedirect    red.set_cookie  renturn red
        if s1.hexdigest() == users[0].upwd:
            red = HttpResponse('登录成功')

            # print '*'*10
            # print count
            # 记住用户名
            if jizhu != 0:
                red.set_cookie('uname', uname)
            else:
                red.set_cookie('uname', '', max_age=-1)
            request.session['user_id'] = users[0].id
            request.session['user_name'] = uname
            return red
        else:
            context = {'title': '用户登录', 'error_name': 0, 'error_pwd': 1, 'uname': uname}
            return render(request, 'df_user/login.html', context)
    else:
        context = {'title': '用户登录', 'error_name': 1, 'error_pwd': 0, 'uname': uname }
        return render(request, 'df_user/login.html', context)

