from django.forms import ModelForm
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field
from django.forms.widgets import CheckboxSelectMultiple

from .models import Study, Session

from core.forms import SubmitCommonLayout


class StudyForm(ModelForm):
    class Meta:
        model = Study
        fields = ('name_text', 'description', 'start_date', 'end_date', 'pi', 'age_min', 'age_max', 
            'percent_english_heard', 'allowed_disabilities', 'born_early', 'qualifications')
        #widgets = {
        #    'allowed_disabilities': CheckboxSelectMultiple(),
        #}

    def __init__(self, *args, **kwargs):
        super(StudyForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset(
                'Study',
                'name_text',
                'description',
                'pi',
                'start_date',
                'end_date'
            ),
           Fieldset(
                'Qualifications',
                'age_min',
                'age_max',
                'percent_english_heard',
                'allowed_disabilities',
                'born_early',
                'qualifications'
            ),
            SubmitCommonLayout()
        )

        self.helper.form_tag = True


class SessionForm(ModelForm):
    class Meta:
        model = Session
        fields = ('study', 'session_date', 'staff', 'child')

    def __init__(self, *args, **kwargs):
        super(SessionForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset(
                'Session Fields',
                'session_date',
                'staff',
                # 'study',
                Field('study', type='hidden'),
                Field('child', type='hidden')
            ),
            SubmitCommonLayout()
        )
        self.helper.form_tag = True