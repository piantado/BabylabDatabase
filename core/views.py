from django.contrib.auth import (login as auth_login, logout as auth_logout)
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import FormView, TemplateView

from braces.views import LoginRequiredMixin

from .forms import AccountLogin


class CreatedMixin(object):
    def get_context_data(self, **kwargs):
        context = super(CreatedMixin, self).get_context_data(**kwargs)
        context['created'] = self.object.created
        context['created_by'] = self.object.created_by
        context['modified'] = self.object.modified
        context['modified_by'] = self.object.modified_by
        return context


class LoginForm(FormView):
    template_name = 'core/account_login.html'
    form_class = AccountLogin

    def form_valid(self, form):
        authenticated_user = form.save()
        auth_login(self.request, authenticated_user)
        return super(LoginForm, self).form_valid(form)

    def get_success_url(self):
        return reverse('home')


def logout(request):
    auth_logout(request)
    return HttpResponseRedirect(reverse('login'))


class HomePageView(LoginRequiredMixin, TemplateView):
    template_name = 'home.html'