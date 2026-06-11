from django.urls import path, re_path

from .views import (
    auth_proxy,
    groups_proxy,
    bills_proxy,
    settlement_proxy,
    receipt_proxy,
    notifications_proxy,
)

urlpatterns = [
    path('auth/register', auth_proxy, {'path': 'register'}),
    path('auth/login', auth_proxy, {'path': 'login'}),
    path('auth/profile', auth_proxy, {'path': 'profile'}),
    re_path(r'^auth/?(?P<path>.*)$', auth_proxy),
    path('groups', groups_proxy),
    re_path(r'^groups/(?P<path>.+)$', groups_proxy),
    path('bills', bills_proxy),
    re_path(r'^bills/(?P<path>.+)$', bills_proxy),
    re_path(r'^settlement/(?P<path>.+)$', settlement_proxy),
    path('receipt/upload', receipt_proxy, {'path': 'upload'}),
    re_path(r'^receipt/(?P<path>.*)$', receipt_proxy),
    path('notifications', notifications_proxy),
    path('notify', notifications_proxy, {'path': 'notify'}),
    re_path(r'^notifications/(?P<path>.*)$', notifications_proxy),
]
