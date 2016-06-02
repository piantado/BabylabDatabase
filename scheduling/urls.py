from django.conf.urls import url, patterns, include

from .views import ContactListView, ContactCreateView, ContactUpdateView, AppointmentListView, AppointmentCreateView, AppointmentUpdateView, AppointmentDetailView, ContactDetailView, AppointmentCalendarView, AppointmentList



urlpatterns = patterns(
    '',
    url(r'^contact/$', ContactListView.as_view(), name='contact_list'),
    url(r'^contact/(?P<pk>\d+)$', ContactDetailView.as_view(), name='contact_detail'),
    url(r'^contact/add/(?P<pk>\d+)$', ContactCreateView.as_view(), name='contact_add'),
    url(r'^contact/update/(?P<pk>\d+)$', ContactUpdateView.as_view(), name='contact_update'),
    url(r'^appointment/$', AppointmentListView.as_view(), name='appointment_list'),
    url(r'^appointment/(?P<pk>\d+)$', AppointmentDetailView.as_view(), name='appointment_detail'),
    url(r'^appointment/add/(?P<pk>\d+)$', AppointmentCreateView.as_view(), name='appointment_add'),
    url(r'^appointment/update/(?P<pk>\d+)$', AppointmentUpdateView.as_view(), name='appointment_update'),
    url(r'^appointment/calendar/$', AppointmentCalendarView.as_view(), name='appointment_calendar'),
    url(r'^api/', AppointmentList.as_view(), name='api'),
)
