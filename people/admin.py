from django.contrib import admin
from .models import Parent, Child, Family, Guardian, Disability, Language


class LanguageInline(admin.TabularInline):
    model = Language


class ParentAdmin(admin.ModelAdmin):
    pass


class ChildAdmin(admin.ModelAdmin):
    inlines = [LanguageInline, ]


class FamilyAdmin(admin.ModelAdmin):
    pass


class GuardianAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')


class DisabilityAdmin(admin.ModelAdmin):
    list_display = ('name', 'order')


class LanguageAdmin(admin.ModelAdmin):
    pass


admin.site.register(Parent, ParentAdmin)
admin.site.register(Child, ChildAdmin)
admin.site.register(Family, FamilyAdmin)
admin.site.register(Guardian, GuardianAdmin)
admin.site.register(Disability, DisabilityAdmin)
admin.site.register(Language, LanguageAdmin)