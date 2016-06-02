from django.forms import ModelForm

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field

from .models import Contact, Appointment

from core.forms import SubmitCommonLayout


class ContactForm(ModelForm):

    class Meta:
        model = Contact
        fields = ('contact_datetime', 'contact_mode_type', 'contact_result_type', 'staff', 'notes', 'child', )

    def __init__(self, *args, **kwargs):
        super(ContactForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset(
                'Contact Fields',
                'contact_datetime',
                'contact_mode_type',
                'contact_result_type',
                'staff',
                'notes',
                Field('child', type='hidden'),
            ),
            SubmitCommonLayout(),
        )
        self.helper.form_tag = True


class AppointmentForm(ModelForm):

    class Meta:
        model = Appointment
        fields = ('appointment_datetime', 'appointment_duration', 'study', 'room', 'run_by', 'status_type', 'reminder_made_type', 'reminder_datetime', 'confirmation_email_type', 'parking_type', 'parking_note', 'babysitter_type', 'notes', 'child',
                 )

    def __init__(self, *args, **kwargs):
        super(AppointmentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset(
                'Appointment',
                'appointment_datetime',
                'appointment_duration',
                'study',
                'room',
                'run_by',
                'status_type',
                Field('child', type='hidden'),
            ),
            Fieldset(
                'Reminder',
                'reminder_made_type',
                'reminder_datetime',
                'confirmation_email_type',
            ),
            Fieldset(
                'Misc',
                'parking_type',
                'parking_note',
                'babysitter_type',
                'notes',
            ),
            SubmitCommonLayout(),
        )
        self.helper.form_tag = True





