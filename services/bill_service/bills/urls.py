from django.urls import path

from .views import BillListCreateView, BillDetailView, BillDetailPublicView, BillItemCreateView

urlpatterns = [
    path('bills', BillListCreateView.as_view(), name='bills'),
    path('bills/<int:bill_id>', BillDetailView.as_view(), name='bill-detail'),
    path('bills/<int:bill_id>/internal', BillDetailPublicView.as_view(), name='bill-detail-internal'),
    path('bills/<int:bill_id>/items', BillItemCreateView.as_view(), name='bill-items'),
]
