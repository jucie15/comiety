from django.shortcuts import render
from django.http import HttpResponse
from .models import School, Society, Profile, Event
from .forms import *
from django.shortcuts import redirect, render
import json
import time

def index(request):
    # 인덱스 페이지
    schools = School.objects.all().count()
    societys = Society.objects.all().count()
    events = Event.objects.all().count()
    context = {}
    context['schools'] = schools
    context['societys'] = societys
    context['events'] = events



    return render(request, 'dongzip/index.html',context)


def member_regist(request):
    # 회원 가입
    ########################################################
    #auth.user FORM을 따로 만들어서 연동해야하나??
    #allauth로 페북 가입 후 추가 정보(Profile)만 입력 받아서 저장 혹은 업데이트 해주면되나??
    ########################################################

    if request.method == 'POST':
        form = ProfileForm(request.POST)
        if form.is_valid():
            member = form.save()
            # reverse('dongzip:society_list', args=[society.id]). => "/soceity/1/""
            # resolve_url('dongzip:society_list', society.id).    => "/soceity/1/"
            # redirect('dongzip:society_list', society.id)        => HttpResponse
            return redirect('dongzip:index')
    else:
        form = ProfileForm()
    return render(request, 'dongzip/member_regist.html', {'form' : form})


    return render(request, 'dongzip/member_regist.html', {'school', school})

def school_list(request):
    # 전체 학교 리스트
    schools = School.objects.all()
    return render(request, 'dongzip/school_list.html', {'schools' : schools} )

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
    # 동아리 및 학교 검색
    if request.method == 'POST':
        name = request.POST['id']

        schools = School.objects.filter(name__icontains = name)
        societys = Society.objects.filter(name__icontains = name)

        context = {}
        context['schools'] = schools
        context['societys'] = societys

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

