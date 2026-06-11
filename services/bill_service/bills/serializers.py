from rest_framework import serializers

from .models import Bill, BillItem


class BillItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = BillItem
        fields = ['id', 'bill', 'item_name', 'price', 'consumed_by_user_ids']
        read_only_fields = ['id', 'bill']


class BillSerializer(serializers.ModelSerializer):
    items = BillItemSerializer(many=True, read_only=True)

    class Meta:
        model = Bill
        fields = [
            'id', 'group_id', 'title', 'created_by', 'created_by_username',
            'total_amount', 'created_at', 'items',
        ]
        read_only_fields = ['id', 'created_at', 'total_amount']


class BillCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bill
        fields = ['group_id', 'title']
