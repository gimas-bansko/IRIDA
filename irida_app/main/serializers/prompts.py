"""
Сериализатори за AI промптове.
"""
from rest_framework import serializers

from ..models import AIPrompt


class AIPromptSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField(read_only=True)
    page_key_display = serializers.CharField(source='get_page_key_display', read_only=True)
    can_edit = serializers.SerializerMethodField(read_only=True)
    can_delete = serializers.SerializerMethodField(read_only=True)
    is_author = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AIPrompt
        fields = [
            'id',
            'title',
            'page_key',
            'page_key_display',
            'prompt_text',
            'instructions',
            'is_system',
            'order',
            'created_by',
            'created_by_name',
            'can_edit',
            'can_delete',
            'is_author',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

    def get_created_by_name(self, obj):
        if obj.is_system:
            return 'Системен'
        if obj.created_by:
            first = obj.created_by.first_name
            last = obj.created_by.last_name
            full_name = f"{first} {last}".strip()
            return full_name if full_name else obj.created_by.username
        return 'Анонимен'

    def get_is_author(self, obj):
        request = self.context.get('request')
        if not request or not getattr(request, 'user', None) or not request.user.is_authenticated:
            return False
        if obj.is_system:
            return False
        return obj.created_by_id == request.user.id

    def get_can_edit(self, obj):
        request = self.context.get('request')
        if not request or not getattr(request, 'user', None) or not request.user.is_authenticated:
            return False
        if obj.is_system:
            return False
        if obj.created_by_id == request.user.id:
            return True
        from ..permissions import is_admin_user
        return is_admin_user(request.user)

    def get_can_delete(self, obj):
        request = self.context.get('request')
        if not request or not getattr(request, 'user', None) or not request.user.is_authenticated:
            return False
        if obj.is_system:
            return False
        if obj.created_by_id == request.user.id:
            return True
        from ..permissions import is_admin_user
        return is_admin_user(request.user)
