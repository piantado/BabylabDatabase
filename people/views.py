from django.views.generic import CreateView, TemplateView, ListView, DetailView, UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.forms.models import inlineformset_factory
from django.http import HttpResponseRedirect

from crispy_forms.bootstrap import UneditableField
from django_tables2.views import SingleTableMixin, RequestConfig
from braces.views import LoginRequiredMixin

from .models import Family, Parent, Child, Language
from .forms import FamilyForm, ParentForm, ChildForm, ParentFormSetHelper, ChildFormSetHelper, AddressForm, LanguageForm, LanguageFormSetHelper, PercentTotalFormSet
from .tables import ChildTable, ParentTable, FamilyTable, LanguageTable

from scheduling.tables import ContactTable, AppointmentTable
from study.tables import SessionTable, StudyTable, NoSessionTable
from core.views import CreatedMixin


class FamilyListView(LoginRequiredMixin, SingleTableMixin, ListView):
    model = Family
    template_name = 'people/family_list.html'
    table_class = FamilyTable
    table_pagination = False


class ParentListView(LoginRequiredMixin, SingleTableMixin, ListView):
    model = Parent
    template_name = 'people/parent_list.html'
    table_class = ParentTable
    table_pagination = False


class ChildListView(LoginRequiredMixin, SingleTableMixin, ListView):
    model = Child
    template_name = 'people/child_list.html'
    table_class = ChildTable
    table_pagination = False


class FamilyDetailView(LoginRequiredMixin, CreatedMixin, DetailView):
    model = Family
    template_name = 'people/family_detail.html'

    def get_context_data(self, **kwargs):
        context = super(FamilyDetailView, self).get_context_data(**kwargs)
        form = AddressForm(instance=self.object)
        form.helper.layout.pop(2)
        form.helper.form_tag = False
        form.helper.filter(basestring, max_level=1).wrap(UneditableField)
        context['form'] = form
        context['child_table'] = ChildTable(self.object.children.all(), exclude=('family', ), prefix='1-')
        RequestConfig(self.request).configure(context['child_table'])
        context['parent_table'] = ParentTable(self.object.parents.all(), exclude=('family', ), prefix='2-')
        RequestConfig(self.request).configure(context['parent_table'])
        context['contact_table'] = ContactTable(self.object.get_contacts(), prefix='3-')
        RequestConfig(self.request).configure(context['contact_table'])
        context['appointment_table'] = AppointmentTable(self.object.get_appointments(), prefix='4-')
        RequestConfig(self.request).configure(context['appointment_table'])
        return context


class AddressUpdateView(LoginRequiredMixin, UpdateView):
    model = Family
    template_name = 'people/address_update.html'
    form_class = AddressForm


class ChildDetailView(LoginRequiredMixin, CreatedMixin, DetailView):
    model = Child
    template_name = 'people/child_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ChildDetailView, self).get_context_data(**kwargs)
        form = ChildForm(instance=self.object, initial={"age": self.object.age, "child_id": self.object.id})
        form.helper.layout.pop(4)
        form.helper.form_tag = False
        form.helper.filter(basestring, max_level=1).wrap(UneditableField)
        form.helper['child_id'].update_attributes(disabled='disabled')
        form.helper['babylab_id'].update_attributes(disabled='disabled')
        form.helper['kid_neurolab_id'].update_attributes(disabled='disabled')
        context['form'] = form
        context['language_table'] = LanguageTable(self.object.languages.all(), prefix='6-')
        RequestConfig(self.request).configure(context['language_table'])
        address_form = AddressForm(instance=self.object.family)
        address_form.helper.layout.pop(2)
        address_form.helper.filter(basestring, max_level=1).wrap(UneditableField)
        address_form.helper.form_tag = False
        context['address_form'] = address_form
        context['child_table'] = ChildTable(self.object.family.children.exclude(id=self.object.id), exclude=('family', ), prefix='1-')
        RequestConfig(self.request).configure(context['child_table'])
        context['contact_table'] = ContactTable(self.object.contacts.all(), exclude=('child', ), prefix='2-')
        RequestConfig(self.request).configure(context['contact_table'])
        context['appointment_table'] = AppointmentTable(self.object.appointments.all(), exclude=('child', ), prefix='3-')
        RequestConfig(self.request).configure(context['appointment_table'])
        context['session_table'] = SessionTable(self.object.sessions.all(), exclude=('child', ), prefix='4-')
        RequestConfig(self.request).configure(context['session_table'])
        context['no_session_table'] = NoSessionTable(self.object.get_null_sessions(), exclude=('description', 'qualifications', 'child_fullname', ), prefix='5-')
        RequestConfig(self.request).configure(context['no_session_table'])
        context['family'] = self.object.family
        return context


class ParentDetailView(LoginRequiredMixin, CreatedMixin, DetailView):
    model = Parent
    template_name = 'people/parent_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ParentDetailView, self).get_context_data(**kwargs)
        form = ParentForm(instance=self.object)
        form.helper.layout.pop(1)
        form.helper.filter(basestring, max_level=1).wrap(UneditableField)
        context['form'] = form
        context['family'] = self.object.family
        return context


class ParentUpdateView(LoginRequiredMixin, UpdateView):
    model = Parent
    template_name = 'people/parent_update.html'
    form_class = ParentForm

    def get_context_data(self, **kwargs):
        context = super(ParentUpdateView, self).get_context_data(**kwargs)
        context['family'] = self.object.family
        return context


class ParentCreateView(LoginRequiredMixin, CreateView):
    model = Parent
    template_name = 'people/parent_add.html'
    form_class = ParentForm

    def get_initial(self):
        initial = super(ParentCreateView, self).get_initial()
        initial['family'] = self.kwargs.get(self.pk_url_kwarg, None)
        return initial

    def get_context_data(self, **kwargs):
        context = super(ParentCreateView, self).get_context_data(**kwargs)
        context['family'] = Family.objects.get(pk=self.kwargs.get(self.pk_url_kwarg, None))
        return context

    def get_success_url(self):
        return reverse('family_detail', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg, None)})


LanguageFormSet = inlineformset_factory(Child, Language, formset=PercentTotalFormSet, extra=1, can_delete=True, fields=('name', 'percent',))


class ChildCreateView(LoginRequiredMixin, CreateView):
    model = Child
    template_name = 'people/child_add.html'
    form_class = ChildForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        language_form = LanguageFormSet()
        language_helper = LanguageFormSetHelper()
        return self.render_to_response(
            self.get_context_data(form=form, language_form=language_form, language_helper=language_helper))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        language_form = LanguageFormSet(request.POST)
        language_helper = LanguageFormSetHelper()
        if form.is_valid() and language_form.is_valid():
            return self.form_valid(form, language_form)
        else:
            return self.form_invalid(form, language_form, language_helper)

    def form_valid(self, form, language_form):
        self.object = form.save()
        language_form.instance = self.object
        language_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, language_form, language_helper):
        return self.render_to_response(self.get_context_data(form=form, language_form=language_form, language_helper=language_helper))

    def get_initial(self):
        initial = super(ChildCreateView, self).get_initial()
        initial['family'] = self.kwargs.get(self.pk_url_kwarg, None)
        return initial

    def get_context_data(self, **kwargs):
        context = super(ChildCreateView, self).get_context_data(**kwargs)
        context['form'].helper['child_id'].update_attributes(disabled='disabled')
        context['form'].helper.form_tag = False
        context['form'].helper.layout.pop(4)
        context['family'] = Family.objects.get(pk=self.kwargs.get(self.pk_url_kwarg, None))
        return context

    def get_success_url(self):
        return reverse('family_detail', kwargs={'pk': self.kwargs.get(self.pk_url_kwarg, None)})


class ChildUpdateView(LoginRequiredMixin, UpdateView):
    model = Child
    template_name = 'people/child_update.html'
    form_class = ChildForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        language_form = LanguageFormSet(instance=self.object)
        language_helper = LanguageFormSetHelper()
        return self.render_to_response(
            self.get_context_data(form=form, language_form=language_form, language_helper=language_helper))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        language_form = LanguageFormSet(request.POST, instance=self.object)
        language_helper = LanguageFormSetHelper()
        if form.is_valid() and language_form.is_valid():
            return self.form_valid(form, language_form)
        else:
            return self.form_invalid(form, language_form, language_helper)

    def form_valid(self, form, language_form):
        self.object = form.save()
        language_form.instance = self.object
        language_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, language_form, language_helper):
        return self.render_to_response(self.get_context_data(form=form, language_form=language_form, language_helper=language_helper))

    def get_initial(self):
        initial_data = super(ChildUpdateView, self).get_initial()
        initial_data['child_id'] = self.object.id
        initial_data['age'] = self.object.age
        return initial_data

    def get_context_data(self, **kwargs):
        context = super(ChildUpdateView, self).get_context_data(**kwargs)
        context['form'].helper['child_id'].update_attributes(disabled='disabled')
        context['form'].helper.form_tag = False
        context['form'].helper.layout.pop(4)
        context['family'] = self.object.family
        context['media'] = ChildForm().media
        return context


ParentFormSet = inlineformset_factory(Family, Parent, extra=2, can_delete=True, fields=('name_first_text', 'name_last_text', 'guardian_type',))#, form=ParentForm)
ChildFormSet = inlineformset_factory(Family, Child, extra=2, can_delete=True, fields=('name_first_text', 'name_last_text', 'gender_type', 'dob_date',))#, form=ChildForm)


class FamilyCreateView(LoginRequiredMixin, CreateView):
    model = Family
    template_name = 'people/family_add.html'
    form_class = FamilyForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        parent_form = ParentFormSet()
        child_form = ChildFormSet()
        parent_helper = ParentFormSetHelper()
        child_helper = ChildFormSetHelper()
        return self.render_to_response(
            self.get_context_data(form=form, parent_form=parent_form, parent_helper=parent_helper, child_form=child_form, child_helper=child_helper))

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        parent_form = ParentFormSet(request.POST)
        child_form = ChildFormSet(request.POST)
        parent_helper = ParentFormSetHelper()
        child_helper = ChildFormSetHelper()

        if form.is_valid() and parent_form.is_valid() and child_form.is_valid():
            return self.form_valid(form, parent_form, child_form)
        else:
            return self.form_invalid(form, parent_form, child_form, parent_helper, child_helper)

    def form_valid(self, form, parent_form, child_form):
        self.object = form.save()

        parent_form.instance = self.object
        #if no last name is filled in for parent, default to family name
        parent_obj = parent_form.save(commit=False)

        for parent in parent_obj:
            if not parent.name_last_text:
                parent.name_last_text = form.cleaned_data['name_text']
            parent.save()
        

        child_form.instance = self.object
        #if no last name is filled in for child, default to family name
        child_obj = child_form.save(commit=False)

        for child in child_obj:
            if not child.name_last_text:
                child.name_last_text = form.cleaned_data['name_text']
            child.save()

        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, parent_form, child_form, parent_helper, child_helper):
        return self.render_to_response(self.get_context_data(form=form, parent_form=parent_form, child_form=child_form, parent_helper=parent_helper, child_helper=child_helper))

    def get_context_data(self, **kwargs):
        context = super(FamilyCreateView, self).get_context_data(**kwargs)
        context['media'] = ChildForm().media
        return context


class FamilyUpdateView(LoginRequiredMixin, UpdateView):
    model = Family
    template_name = 'people/family_update.html'
    form_class = FamilyForm

    def get(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        parent_form = ParentFormSet(instance=self.object)
        parent_helper = ParentFormSetHelper()
        child_form = ChildFormSet(instance=self.object)
        child_helper = ChildFormSetHelper()
        return self.render_to_response(
            self.get_context_data(form=form, parent_form=parent_form, parent_helper=parent_helper, child_form=child_form, child_helper=child_helper))

    def post(self, request, *args, **kwargs):
        self.object = self.get_object()
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        parent_form = ParentFormSet(request.POST, instance=self.object)
        child_form = ChildFormSet(request.POST, instance=self.object)
        parent_helper = ParentFormSetHelper()
        child_helper = ChildFormSetHelper()
        if form.is_valid() and parent_form.is_valid() and child_form.is_valid():
            return self.form_valid(form, parent_form, child_form)
        else:
            return self.form_invalid(form, parent_form, child_form, parent_helper, child_helper)

    def form_valid(self, form, parent_form, child_form):
        self.object = form.save()
        parent_form.instance = self.object
        parent_form.save()
        child_form.instance = self.object
        child_form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form, parent_form, child_form, parent_helper, child_helper):
        return self.render_to_response(self.get_context_data(form=form, parent_form=parent_form, child_form=child_form, parent_helper=parent_helper, child_helper=child_helper))

    def get_context_data(self, **kwargs):
        context = super(FamilyUpdateView, self).get_context_data(**kwargs)
        context['media'] = ChildForm().media
        return context

