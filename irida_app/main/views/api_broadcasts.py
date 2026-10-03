"""
API за броадкаст съобщения и известия към потребителите.
"""

from django.db.models import Q
from django.shortcuts import get_object_or_404
from django.utils import timezone
from rest_framework import generics, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..audit import log_audit_event
from ..constants import GUESTADMIN, SCHOOLADMIN, STUDENT, SUPERADMIN, TEACHER
from ..models import BroadcastMessage, BroadcastMessageRead
from ..permissions import is_admin_user
from ..serializers.broadcasts import BroadcastMessageSerializer


class BroadcastUnreadListView(APIView):
    """
    GET /api/broadcast-messages/unread/
    Връща списък с активни, неизтекли и непрочетени съобщения за текущия потребител
    в зависимост от неговата роля.
    """
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        now = timezone.now()

        # Базов queryset: активни и валидни (неизтекли)
        qs = BroadcastMessage.objects.filter(is_active=True).filter(
            Q(expires_at__isnull=True) | Q(expires_at__gte=now)
        )

        # Филтриране по роля
        user_profile = getattr(user, 'userprofile', None)
        role = getattr(user_profile, 'access_level', None)
        is_admin = is_admin_user(user)

        target_roles = [BroadcastMessage.AUDIENCE_ALL]
        if is_admin:
            target_roles.append(BroadcastMessage.AUDIENCE_ADMIN)
        if role == TEACHER or is_admin:
            target_roles.append(BroadcastMessage.AUDIENCE_TEACHER)
        if role == STUDENT:
            target_roles.append(BroadcastMessage.AUDIENCE_STUDENT)

        qs = qs.filter(target_role__in=target_roles)

        # Изключваме вече прочетените от този потребител
        read_message_ids = BroadcastMessageRead.objects.filter(user=user).values_list('message_id', flat=True)
        qs = qs.exclude(id__in=read_message_ids).order_by('-created_at', '-id')

        serializer = BroadcastMessageSerializer(qs, many=True, context={'request': request})
        return Response(serializer.data, status=status.HTTP_200_OK)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
def broadcast_mark_read(request, pk):
    """
    POST /api/broadcast-messages/<pk>/mark-read/
    Маркира дадено съобщение като прочетено за текущия потребител.
    """
    message = get_object_or_404(BroadcastMessage, id=pk)
    read_obj, created = BroadcastMessageRead.objects.get_or_create(
        message=message,
        user=request.user
    )
    return Response({
        'status': 'ok',
        'message_id': message.id,
        'read_at': read_obj.read_at
    }, status=status.HTTP_200_OK)


class BroadcastMessageListCreateView(generics.ListCreateAPIView):
    """
    GET /api/broadcast-messages/ - Списък на всички съобщения (за администратори)
    POST /api/broadcast-messages/ - Създаване на ново съобщение
    """
    permission_classes = [IsAuthenticated]
    serializer_class = BroadcastMessageSerializer

    def get_queryset(self):
        return BroadcastMessage.objects.all().order_by('-created_at', '-id')

    def perform_create(self, serializer):
        instance = serializer.save(created_by=self.request.user)
        log_audit_event(
            request=self.request,
            action="CREATE",
            target_model="BroadcastMessage",
            target_id=instance.id,
            status="SUCCESS",
            details=f"Created broadcast message '{instance.title}' (target_role: {instance.target_role})"
        )


class BroadcastMessageRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    """
    GET, PUT, PATCH, DELETE /api/broadcast-messages/<pk>/
    """
    permission_classes = [IsAuthenticated]
    queryset = BroadcastMessage.objects.all()
    serializer_class = BroadcastMessageSerializer

    def perform_update(self, serializer):
        instance = serializer.save()
        log_audit_event(
            request=self.request,
            action="UPDATE",
            target_model="BroadcastMessage",
            target_id=instance.id,
            status="SUCCESS",
            details=f"Updated broadcast message '{instance.title}'"
        )

    def perform_destroy(self, instance):
        msg_id = instance.id
        title = instance.title
        instance.delete()
        log_audit_event(
            request=self.request,
            action="DELETE",
            target_model="BroadcastMessage",
            target_id=msg_id,
            status="SUCCESS",
            details=f"Deleted broadcast message '{title}'"
        )
