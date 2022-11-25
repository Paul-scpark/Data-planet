from pathlib import Path
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse

import os, bcrypt, json, jwt
from .models import User

# Create your views here.
def main(request):
    return render(
        request,
        'apps/main.html'
    )

def overview(request):
    return render(
        request,
        'apps/overview.html'
    )

def overview_platform(request):
    return render(
        request,
        'apps/overview_platform.html'
    )

def overview_eda(request):
    return render(
        request,
        'apps/overview_eda.html'
    )

def login(request):
    if request.method == "GET":
        return render(request, 'apps/login.html')
    
    elif request.method == "POST":
        inputId = request.POST['email']
        inputPassword = request.POST['password']
        
        ### 1. 사용자의 ID (이메일)이 DB 상에서 존재하는지 여부 확인
        if User.objects.filter(email=inputId).exists():
            getUser = User.objects.get(email=inputId)
            ### 2. ID가 존재한다면, 입력 받은 password와 일치 여부 확인
            ## 사용자의 user_id 값으로 JWT 발급
            if bcrypt.checkpw(inputPassword.encode('utf-8'), getUser.password.encode('utf-8')):
                payload = {'id': getUser.user_id}
                access_token = jwt.encode(payload, 'secret', 'HS256')
                print(access_token)
                
                return HttpResponse(
                    "<script>alert('로그인에 성공하셨습니다.');"
                    "location.href='/';</script>"
                )

            else: 
                return HttpResponse(
                    "<script>alert('아이디 또는 비밀번호가 일치하지 않습니다.');"
                    "location.href='/login';</script>"
                )

# def logout(request):
#     if request.session.get('user'):
#         del(request.session['user'])
    
#     return redirect('/')

def search_category(request):
    return render(
        request,
        'apps/search_category.html'
    )

def search_detail(request):
    return render(
        request,
        'apps/search_detail.html'
    )

def profile(request):
    return render(
        request,
        'apps/profile.html'
    )

def community(request):
    return render(
        request,
        'apps/community.html'
    )

def community_create(request):
    return render(
        request,
        'apps/community_create.html'
    )

def support(request):
    return render(
        request,
        'apps/support.html'
    )

def signup(request):
    if request.method == "GET":
        return render(request, 'apps/signup.html')
    
    elif request.method == "POST":
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        re_password = request.POST['rePassword']
        
        ### 1. 회원가입 과정에서 이상 여부 확인
        ## 이메일 중복 확인
        if User.objects.filter(email=email).exists():
            return HttpResponse(
                "<script>alert('이미 존재하는 이메일입니다.\\n회원 가입 페이지로 돌아갑니다.');"
                "location.href='/signup';</script>"
            )
        
        ## 패스워드 일치 여부 확인
        if password != re_password:
            return HttpResponse(
                "<script>alert('비밀번호 불일치!\\n회원 가입 페이지로 돌아갑니다.');"
                "location.href='/signup';</script>"
            )
        
        ## 패스워드 길이 확인
        if len(password) < 8:
            return HttpResponse(
                "<script>alert('비밀번호는 8자리 이상으로 입력해주세요!!\\n회원 가입 페이지로 돌아갑니다.');"
                "location.href='/signup';</script>"
            )
        
        ### 2. 패스워드 해쉬 처리
        password = password.encode('utf8')
        password_bcrypt = bcrypt.hashpw(password, bcrypt.gensalt()).decode('utf8')
        
        ### 3. 위 로직에서 특이사항 없었으면, DB에 데이터 적재
        User.objects.create(name=name, email=email, password=password_bcrypt).save()
        return HttpResponse(
            "<script>alert('회원가입 완료.\\n메인 페이지로 돌아갑니다.');"
            "location.href='/';</script>"
        )