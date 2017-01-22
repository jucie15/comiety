from django.contrib import admin
from .models import User, School, Society, Event

class  UserAdmin(admin.ModelAdmin):

    list_display = ('name', 'email')
    model = User

class SchoolAdmin(admin.ModelAdmin):
    model = School

class SocietyAdmin(admin.ModelAdmin):
    model = Society

class EventAdmin(admin.ModelAdmin):
    model = Event

admin.site.register(User, UserAdmin)
admin.site.register(School, SchoolAdmin)
admin.site.register(Society, SocietyAdmin)
admin.site.register(Event, EventAdmin)
