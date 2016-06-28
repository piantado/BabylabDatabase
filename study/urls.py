from django.conf.urls import url, patterns

from .views import StudyListView, StudyDetailView, SessionCreateView, SessionDetailView, SessionUpdateView, SessionListView, SessionNoListView, SessionListAllView
urlpatterns = [
	url(r'^study/$', StudyListView.as_view(), name='study_list'),
    url(r'^study/(?P<pk>\d+)/$', StudyDetailView.as_view(), name='study_detail'),
    url(r'^session/$', SessionListAllView.as_view(), name='session_list_all'),
    url(r'^session/list/(?P<pk>\d+)/$', SessionListView.as_view(), name='session_list'),
    url(r'^session/nolist/(?P<pk>\d+)/$', SessionNoListView.as_view(), name='session_no_list'),
    url(r'^session/add/(?P<pk>\d+)/study/(?P<key>\d+)/$', SessionCreateView.as_view(), name='session_add'),
    url(r'^session/(?P<pk>\d+)$', SessionDetailView.as_view(), name='session_detail'),
    url(r'^session/update/(?P<pk>\d+)$', SessionUpdateView.as_view(), name='session_update'),
]