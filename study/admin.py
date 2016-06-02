from django.contrib import admin
from .models import Study, Session


class StudyAdmin(admin.ModelAdmin):
    list_display = ('name_text', 'description', 'qualifications')


class SessionAdmin(admin.ModelAdmin):
    list_display = ('study', 'session_date', 'child')

admin.site.register(Study, StudyAdmin)
admin.site.register(Session, SessionAdmin)

