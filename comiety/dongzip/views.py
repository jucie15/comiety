from django.shortcuts import render
from django.http import HttpResponse
from .models import School, Society, Profile, Event
from .forms import *
from django.contrib.auth.views import login as auth_login
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers
from django.conf import settings
from django.shortcuts import redirect, render
from django.db.models import Q
from django.contrib.gis.measure import D
import json
import time

def index(request):
    # 인덱스 페이지
    school_cnt = School.objects.all().count()
    society_cnt = Society.objects.all().count()
    event_cnt = Event.objects.all().count()
    context = {}
    context['school_cnt'] = school_cnt
    context['society_cnt'] = society_cnt
    context['event_cnt'] = event_cnt

    return render(request, 'dongzip/index.html', context)


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


    providers = []
    for provider in get_providers():
        try:
            provider.social_app = SocialApp.objects.get(provider=provider.id, sites=settings.SITE_ID)
        except SocialApp.DoesNotExist:
            provider.social_app = None
        providers.append(provider)

    return render(request, 'dongzip/member_regist1.html', {'providers': providers})

    return render(request, 'dongzip/member_regist1.html', {'form' : form})


    return render(request, 'dongzip/member_regist1.html', {'school', school})


    return render(request, 'dongzip/member_info_regist.html', {'form' : form})


def school_list(request):
    # 전체 학교 리스트
    keyword = request.GET.get('keyword','')
    result = School.objects.all().filter(name__contains=keyword)
    keyword_display=""
    schools = School.objects.all()
    if keyword:
        schools = result
        keyword_display = request.GET.get('keyword','')+" 에 대한 검색결과입니다."

    context={'keyword' : keyword, 'schools':schools, 'keyword_display':keyword_display}
    return render(request, 'dongzip/school_list.html', context )

def school_detail(request, id):
    school = School.objects.filter(id=id)
    return render(request,'dongzip/school_detail.html',{'school':school})
'''
학교별 동아리 리스트
관심사 별 동아리 리스트 별개
url 어떤식을 나눌까.
'''
def society_list(request, id):
    # 학교 별 동아리 리스트
    societys = Society.objects.filter(school_id = id)
    return render(request, 'dongzip/society_list.html', {
            'societys' : societys,
        } )


'''
url
동아리 id값을 받아올지
동아리 이름으로 받아올지
url에서 society_detail뺼지

'''
def society_detail(request, id):
    # 동아리 별 세부페이지
    society = Society.objects.get(id = id)

    return render(request, 'dongzip/society_detail.html', {
            'society' : society,
        })

def society_search(request):
    # 동아리 검색
    '''
        학교 이름도 키워드로 넣어야 함 더러운 방법 뿐인가??
        자동완성 기능 넣기
    '''

    if request.method == 'GET':
        keyword = request.GET.get('q','')
        distance = request.GET.get('distance')
        school_name = request.GET.get('school')

        school_pnt = School.objects.get(name = school_name).point

        school_list = School.objects.filter(
            point__distance_lte = (school_pnt, D(km = distance)))

        school_society_list = []
        for school in school_list:
            society = Society.objects.filter(school = school)
            school_society_list.append(society)

        print(school_society_list)
        search_society_list = Society.objects.filter(
                Q(description__icontains = keyword) | Q(name__icontains = keyword) | Q(school__name__icontains = keyword))


        context = {}
        context['search_society_list'] = search_society_list
        context['keyword'] = keyword

        return render(request, 'dongzip/society_search.html', context)
    return render(request, 'dongzip/society_search.html')

def society_regist(request):
    # 동아리 등록
    if request.method == 'POST':
        form = SocietyForm(request.POST)
        if form.is_valid():
            society = form.save()
            # reverse('dongzip:society_list', args=[society.id]). => "/soceity/1/""
            # resolve_url('dongzip:society_list', society.id).    => "/soceity/1/"
            # redirect('dongzip:society_list', society.id)        => HttpResponse
            return redirect('dongzip:society_list', society.school_id)
    else:
        form = SocietyForm()
    return render(request, 'dongzip/society_regist.html', {'form' : form})

def ajax_search(request):
    if request.is_ajax():
        keyword = request.GET.get('term','')
        school_list = School.objects.all().filter(name__icontains = keyword)
        results = []
        for school in school_list:
            school_json = {}
            school_json['id'] = school.id
            school_json['label'] = school.name
            school_json['value'] = school.name
            results.append(school_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def ajax_counter(request):
    # 메인페이지 대쉬보드 카운트

    if request.is_ajax():
        time.sleep(2) # 응답 대기 시간

        school_cnt = School.objects.all().count()
        society_cnt = Society.objects.all().count()
        event_cnt = Event.objects.all().count()

        count_json = {} # 넘겨줄 데이터
        count_json['school_cnt'] = school_cnt
        count_json['society_cnt'] = society_cnt
        count_json['event_cnt'] = event_cnt

    data = json.dumps(count_json)# json형식을 씌워 넘겨준다
    return HttpResponse(data)
