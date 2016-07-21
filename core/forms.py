from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, HTML
from crispy_forms.bootstrap import FormActions

from django import forms
from django.contrib.auth import authenticate

from .models import MyUser
from .widgets import CustomDateWidget, CustomSplitDateTimeWidget

# This overrides all DateField and DateTimeField forms in this project
# in order to use the custom widgets
forms.DateField.widget = CustomDateWidget
forms.SplitDateTimeField.widget = CustomSplitDateTimeWidget #changed this from DateTimeField? http://stackoverflow.com/questions/34332184/django-adminsplitdatetime-valid-date-time-error
forms.SplitDateTimeField.input_date_formats = ['%m-%d-%Y']
forms.SplitDateTimeField.input_time_formats = ['%I:%M %p']
#forms.DateTimeField.input_formats = ('%Y-%m-%d %I:%M %p',)
#forms.DateTimeField.input_formats = ['%m-%d-%Y %I:%M %p']


class LoginCommonLayout(Layout):
    def __init__(self, *args, **kwargs):
        super(LoginCommonLayout, self).__init__(
            FormActions(
                HTML('<button class="btn btn-success" type="submit">Log In</button>')
            )
        )


class AccountLogin(ModelForm):

    class Meta:
        model = MyUser
        fields = ('username', 'password',)
        help_texts = {'username': ''}
        widgets = {'password': forms.PasswordInput(render_value=False)}

    def __init__(self, *args, **kwargs):
        super(AccountLogin, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-md-2'
        self.helper.field_class = 'col-md-4'
        self.helper.layout = Layout(
            Fieldset(
                'Please Sign In',
                'username',
                'password',
            ),
            LoginCommonLayout()
        )
        self.helper.form_tag = True

    def clean(self):
        username = self.cleaned_data.get('username')
        password = self.cleaned_data.get('password')

        self._user = authenticate(username=username, password=password)
        if self._user is None:
            raise forms.ValidationError('Invalid username and/or password')
        elif not self._user.is_active:
            raise forms.ValidationError('Your account is inactive')
        return self.cleaned_data

    def save(self):
        return getattr(self, "_user", None)


class SubmitCommonLayout(Layout):
    def __init__(self, *args, **kwargs):
        super(SubmitCommonLayout, self).__init__(
            FormActions(
                HTML('<button class="btn btn-primary" type="submit"><span class="fa fa-floppy-o"></span> Save</button>')
            )
        )

#class SplitDateTimeForm(forms.Form):
#    splitdatetime = CustomSplitDateTimeField()