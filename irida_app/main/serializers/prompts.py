"""
Сериализатори за AI промптове.
"""
from rest_framework import serializers

from ..models import AIPrompt


class AIPromptSerializer(serializers.ModelSerializer):
    created_by_name = serializers.SerializerMethodField(read_only=True)
    page_key_display = serializers.CharField(source='get_page_key_display', read_only=True)

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
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']

    def get_created_by_name(self, obj):
        if obj.created_by:
            first = obj.created_by.first_name
            last = obj.created_by.last_name
            full_name = f"{first} {last}".strip()
            return full_name if full_name else obj.created_by.username
        return 'Системен' if obj.is_system else ''
