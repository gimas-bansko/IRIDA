"""
Сериализатори за броадкаст съобщения и известия.
"""

from rest_framework import serializers

from ..models import BroadcastMessage, BroadcastMessageRead


class BroadcastMessageSerializer(serializers.ModelSerializer):
    target_role_display = serializers.CharField(source='get_target_role_display', read_only=True)
    created_by_name = serializers.SerializerMethodField(read_only=True)
    is_read = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = BroadcastMessage
        fields = [
            'id',
            'title',
            'message',
            'target_role',
            'target_role_display',
            'is_active',
            'created_by',
            'created_by_name',
            'created_at',
            'expires_at',
            'is_read',
        ]
        read_only_fields = ['id', 'created_at', 'created_by']

    def get_created_by_name(self, obj):
        if obj.created_by:
            first = getattr(obj.created_by, 'first_name', '')
            last = getattr(obj.created_by, 'last_name', '')
            full = f"{first} {last}".strip()
            return full if full else obj.created_by.username
        return 'Системен администратор'

    def get_is_read(self, obj):
        request = self.context.get('request')
        if not request or not getattr(request, 'user', None) or not request.user.is_authenticated:
            return False
        return BroadcastMessageRead.objects.filter(message=obj, user=request.user).exists()


class BroadcastMessageReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BroadcastMessageRead
        fields = ['id', 'message', 'user', 'read_at']
        read_only_fields = ['id', 'read_at', 'user']
