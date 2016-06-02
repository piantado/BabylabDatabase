from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django import forms

from .models import MyUser


class MyUserChangeForm(UserChangeForm):
    class Meta(UserChangeForm.Meta):
        model = MyUser


class MyUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = MyUser

    def clean_username(self):
        username = self.cleaned_data['username']
        try:
            MyUser.objects.get(username=username)
        except MyUser.DoesNotExist:
            return username
        raise forms.ValidationError(self.error_messages['duplicate_username'])


class MyUserAdmin(UserAdmin):
    form = MyUserChangeForm
    add_form = MyUserCreationForm
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('title', )}),
    )
    list_display = ('username', 'first_name', 'last_name', 'email', 'is_active', 'title', )
    list_filter = ('is_active', 'is_staff', )


admin.site.register(MyUser, MyUserAdmin)