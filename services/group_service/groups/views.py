from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Group, GroupMember
from .serializers import GroupSerializer, GroupMemberSerializer, AddMemberSerializer


class GroupListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        groups = Group.objects.filter(members__user_id=request.user.id).distinct()
        return Response(GroupSerializer(groups, many=True).data)

    def post(self, request):
        name = request.data.get('name')
        if not name:
            return Response({'error': 'Nama grup wajib diisi'}, status=status.HTTP_400_BAD_REQUEST)
        group = Group.objects.create(name=name, created_by=request.user.id)
        GroupMember.objects.create(
            group=group,
            user_id=request.user.id,
            username=request.user.username,
        )
        return Response(GroupSerializer(group).data, status=status.HTTP_201_CREATED)


class GroupMemberView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, group_id):
        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return Response({'error': 'Grup tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)
        members = group.members.all()
        return Response(GroupMemberSerializer(members, many=True).data)

    def post(self, request, group_id):
        try:
            group = Group.objects.get(pk=group_id)
        except Group.DoesNotExist:
            return Response({'error': 'Grup tidak ditemukan'}, status=status.HTTP_404_NOT_FOUND)

        if group.created_by != request.user.id:
            return Response({'error': 'Hanya pembuat grup yang dapat menambah anggota'}, status=status.HTTP_403_FORBIDDEN)

        serializer = AddMemberSerializer(data=request.data)
        if not serializer.is_valid():
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        user_id = serializer.validated_data['user_id']
        username = serializer.validated_data.get('username', '')

        if GroupMember.objects.filter(group=group, user_id=user_id).exists():
            return Response({'error': 'Anggota sudah ada di grup'}, status=status.HTTP_400_BAD_REQUEST)

        member = GroupMember.objects.create(group=group, user_id=user_id, username=username)
        return Response(GroupMemberSerializer(member).data, status=status.HTTP_201_CREATED)
