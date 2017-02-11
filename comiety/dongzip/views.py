from django.shortcuts import render
from django.http import HttpResponse
from .models import School, Society, Profile, Event
from geodjango.models import SchoolLocation
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


def school_list(request):
    # 전체 학교 리스트
    keyword = request.GET.get('keyword','')
    school_list = School.objects.filter(name__contains=keyword)

    context = {}
    context['keyword'] = keyword
    context['school_list'] = school_list

    return render(request, 'dongzip/school_list.html', context )

def school_detail(request, id):
    # 학교별 세부페이지
    school = School.objects.get(id=id)

    keyword = request.GET.get('keyword','')

    # 키워드 검색 조건
    condition = (Q(description__icontains = keyword) | Q(name__icontains = keyword)) & Q(school = school)

    society_list = Society.objects.filter(condition)

    context = {}
    context['keyword'] = keyword
    context['society_list'] = society_list
    context['school'] = school # 수정 할지 확인하기

    return render(request,'dongzip/school_detail.html', context)


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

def society_search(request, name):
    # 동아리 검색
    # 동아리가 소속된 학교 위치 기반으로 필터링 후 키워드 검색

    '''
        자동완성 기능 넣기
        혹시나 학교의 좌표 받아올때(get() 사용) 값이 없을 경우 예외 처리 혹시나
    '''
    if request.method == 'GET':
        keyword = request.GET.get('q', '')
        distance = request.GET.get('distance')
        school_name = request.GET.get('school', '')

        # 키워드 검색 쿼리문
        condition = Q(description__icontains = keyword) | Q(name__icontains = keyword) | Q(school__name__icontains = keyword)

        if school_name != '':
            # 학교 위치 기반 필터링을 원할 경우 조건 추가
            school_pnt = SchoolLocation.objects.get(school__name = school_name).point # 지정 학교의 좌표
            condition = condition & Q(school__schoollocation__point__distance_lte = (school_pnt, D(km = distance)))

        if name != 'all':
            # 카테고리 분류별 필터링을 원할 경우 조건 추가
            condition = condition & Q(categorys__name = name)

        search_society_list = Society.objects.filter(condition)

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
            school_json['label'] = school.name
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

def aboutus(request):
    return render(request, 'dongzip/aboutus.html')
# front test
def profile(request):
    return render(request, 'dongzip/my_profile.html')

def society_admin(request):
    return render(request, 'dongzip/society_admin.html')

