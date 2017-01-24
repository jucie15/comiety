from django.contrib import admin
from .models import Profile, School, Society, Event

class  ProfileAdmin(admin.ModelAdmin):

    #list_display = ('name', 'email')
    model = Profile

class SchoolAdmin(admin.ModelAdmin):
    model = School

class SocietyAdmin(admin.ModelAdmin):
    model = Society

class EventAdmin(admin.ModelAdmin):
    model = Event

admin.site.register(Profile, ProfileAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Society, SocietyAdmin)
admin.site.register(Event, EventAdmin)
