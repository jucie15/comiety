from django.shortcuts import render
from django.http import HttpResponse
from .models import School, Society, Profile
from .forms import SocietyForm
from django.shortcuts import redirect, render

def index(request):
    # schools = School.objects.all()

    # for school in schools:
    #     school_cnt = Profile.objects.filter(school_id = school.id).count()
    #     school.member_number = school_cnt
    #     school.save()

    return render(request, 'dongzip/index.html')


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


def society_search(request):
    if request.method == 'POST':
        name = request.POST['id']

        schools = School.objects.filter(name__icontains = name)
        societys = Society.objects.filter(name__icontains = name)

        context = {}
        context['schools'] = schools
        context['societys'] = societys

        return render(request, 'dongzip/society_search.html', context)
    return render(request, 'dongzip/society_search.html')

# def society_regist(request):
#     if request.method == 'POST':
#         form = SocietyForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return render(request, 'dongzip/society_list.html', {'societys' : societys})
#     else:
#         form = SearchSocietyForm()
#     return render(request, 'dongzip/society_regist.html')

