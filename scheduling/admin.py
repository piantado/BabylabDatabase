from django.contrib import admin

from .models import Contact, Appointment, Room


class ContactAdmin(admin.ModelAdmin):
    pass


class AppointmentAdmin(admin.ModelAdmin):
    pass


class RoomAdmin(admin.ModelAdmin):
    pass

admin.site.register(Contact, ContactAdmin)
admin.site.register(Appointment, AppointmentAdmin)
admin.site.register(Room, RoomAdmin)