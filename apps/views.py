from django.shortcuts import render, redirect
import json, bcrypt, jwt, re
from django.http import JsonResponse, HttpResponse
from .models import User

from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.core.mail import EmailMessage
from .tokens import account_activation_token
from django.utils.encoding import force_bytes
from django.utils.encoding import force_str
from .text import message
from django.views import View
from django.core.exceptions import ValidationError


import environ
env = environ.Env()
environ.Env.read_env()

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


def logout(request):
    if request.session.get('user'):
        del(request.session['user'])

    return redirect('/')

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
    if request.method == 'POST':
        name = request.POST['name']
        email = request.POST['email']
        password = request.POST['password']
        password_check = request.POST['password_check']

        if User.objects.filter(email=email).exists():
            # return JsonResponse({'message': 'ALREADY_EXISTS'}, status=400)
            return HttpResponse("<script>alert('이미 존재하는 이메일입니다.\\n회원 가입 페이지로 돌아갑니다.');"
                                "location.href='/signup';</script>")

        regex_email = '^[a-zA-Z0-9+-_.]+@[a-zA-Z0-9_-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(regex_email, email):
            # return JsonResponse({'message': 'INVALID_EMAIL'}, status=400)
            return HttpResponse("<script>alert('이메일 형식에 일치하지 않습니다.\\n회원 가입 페이지로 돌아갑니다.');"
                                "location.href='/signup';</script>")

        if password != password_check:
            # return JsonResponse({'message': '비밀번호 불일치!'}, status=400)
            return HttpResponse("<script>alert('비밀번호 불일치!\\n회원 가입 페이지로 돌아갑니다.');"
                                "location.href='/signup';</script>")

        password_encode = password.encode('utf-8')
        password_crypt = bcrypt.hashpw(password_encode, bcrypt.gensalt()).decode('utf-8')

        user = User.objects.create(name=name, email=email, password=password_crypt)
        # return JsonResponse({'message': 'SUCCESS!'}, status=201)

        # 이메일 인증
        current_site = get_current_site(request)
        domain = current_site.domain
        uidb64 = urlsafe_base64_encode(force_bytes(user.pk))
        token = account_activation_token.make_token(user)
        message_data = message(domain, uidb64, token)

        mail_title = "[DataPlanet] 회원가입 이메일 인증을 완료해주세요."
        mail = EmailMessage(mail_title, message_data, to=[email])
        mail.send()

        return HttpResponse("<script>alert('인증 메일이 발송되었습니다.메일을 확인해주세요.\\n메인 페이지로 돌아갑니다.');"
                            "location.href='/';</script>")

    elif request.method == 'GET':
        return render(request, 'apps/signup.html')

class activate(View):
    def get(self, request, uidb64, token):
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = User.objects.get(pk=uid)

            if account_activation_token.check_token(user, token):
                user.is_authenticated = True
                user.save()
                return redirect('/')

            return JsonResponse({"message": "AUTH FAIL"}, status=400)

        except ValidationError:
            return JsonResponse({"message": "TYPE_ERROR"}, status=400)
        except KeyError:
            return JsonResponse({"message": "INVALID_KEY"}, status=400)