from django import forms
from django.forms.models import BaseInlineFormSet

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field
from crispy_forms.bootstrap import UneditableField, PrependedText
from localflavor.us.forms import USZipCodeField

from core.forms import SubmitCommonLayout, SubmitAddressLayout

from .models import Family, Parent, Child, Language

class FamilyForm(forms.ModelForm):
    class Meta:
        model = Family
        fields = ('name_text',)

    def __init__(self, *args, **kwargs):
        super(FamilyForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.layout = Layout(
            Fieldset(
                'Family Name',
                'name_text'
                )
        )
        self.helper.form_tag = False


class AddressForm(forms.ModelForm):
    zipcode = USZipCodeField(required=False)

    class Meta:
        model = Family
        fields = ('address1', 'address2', 'city', 'state', 'zipcode', 'homephone', 'preferred_contact_type', 'lab_reference', 'lab_reference_other', 'notes')

    def __init__(self, *args, **kwargs):
        super(AddressForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset(
                'Address Fields',
                'address1',
                'address2',
                'city',
                'state',
                'zipcode',
                'homephone',
                'preferred_contact_type',
            ),
            Fieldset(
                'Misc',
                'lab_reference',
                'lab_reference_other',
                'notes'
            ),
            SubmitCommonLayout()
        )
        self.helper.form_tag = True


class ParentForm(forms.ModelForm):
    class Meta:
        model = Parent
        fields = ('name_first_text', 'name_last_text', 'guardian_type', 'workphone', 'cellphone', 'email', 'family')

    def __init__(self, *args, **kwargs):
        super(ParentForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
           Fieldset(
                'Parent Fields',
                'name_first_text',
                'name_last_text',
                'guardian_type',
                'workphone',
                'cellphone',
                'email',
                Field('family', type='hidden')
            ),
            SubmitCommonLayout()
        )
        self.helper.form_tag = True

    def clean(self):
        cleaned_data = super(ParentForm, self).clean()

        print "calling clean function for parent"

        if not cleaned_data['name_last_text']:
            cleaned_data['name_last_text'] = cleaned_data['family']

        return cleaned_data


class ParentFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ParentFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            'name_first_text',
            'name_last_text',
            'guardian_type',
        )
        self.form_tag = False
        self.template = 'people/table_inline_formset.html'
        self.form_id = 'parent'
        self.legend = 'Parents'


class ChildForm(forms.ModelForm):
    child_id = forms.IntegerField(label='ID', required=False)
    age = forms.CharField(max_length=100, required=False)
    dob_date = forms.DateField(label='Birth Day', input_formats = ['%m-%d-%Y'])

    class Meta:
        model = Child
        fields = ('name_first_text', 'name_last_text', 'gender_type', 'dob_date', 'babylab_id', 'kid_neurolab_id', 'ethnicity', 'race',
                  'handedness', 'fmri', 'fmri_date', 'dob_early', 'disability', 'breastfed', 'breastfeeding_duration', 'bottle_fed',
                  'notes', 'family')

    def __init__(self, *args, **kwargs):
        super(ChildForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
            Fieldset(
                'ID',
                PrependedText('child_id', 'ID'),
                PrependedText('babylab_id', 'B'),
                PrependedText('kid_neurolab_id', 'K'),
            ),
            Fieldset(
                'Demographics',
                'name_first_text',
                'name_last_text',
                'gender_type',
                'dob_date',
                UneditableField('age'),
                'ethnicity',
                'race',
                Field('family', type='hidden'),
            ),
            Fieldset(
                'Medical',
                'handedness',
                'fmri',
                'fmri_date',
                'dob_early',
                'disability',
            ),
            Fieldset(
                'Misc',
                'breastfed',
                'breastfeeding_duration',
                'bottle_fed',
                'notes',
            ),
            SubmitCommonLayout()
        )
        self.helper.form_tag = True

    def clean(self):
        cleaned_data = super(ChildForm, self).clean()

        print "calling clean function for child"

        if not cleaned_data['name_last_text']:
            cleaned_data['name_last_text'] = cleaned_data['family']

        return cleaned_data


class ChildFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(ChildFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
                'name_first_text',
                'name_last_text',
                'gender_type',
                'dob_date',
        )
        self.form_tag = False
        self.template = 'people/table_inline_formset.html'
        self.form_id = 'child'
        self.legend = 'Children'


class LanguageForm(forms.ModelForm):
    class Meta:
        model = Language
        fields = ('name', 'percent')

    def __init__(self, *args, **kwargs):
        super(LanguageForm, self).__init__(*args, **kwargs)
        self.helper = FormHelper()
        self.helper.form_class = 'form-horizontal'
        self.helper.label_class = 'col-lg-2'
        self.helper.field_class = 'col-lg-8'
        self.helper.layout = Layout(
           Fieldset(
                'Language Fields',
                'name',
                'percent',
                Field('child', type='hidden')
            ),
            SubmitCommonLayout()
        )
        self.helper.form_tag = True


class LanguageFormSetHelper(FormHelper):
    def __init__(self, *args, **kwargs):
        super(LanguageFormSetHelper, self).__init__(*args, **kwargs)
        self.form_method = 'post'
        self.layout = Layout(
            'name',
            'percent',
        )
        self.form_tag = False
        self.template = 'people/table_inline_formset.html'
        self.form_id = 'language'
        self.legend = 'Languages Heard'


class PercentTotalFormSet(BaseInlineFormSet):
    def clean(self):
        super(PercentTotalFormSet, self).clean()
        if any(self.errors):
            # Don't bother validating the formset unless each form is valid on its own
            return
        total_sum = 0
        for form in self.forms:
            if not form.cleaned_data.get('DELETE'):
                total_sum += form.cleaned_data.get('percent', 0)
        if total_sum > 100:
            for form in self.forms:
                if form.cleaned_data.get('percent', 0) > 0:
                    form.add_error('percent', 'Total language percentage cannot exceed 100')