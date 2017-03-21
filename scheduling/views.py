from django.views.generic import CreateView, TemplateView, ListView, DetailView, UpdateView
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages

from braces.views import LoginRequiredMixin
from crispy_forms.bootstrap import UneditableField
from django_tables2.views import SingleTableMixin

from .models import Contact, Appointment
from .forms import ContactForm, AppointmentForm
from .tables import ContactTable, AppointmentTable

from people.models import Child, Family
from core.views import CreatedMixin

from rest_framework.views import APIView
from rest_framework.response import Response


from .serializers import AppointmentSerializer

class ContactListView(LoginRequiredMixin, SingleTableMixin, ListView):
    model = Contact
    template_name = 'scheduling/contact_list.html'
    table_class = ContactTable
    table_pagination = False


class ContactCreateView(LoginRequiredMixin, CreateView):
    model = Contact
    template_name = 'scheduling/contact_add.html'
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        context = super(ContactCreateView, self).get_context_data(**kwargs)
        context['media'] = ContactForm().media
        context['child'] = Child.objects.get(pk=self.kwargs.get(self.pk_url_kwarg, None))
        context['family'] = context['child'].family
        return context

    def get_initial(self):
        initial = super(ContactCreateView, self).get_initial()
        initial['child'] = self.kwargs.get(self.pk_url_kwarg, None)
        initial['staff'] = self.request.user
        return initial

    def form_valid(self, form):

        if form.cleaned_data['contact_result_type'] == 0:
            super(ContactCreateView, self).form_valid(form)
            return HttpResponseRedirect(reverse('appointment_add', kwargs={'pk': form.cleaned_data['child'].id}))
        else:
            return super(ContactCreateView, self).form_valid(form)


class ContactUpdateView(LoginRequiredMixin, UpdateView):
    model = Contact
    template_name = 'scheduling/contact_update.html'
    form_class = ContactForm

    def get_context_data(self, **kwargs):
        context = super(ContactUpdateView, self).get_context_data(**kwargs)
        context['media'] = ContactForm().media
        context['child'] = Child.objects.get(pk=self.object.child.id)
        context['family'] = context['child'].family
        return context

    def form_valid(self, form):

        if form.cleaned_data['contact_result_type'] == 0:
            super(ContactUpdateView, self).form_valid(form)
            return HttpResponseRedirect(reverse('appointment_add', kwargs={'pk': form.cleaned_data['child'].id}))
        else:
            return super(ContactUpdateView, self).form_valid(form)


class ContactDetailView(LoginRequiredMixin, CreatedMixin, DetailView):
    model = Contact
    template_name = 'scheduling/contact_detail.html'

    def get_context_data(self, **kwargs):
        context = super(ContactDetailView, self).get_context_data(**kwargs)
        form = ContactForm(instance=self.object)
        form.helper.layout.pop(1)
        form.helper.filter(basestring, max_level=1).wrap(UneditableField)
        form.helper.form_tag = False
        context['form'] = form
        context['media'] = AppointmentForm().media
        context['child'] = Child.objects.get(pk=self.object.child.id)
        context['family'] = context['child'].family
        return context


class AppointmentListView(LoginRequiredMixin, SingleTableMixin, ListView):
    model = Appointment
    template_name = 'scheduling/appointment_list.html'
    table_class = AppointmentTable
    table_pagination = False


class AppointmentCreateView(LoginRequiredMixin, CreateView):
    model = Appointment
    template_name = 'scheduling/appointment_add.html'
    form_class = AppointmentForm

    def get_context_data(self, **kwargs):
        context = super(AppointmentCreateView, self).get_context_data(**kwargs)
        context['media'] = AppointmentForm().media
        context['child'] = Child.objects.get(pk=self.kwargs.get(self.pk_url_kwarg, None))
        context['family'] = context['child'].family
        return context

    def get_initial(self):
        initial = super(AppointmentCreateView, self).get_initial()
        initial['child'] = self.kwargs.get(self.pk_url_kwarg, None)
        initial['status_type'] = 4
        return initial

    def form_valid(self, form):

        if form.cleaned_data['status_type'] == 0:
            super(AppointmentCreateView, self).form_valid(form)
            from study.models import Session
            if Session.objects.filter(child=form.cleaned_data['child'].id, study=form.cleaned_data['study'].id).exists():
                session = Session.objects.get(child=form.cleaned_data['child'].id, study=form.cleaned_data['study'].id)
                return HttpResponseRedirect(reverse('session_update', kwargs={'pk': session.pk}))
            else:
                return HttpResponseRedirect(reverse('session_add', kwargs={'pk': form.cleaned_data['child'].id, 'key': form.cleaned_data['study'].id}))
        else:
            super(AppointmentCreateView, self).form_valid(form)
            return HttpResponseRedirect(reverse('child_detail', kwargs={'pk': form.cleaned_data['child'].id}))


class AppointmentUpdateView(LoginRequiredMixin, UpdateView):
    model = Appointment
    template_name = 'scheduling/appointment_update.html'
    form_class = AppointmentForm

    def get_context_data(self, **kwargs):
        context = super(AppointmentUpdateView, self).get_context_data(**kwargs)
        context['media'] = AppointmentForm().media
        context['child'] = Child.objects.get(pk=self.object.child.id)
        context['family'] = context['child'].family
        return context

    def form_valid(self, form):

        if form.cleaned_data['status_type'] == 0:
            super(AppointmentUpdateView, self).form_valid(form)
            from study.models import Session
            if Session.objects.filter(child=form.cleaned_data['child'].id, study=form.cleaned_data['study'].id).exists():
                session = Session.objects.get(child=form.cleaned_data['child'].id, study=form.cleaned_data['study'].id)
                return HttpResponseRedirect(reverse('session_update', kwargs={'pk': session.pk}))
            else:
                return HttpResponseRedirect(reverse('session_add', kwargs={'pk': form.cleaned_data['child'].id, 'key': form.cleaned_data['study'].id}))

        else:
            super(AppointmentUpdateView, self).form_valid(form)
            return HttpResponseRedirect(reverse('child_detail', kwargs={'pk': form.cleaned_data['child'].id}))


class AppointmentDetailView(LoginRequiredMixin, CreatedMixin, DetailView):
    model = Appointment
    template_name = 'scheduling/appointment_detail.html'

    def get_context_data(self, **kwargs):
        context = super(AppointmentDetailView, self).get_context_data(**kwargs)
        form = AppointmentForm(instance=self.object)
        form.helper.layout.pop(3)
        form.helper.filter(basestring, max_level=1).wrap(UneditableField)
        form.helper.form_tag = False
        context['form'] = form
        context['media'] = AppointmentForm().media
        context['child'] = Child.objects.get(pk=self.object.child.id)
        context['family'] = context['child'].family
        return context


class AppointmentCalendarView(LoginRequiredMixin, TemplateView):
    template_name = 'scheduling/appointment_calendar.html'


class AppointmentList(APIView):
    def get(self, request, format=None):
        appointments = Appointment.objects.all()
        serializer = AppointmentSerializer(appointments, many=True)
        results = {'success': 1, 'result': serializer.data}
        return Response(results)