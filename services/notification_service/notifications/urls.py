from django.urls import path

from .views import NotifyView, NotificationListView

urlpatterns = [
    path('notify', NotifyView.as_view(), name='notify'),
    path('notifications', NotificationListView.as_view(), name='notifications'),
]
