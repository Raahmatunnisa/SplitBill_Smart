from rest_framework import status
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Notification
from .serializers import NotificationSerializer


class NotifyView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        user_ids = request.data.get('user_ids', [])
        message = request.data.get('message', '')

        if not user_ids or not message:
            return Response({'error': 'user_ids dan message wajib diisi'}, status=status.HTTP_400_BAD_REQUEST)

        created = []
        for uid in user_ids:
            notif = Notification.objects.create(user_id=int(uid), message=message)
            created.append(NotificationSerializer(notif).data)

        return Response({'notifications': created}, status=status.HTTP_201_CREATED)


class NotificationListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        notifications = Notification.objects.filter(user_id=request.user.id)
        return Response(NotificationSerializer(notifications, many=True).data)
