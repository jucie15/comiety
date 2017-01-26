from django.shortcuts import render
from django.http import HttpResponse
from .models import School, Society, Profile

def index(request):
    schools = School.objects.all()

    for school in schools:
        school_cnt = Profile.objects.filter(school_id = school.id).count()
        school.member_number = school_cnt
        school.save()

    return render(request, 'dongzip/login.html')


def member_regist(request):

    # profile = Profile.objects.get(id = 1)
    # profile.save()
    school = School.objects.get(id = 2)
    # school = School.objects.get(pk=1)
    # school.member_number += 1
    # school.save()
    return HttpResponse(school.member_number)


def school_list(request):
    schools = School.objects.all()
    return render(request, 'dongzip/school_list.html', {'schools' : schools} )


def society_list(request, id):
    societys = Society.objects.filter(school_id = id)
    return render(request, 'dongzip/society_list.html', {'societys' : societys} )
