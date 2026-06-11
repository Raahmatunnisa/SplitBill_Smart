import requests
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Bill, BillItem
from .serializers import BillSerializer, BillCreateSerializer, BillItemSerializer


def notify_members(user_ids, message):
    try:
        requests.post(
            f'{settings.NOTIFICATION_SERVICE_URL}/api/notify',
            json={'user_ids': user_ids, 'message': message},
            timeout=5,
        )
    except requests.RequestException:
        pass


class BillListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        group_id = request.query_params.get('group_id')
        bills = Bill.objects.all().order_by('-created_at')
        if group_id:
            bills = bills.filter(group_id=group_id)
        return Response(BillSerializer(bills[:50], many=True).data)

    def post(self, request):
        serializer = BillCreateSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        bill = Bill.objects.create(
            group_id=serializer.validated_data['group_id'],
            title=serializer.validated_data['title'],
            created_by=request.user.id,
            created_by_username=request.user.username,
        )

        notify_members(
            [request.user.id],
            f'Tagihan baru "{bill.title}" telah dibuat.',
        )

        return Response(BillSerializer(bill).data, status=status.HTTP_201_CREATED)


class BillDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, bill_id):
        try:
            bill = Bill.objects.get(pk=bill_id)
        except Bill.DoesNotExist:
            return Response({'error': 'Tagihan tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
        return Response(BillSerializer(bill).data)


class BillDetailPublicView(APIView):
    permission_classes = [AllowAny]

    def get(self, request, bill_id):
        try:
            bill = Bill.objects.get(pk=bill_id)
        except Bill.DoesNotExist:
            return Response({'error': 'Tagihan tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
        return Response(BillSerializer(bill).data)


class BillItemCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, bill_id):
        try:
            bill = Bill.objects.get(pk=bill_id)
        except Bill.DoesNotExist:
            return Response({'error': 'Tagihan tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)

        item_name = request.data.get('item_name')
        price = request.data.get('price')
        consumed_by = request.data.get('consumed_by_user_ids', [])

        if not item_name or price is None:
            return Response({'error': 'item_name dan price wajib diisi'}, status=status.HTTP_400_BAD_REQUEST)

        item = BillItem.objects.create(
            bill=bill,
            item_name=item_name,
            price=price,
            consumed_by_user_ids=consumed_by,
        )
        bill.recalculate_total()

        all_user_ids = set()
        for bi in bill.items.all():
            all_user_ids.update(bi.consumed_by_user_ids)
        if all_user_ids:
            notify_members(
                list(all_user_ids),
                f'Item "{item_name}" ditambahkan ke tagihan "{bill.title}".',
            )

        return Response(BillItemSerializer(item).data, status=status.HTTP_201_CREATED)
