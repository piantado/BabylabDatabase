from django.views.generic import CreateView, ListView, DetailView, UpdateView
from django.core.urlresolvers import reverse_lazy, reverse
from django.shortcuts import get_object_or_404
from django.http import HttpResponseRedirect

from braces.views import LoginRequiredMixin
from crispy_forms.bootstrap import UneditableField
from django_tables2.views import SingleTableMixin, RequestConfig

from .models import Study, Session
from .forms import StudyForm, SessionForm
from .tables import StudyTable, SessionTable, NoSessionTable, SessionListTable

from people.models import Child, Family
from core.views import CreatedMixin
from core.models import Disability

import json


class StudyListView(LoginRequiredMixin, SingleTableMixin, ListView):
    model = Study
    template_name = 'study/study_list.html'
    context_object_name = 'study_list'
    table_class = StudyTable


class StudyDetailView(LoginRequiredMixin, DetailView):
    model = Study
    template_name = 'study/study_detail.html'

    def get_context_data(self, **kwargs):
        context = super(StudyDetailView, self).get_context_data(**kwargs)
        form = StudyForm(instance=self.object)
        # form.helper.layout.pop(1)
        form.helper.filter(basestring, max_level=1).wrap(UneditableField)
        # form.helper.form_tag = False
        context['form'] = form
        return context

class StudyCreateView(LoginRequiredMixin, CreateView):
    model = Study
    template_name = 'study/study_add.html'
    form_class = StudyForm

    def get(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        return self.render_to_response(
            self.get_context_data(form=form))


    def get_context_data(self, **kwargs):
        context = super(StudyCreateView, self).get_context_data(**kwargs)
        context['media'] = StudyForm().media
        print "got context data"
        return context

    def post(self, request, *args, **kwargs):
        self.object = None
        form_class = self.get_form_class()
        form = self.get_form(form_class)
        if form.is_valid():
            return self.form_valid(form)
        else:
            return self.form_invalid(form)

    def form_valid(self, form):
        self.object = form.save()
        return HttpResponseRedirect(self.get_success_url())

    def form_invalid(self, form):
        return self.render_to_response(self.get_context_data(form=form))

    def get_success_url(self):
        return reverse('study_list')

class StudyUpdateView(LoginRequiredMixin, UpdateView):
    model = Study
    template_name = 'study/study_update.html'
    form_class = StudyForm

    def get_context_data(self, **kwargs):
        context = super(StudyUpdateView, self).get_context_data(**kwargs)
        context['media'] = StudyForm().media
        return context


class SessionListAllView(LoginRequiredMixin, SingleTableMixin, ListView):
    model = Study
    template_name = 'study/session_list_all.html'
    table_class = SessionListTable


class SessionCreateView(LoginRequiredMixin, CreateView):
    model = Session
    template_name = 'study/session_add.html'
    form_class = SessionForm

    def get_initial(self):
        initial = super(SessionCreateView, self).get_initial()
        initial['child'] = self.kwargs.get(self.pk_url_kwarg, None)
        initial['study'] = self.kwargs.get('key', None)
        return initial

    def get_context_data(self, **kwargs):
        context = super(SessionCreateView, self).get_context_data(**kwargs)
        context['media'] = SessionForm().media
        context['child'] = Child.objects.get(pk=self.kwargs.get(self.pk_url_kwarg, None))
        context['family'] = context['child'].family
        context['study'] = Study.objects.get(pk=self.kwargs.get('key', None))
        return context


class SessionDetailView(LoginRequiredMixin, CreatedMixin, DetailView):
    model = Session
    template_name = 'study/session_detail.html'

    def get_context_data(self, **kwargs):
        context = super(SessionDetailView, self).get_context_data(**kwargs)
        form = SessionForm(instance=self.object)
        form.helper.layout.pop(1)
        form.helper.filter(basestring, max_level=1).wrap(UneditableField)
        form.helper.form_tag = False
        context['form'] = form
        context['media'] = SessionForm().media
        context['child'] = self.object.child
        context['family'] = context['child'].family
        return context


class SessionUpdateView(LoginRequiredMixin, UpdateView):
    model = Session
    template_name = 'study/session_update.html'
    form_class = SessionForm

    def get_context_data(self, **kwargs):
        context = super(SessionUpdateView, self).get_context_data(**kwargs)
        context['media'] = SessionForm().media
        context['child'] = self.object.child
        context['family'] = context['child'].family
        return context


class SessionListView(LoginRequiredMixin, ListView):
    model = Session
    template_name = 'study/session_list.html'
    context_object_name = 'session_list'

    def get_queryset(self):
        self.study = get_object_or_404(Study, id=self.kwargs.get('pk', None))
        return Session.objects.filter(study=self.study)

    def get_context_data(self, **kwargs):
        context = super(SessionListView, self).get_context_data(**kwargs)
        context['session_table'] = SessionTable(Study.session_taken(self.study), prefix='1-')
        RequestConfig(self.request).configure(context['session_table'])
        context['study'] = self.study
        return context


class SessionNoListView(LoginRequiredMixin, ListView):
    model = Session
    template_name = 'study/session_no_list.html'
    context_object_name = 'session_no_list'

    def get_queryset(self):
        self.study = get_object_or_404(Study, id=self.kwargs.get('pk', None))
        return Session.objects.filter(study=self.study)

    def get_context_data(self, **kwargs):
        context = super(SessionNoListView, self).get_context_data(**kwargs)
        context['session_table'] = NoSessionTable(Study.session_not_taken(self.study), prefix='1-')
        RequestConfig(self.request).configure(context['session_table'])
        context['study'] = self.study
        context['all_disabilities'] = Disability.objects.all()
        return context