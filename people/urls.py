from django.conf.urls import url, patterns

from .views import FamilyCreateView, FamilyListView, FamilyDetailView, FamilyUpdateView, ParentListView, ParentUpdateView, ParentCreateView, ChildUpdateView, ChildCreateView, ChildListView, ChildDetailView, AddressUpdateView, ParentDetailView

urlpatterns = [
    url(r'^family/$', FamilyListView.as_view(), name='family_list'),
    url(r'^family/(?P<pk>\d+)/$', FamilyDetailView.as_view(), name='family_detail'),
    url(r'^family/address/(?P<pk>\d+)/$', AddressUpdateView.as_view(), name='address_update'),
    url(r'^family/update/(?P<pk>\d+)/$', FamilyUpdateView.as_view(), name='family_update'),
    url(r'^family/add/$', FamilyCreateView.as_view(), name='family_add'),
    url(r'^parent/$', ParentListView.as_view(), name='parent_list'),
    url(r'^parent/(?P<pk>\d+)/$', ParentDetailView.as_view(), name='parent_detail'),
    url(r'^parent/update/(?P<pk>\d+)/$', ParentUpdateView.as_view(), name='parent_update'),
    url(r'^parent/add/(?P<pk>\d+)$', ParentCreateView.as_view(), name='parent_add'),
    url(r'^child/update/(?P<pk>\d+)/$', ChildUpdateView.as_view(), name='child_update'),
    url(r'^child/add/(?P<pk>\d+)$', ChildCreateView.as_view(), name='child_add'),
    url(r'^child/$', ChildListView.as_view(), name='child_list'),
    url(r'^child/(?P<pk>\d+)/$', ChildDetailView.as_view(), name='child_detail'),
]