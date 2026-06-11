from rest_framework import serializers

from .models import Group, GroupMember


class GroupMemberSerializer(serializers.ModelSerializer):
    class Meta:
        model = GroupMember
        fields = ['id', 'group', 'user_id', 'username', 'joined_at']
        read_only_fields = ['id', 'joined_at']


class GroupSerializer(serializers.ModelSerializer):
    member_count = serializers.SerializerMethodField()

    class Meta:
        model = Group
        fields = ['id', 'name', 'created_by', 'created_at', 'member_count']
        read_only_fields = ['id', 'created_at']

    def get_member_count(self, obj):
        return obj.members.count()


class AddMemberSerializer(serializers.Serializer):
    user_id = serializers.IntegerField()
    username = serializers.CharField(required=False, allow_blank=True, default='')
