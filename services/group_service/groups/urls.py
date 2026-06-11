from django.urls import path

from .views import GroupListCreateView, GroupMemberView

urlpatterns = [
    path('groups', GroupListCreateView.as_view(), name='groups'),
    path('groups/<int:group_id>/members', GroupMemberView.as_view(), name='group-members'),
]
