import requests
from decimal import Decimal
from django.conf import settings
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import SettlementLog


def fetch_bill(bill_id):
    response = requests.get(
        f'{settings.BILL_SERVICE_URL}/api/bills/{bill_id}/internal',
        timeout=10,
    )
    if response.status_code != 200:
        return None
    return response.json()


def fetch_group_members(group_id, auth_header):
    response = requests.get(
        f'{settings.GROUP_SERVICE_URL}/api/groups/{group_id}/members',
        headers={'Authorization': auth_header},
        timeout=10,
    )
    if response.status_code != 200:
        return []
    return response.json()


def calculate_settlement(bill_data, members):
    payer_id = bill_data['created_by']
    payer_name = bill_data.get('created_by_username', f'User {payer_id}')

    member_map = {m['user_id']: m.get('username', f'User {m["user_id"]}') for m in members}
    if payer_id not in member_map:
        member_map[payer_id] = payer_name

    user_debts = {}

    for item in bill_data.get('items', []):
        price = Decimal(str(item['price']))
        consumers = item.get('consumed_by_user_ids', [])
        if not consumers:
            continue
        share = price / len(consumers)
        for user_id in consumers:
            uid = int(user_id)
            if uid == payer_id:
                continue
            user_debts[uid] = user_debts.get(uid, Decimal('0')) + share

    settlements = []
    per_user = []
    total_debt = Decimal('0')

    for user_id, amount in sorted(user_debts.items()):
        amount = amount.quantize(Decimal('0.01'))
        total_debt += amount
        from_name = member_map.get(user_id, f'User {user_id}')
        settlements.append({
            'from_user_id': user_id,
            'from_username': from_name,
            'to_user_id': payer_id,
            'to_username': member_map.get(payer_id, payer_name),
            'amount': float(amount),
            'description': f'{from_name} bayar {member_map.get(payer_id, payer_name)} Rp{amount:,.0f}'.replace(',', '.'),
        })
        per_user.append({
            'user_id': user_id,
            'username': from_name,
            'debt': float(amount),
        })

    return {
        'bill_id': bill_data['id'],
        'bill_title': bill_data['title'],
        'payer_id': payer_id,
        'payer_username': member_map.get(payer_id, payer_name),
        'total_amount': float(bill_data.get('total_amount', 0)),
        'total_debt': float(total_debt),
        'settlements': settlements,
        'per_user_debt': per_user,
    }


class SettlementView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, bill_id):
        bill_data = fetch_bill(bill_id)
        if not bill_data:
            return Response({'error': 'Tagihan tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)

        auth_header = request.headers.get('Authorization', '')
        members = fetch_group_members(bill_data['group_id'], auth_header)

        result = calculate_settlement(bill_data, members)
        SettlementLog.objects.create(bill_id=bill_id, result=result)

        return Response(result)
