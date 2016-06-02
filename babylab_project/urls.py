from django.conf.urls import patterns, include, url
from core.views import HomePageView, LoginForm, logout

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'babylab_project.views.home', name='home'),
    # url(r'^babylab_project/', include('babylab_project.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', HomePageView.as_view(), name='home'),
    url(r'^people/', include('people.urls')),
    url(r'^study/', include('study.urls')),
    url(r'^scheduling/', include('scheduling.urls')),
    url(r'^accounts/login/$', LoginForm.as_view(), name='login'),
    url(r'^accounts/logout/$', logout, name='logout'),
)
