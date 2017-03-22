from django.shortcuts import render
from django.http import HttpResponse
from .models import School, Society, Profile, Event, Category, Membership
from geodjango.models import SchoolLocation
from .forms import *
from django.contrib.auth.views import login as auth_login
from django.contrib.auth.decorators import login_required
from allauth.socialaccount.models import SocialApp
from allauth.socialaccount.templatetags.socialaccount import get_providers
from django.conf import settings
from django.shortcuts import redirect, render, get_object_or_404
from django.db.models import Q
from django.contrib.gis.measure import D
import json
import time



def index(request):
    if request.user.is_anonymous() or Profile.objects.filter(user=request.user).exists():
        school_cnt = School.objects.all().count()
        society_cnt = Society.objects.all().count()
        event_cnt = Event.objects.all().count()
        category_list = Category.objects.all()

        context = {}
        context['school_cnt'] = school_cnt
        context['society_cnt'] = society_cnt
        context['event_cnt'] = event_cnt
        context['category_list'] = category_list
        return render(request, 'dongzip/index.html', context)

    # 인덱스 페이지
    else:
        return redirect ('accounts:member_info_regist')


def school_list(request):
    # 전체 학교 리스트
    keyword = request.GET.get('keyword','')
    school_list = School.objects.filter(name__contains=keyword)

    context = {}
    context['keyword'] = keyword
    context['school_list'] = school_list

    return render(request, 'dongzip/school_list.html', context)

def school_detail(request, id):
    # 학교별 세부페이지
    school = get_object_or_404(School, id=id)

    keyword = request.GET.get('keyword','')

    # 키워드 검색 조건
    condition = (Q(description__icontains = keyword) | Q(name__icontains = keyword)) & Q(school = school)

    society_list = Society.objects.filter(condition)

    society_number = Society.objects.filter(school=school).count()
    school_point = get_object_or_404(SchoolLocation, school__name = school)


    context = {}
    context['keyword'] = keyword
    context['society_list'] = society_list
    context['school'] = school # 수정 할지 확인하기
    context['society_number'] = society_number
    context['school_point'] = school_point
    # context['school_lng'] =
    # context['school_lat'] =

    return render(request,'dongzip/school_detail.html', context)


'''
url
동아리 id값을 받아올지
동아리 이름으로 받아올지
url에서 society_detail뺼지

'''
def society_detail(request, id):
    # 동아리 별 세부페이지
    society = get_object_or_404(Society, id=id)

    return render(request, 'dongzip/society_detail.html', {
            'society' : society,
        })

def society_apply(request, id):
    society = get_object_or_404(Society, id=id)
    user = request.user.profile
    membership = Membership(society=society, user=user, power=-1)
    membership.save()

    return redirect('dongzip:society_detail', id)

def society_search(request, name):
    # 동아리 검색
    # 동아리가 소속된 학교 위치 기반으로 필터링 후 키워드 검색

    '''
        자동완성 기능 넣기
        혹시나 학교의 좌표 받아올때(get() 사용) 값이 없을 경우 예외 처리 혹시나
    '''
    keyword = request.GET.get('q', '')
    distance = request.GET.get('distance')
    school_name = request.GET.get('school', '')
    category_name = '전체 검색'

    # 키워드 검색 쿼리문
    condition = Q(description__icontains = keyword) | Q(name__icontains = keyword) | Q(school__name__icontains = keyword)

    if school_name != '':
        # 학교 위치 기반 필터링을 원할 경우 조건 추가
        school_pnt = get_object_or_404(SchoolLocation, school__name=school_name).point
        condition = condition & Q(school__schoollocation__point__distance_lte = (school_pnt, D(km = distance)))
        school = get_object_or_404(School, name=school_name)

    if name != 'all':
        # 카테고리 분류별 필터링을 원할 경우 조건 추가
        condition = condition & Q(categorys__url_name = name)
        category_name = get_object_or_404(Category, url_name__icontains=name).name

    search_society_list = Society.objects.filter(condition)
    context = {}
    context['search_society_list'] = search_society_list
    context['keyword'] = keyword
    context['category_name'] = category_name
    context['school_name'] = school_name
    context['name'] = name

    return render(request, 'dongzip/society_search.html', context)


@login_required
def society_regist(request):
    # 동아리 등록
    if request.is_ajax():
        render(request, 'dongzip/society_regist.html', {'form' : form})
    if request.method == 'POST':
        form = SocietyForm(request.POST)
        user = request.user.profile
        if form.is_valid():
            society = form.save(commit = False)
            society.school = user.school
            society.save()
            membership = Membership(user=user, society=society, power=2)
            membership.save()
            # reverse('dongzip:society_list', args=[society.id]). => "/soceity/1/""
            # resolve_url('dongzip:society_list', society.id).    => "/soceity/1/"
            # redirect('dongzip:society_list', society.id)        => HttpResponse
            return redirect('dongzip:society_detail', society.id)
    else:
        form = SocietyForm()
    return render(request, 'dongzip/society_regist.html', {'form' : form})


@login_required
def society_admin(request, id):

     # if request.user.profile.membership_set.get(society_id=id).power >= 1:
    #     pass
    manager = get_object_or_404(Profile, society__id = id, membership__power = 2)
    staff_list = Profile.objects.filter(society__id = id, membership__power = 1)
    member_list = Profile.objects.filter(society__id = id, membership__power = 0)
    applicants = Profile.objects.filter(society__id=id, membership__power=-1)
    society = get_object_or_404(Society, id=id)
    applicants = Profile.objects.filter(society__id=id,membership__power=-1)

    context={}
    context['applicants'] = applicants
    context['member_list'] = member_list
    context['society_id'] = id
    context['manager'] = manager
    context['staff_list'] = staff_list
    context['society'] = society

    return render(request, 'dongzip/society_admin.html', context)


def society_admin_manager_edit(request, id):
    if request.user.profile.membership_set.get( society_id = id ).power != 2:
        #권한 수정하려는 유저가 동쨩이아닐 경우
        pass

    if request.method == 'POST':
        manager_id = get_object_or_404(Profile,society__id = id, membership__power = 2).id
        new_manager_id = request.POST.get('manager_id') # 새로운 동쨩 id
        manager = get_object_or_404(Membership, society_id = id, user_id = manager_id)
        new_manager = get_object_or_404(Membership, society_id = id, user_id = new_manager_id)


        manager.power = 1
        new_manager.power = 2

        manager.save()
        new_manager.save()

    return redirect('dongzip:society_admin', id)


def society_admin_manager_add(request, id):
    if request.user.profile.membership_set.get( society_id = id ).power < 1:
    #권한 수정하려는 유저가 운영진이 아닐 경우
        pass

    if request.method == 'POST':
        member_id = request.POST.get('member_id')
        member = get_object_or_404(Membership, society_id = id, user_id = member_id)

        member.power = 1
        member.save()

    return redirect('dongzip:society_admin', id)



def society_admin_manager_remove(request, id):
    if request.user.profile.membership_set.get( society_id = id ).power != 2:
    #권한 수정하려는 유저가 관리자가 아닐 경우
        pass

    if request.method == 'POST':
        staff_id = request.POST.get('staff_id')
        staff = get_object_or_404(Membership, society_id = id, user_id = staff_id)

        staff.power = 0
        staff.save()

    return redirect('dongzip:society_admin', id)


@login_required
def society_admin_info(request, id):
    society = get_object_or_404(Society, id=id)

    if request.method=="POST":
        form = SocietyForm(request.POST, request.FILES, instance=society)
        if form.is_valid():
            society = form.save()
            return redirect("dongzip:society_admin", society.id)
    else:
        form = SocietyForm(instance=society)
        return render(request, "dongzip/society_admin_1.html", { 'form':form, 'society':society })


# 미완성 아직 수정 필요! 템플릿도 수정 필요!
@login_required
def society_admin_member_edit(request,id):
    member_list = Profile.objects.filter(society__id = id, membership__power = 0)
    applicants = Profile.objects.filter(society__id=id, membership__power=-1)
    return render(request, "dongzip/society_admin_member_edit.html", {
        'member_list':member_list, 'applicants':applicants })


@login_required
def society_admin_member_info(request, id):
    society = get_object_or_404(Society, id=id)

    return render(request, 'dongzip/society_admin_member_info.html', {
            'society' : society,
        })


@login_required
def society_admin_manager_info(request, id):
    manager = get_object_or_404(Profile, society__id = id, membership__power = 2)
    staff_list = Profile.objects.filter(society__id = id, membership__power = 1)
    member_list = Profile.objects.filter(society__id = id, membership__power = 0)
    applicants = Profile.objects.filter(society__id=id, membership__power=-1)
    society = get_object_or_404(Society, id=id)
    applicants = Profile.objects.filter(society__id=id,membership__power=-1)

    context={}
    context['applicants'] = applicants
    context['member_list'] = member_list
    context['society_id'] = id
    context['manager'] = manager
    context['staff_list'] = staff_list
    context['society'] = society

    return render(request, 'dongzip/society_admin_manager_info.html', context)

@login_required
def favorite_society(request, id):
    # 동아리 즐겨찾기 기능
    if request.is_ajax():
        user = request.user.profile # 요청 유저

        society = get_object_or_404(Society, id=id) # 즐겨찾을 동아리
        if user.favorite_society.filter(id=id).exists():
            # 이미 즐겨찾기 등록이 되있으면
            # 즐겨찾기 삭제
            user.favorite_society.remove(society)
            message = '즐겨찾기 해제'
            isFavorite = False
        else:
            # 즐겨찾기 추가
            user.favorite_society.add(society)
            message = '즐겨찾기 추가'
            isFavorite = True

        context = {}
        context['message'] = message
        context['isFavorite'] = isFavorite
        data = json.dumps(context)
    else:
        data = json.dumps({'status':'fail'})
    return HttpResponse(data)


def event_list(request):
    return render(request, 'dongzip/event_list.html')

def event_detail(request):
    return render(request, 'dongzip/event_detail.html')


def ajax_search_event(request):
    if request.is_ajax():
        keyword = request.GET.get('term','')
        event_list = Event.objects.all().filter(title__icontains = keyword)
        results = []
        for event in event_list:
            event_json = {}
            event_json['label'] = event.title
            results.append(event_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def ajax_search_sch(request):
    # 자동 완성 기능
    if request.is_ajax():
        keyword = request.GET.get('term','')
        school_list = School.objects.all().filter(name__icontains = keyword)
        results = []
        for school in school_list:
            school_json = {}
            school_json['id'] = school.id
            school_json['label'] = school.name
            results.append(school_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)


def ajax_search_soc(request, id):
    # 자동 완성 기능
    if request.is_ajax():
        keyword = request.GET.get('term','')

        school = get_object_or_404(School, id=id)
        condition = (Q(description__icontains = keyword) | Q(name__icontains = keyword)) & Q(school = school)
        society_list = school.society_set.filter(condition)
        results = []
        for society in society_list:
            society_json = {}
            society_json['label'] = society.name
            results.append(society_json)
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

        global count_json
        count_json ={}

        count_json['school_cnt'] = school_cnt
        count_json['society_cnt'] = society_cnt
        count_json['event_cnt'] = event_cnt

    else:
        count_json = {} # 넘겨줄 데이터

    data = json.dumps(count_json)# json형식을 씌워 넘겨준다
    return HttpResponse(data)

def ajax_search_related(request, name):
    # 자동 완성 기능
    if request.is_ajax():
        keyword = request.GET.get('term','')
        condition = Q(name__icontains = keyword)

        if name != 'all':
            # 카테고리 분류별 필터링을 원할 경우 조건 추가
            condition = condition & Q(categorys__url_name = name)
            society_list = Society.objects.filter(condition)
        results = []
        for society in society_list:
            society_json = {}
            society_json['label'] = society.name

            results.append(society_json)
        data = json.dumps(results)
    else:
        data = 'fail'
    mimetype = 'application/json'
    return HttpResponse(data, mimetype)

def aboutus(request):
    return render(request, 'dongzip/aboutus.html')


def privacy_policy(request):
    return render(request, 'dongzip/privacy_policy.html')





