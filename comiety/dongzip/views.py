from django.shortcuts import render
from django.http import HttpResponse
from .models import School, Society, Profile
from .forms import SocietyForm
from django.shortcuts import redirect, render

def index(request):
    # 인덱스 페이지
    # schools = School.objects.all()

    # for school in schools:
    #     school_cnt = Profile.objects.filter(school_id = school.id).count()
    #     school.member_number = school_cnt
    #     school.save()

    return render(request, 'dongzip/index.html')


def member_regist(request):
    #회원 가입
    # profile = Profile.objects.get(id = 1)
    # profile.save()
    school = School.objects.get(id = 2)
    # school = School.objects.get(pk=1)
    # school.member_number += 1
    # school.save()
    return HttpResponse(school.member_number)

def school_list(request):
    #전체 학교 리스트
    schools = School.objects.all()
    return render(request, 'dongzip/school_list.html', {'schools' : schools} )


def society_list(request, id):
    #학교 별 동아리 리스트
    societys = Society.objects.filter(school_id = id)
    return render(request, 'dongzip/society_list.html', {'societys' : societys} )


def society_search(request):
    #동아리 및 학교 검색
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
    #동아리 등록

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

