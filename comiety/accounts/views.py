from django.shortcuts import render, redirect
from django.contrib.auth.views import login as auth_login
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers
from django.contrib.auth.decorators import login_required
from django.conf import settings
from .forms import *

def login(request):
    providers = []
    for provider in get_providers():
        try:
            provider.social_app = SocialApp.objects.get(provider=provider.id, sites=settings.SITE_ID)
        except SocialApp.DoesNotExist:
            provider.social_app = None
        providers.append(provider)
    return render(request, 'accounts/login.html', {'providers': providers})


def member_regist(request):
    if request.method =="POST":
        form = UserForm(request.POST)
        if form.is_valid():
            user = form.save()
            return redirect('accounts:member_info_regist')
    elif request.method =='GET':
        form = UserForm()

    providers = []
    for provider in get_providers():
        try:
            provider.social_app = SocialApp.objects.get(provider=provider.id, sites=settings.SITE_ID)
        except SocialApp.DoesNotExist:
            provider.social_app = None
        providers.append(provider)

    return render(request, 'accounts/member_regist.html', {
        'form' : form, 'providers':providers
        })

def member_info_regist(request):
    # 회원 가입
    '''
        auth.user FORM을 따로 만들어서 연동해야하나??
        allauth로 페북 가입 후 추가 정보(Profile)만 입력 받아서 저장 혹은 업데이트 해주면되나??
        페북등으로 가입 후 우리 페이지 가입이 되었는지 어케확인하지?
        인증비트하나추가할까?
    '''
    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            member = form.save(commit = False)
            # reverse('dongzip:society_list', args=[society.id]). => "/soceity/1/""
            # resolve_url('dongzip:society_list', society.id).    => "/soceity/1/"
            # redirect('dongzip:society_list', society.id)        => HttpResponse
            return redirect('dongzip:index')
    else:
        form = ProfileForm()

    return render(request, 'accounts/member_info_regist.html', {'form':form})

@login_required
def my_profile(request):
    return render(request, 'accounts/my_profile.html')

