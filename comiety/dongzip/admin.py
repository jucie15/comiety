from django.contrib import admin
from .models import *

class  ProfileAdmin(admin.ModelAdmin):

    #list_display = ('name', 'email')
    model = Profile

class SchoolAdmin(admin.ModelAdmin):
    model = School
    search_fields = ('name', )

class SocietyAdmin(admin.ModelAdmin):
    model = Society

class EventAdmin(admin.ModelAdmin):
    model = Event

class CategoeryAdmin(admin.ModelAdmin):
    model = Category


admin.site.register(Profile, ProfileAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Society, SocietyAdmin)
admin.site.register(Event, EventAdmin)
admin.site.register(Category, CategoeryAdmin)
