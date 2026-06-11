from django.urls import path

from .views import SettlementView

urlpatterns = [
    path('settlement/<int:bill_id>', SettlementView.as_view(), name='settlement'),
]
