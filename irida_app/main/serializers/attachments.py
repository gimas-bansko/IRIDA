"""
Сериализатори за глобални приложения / файлове.
"""

import os
from rest_framework import serializers

from ..models import AppAttachment


class AppAttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField(read_only=True)
    file_name = serializers.SerializerMethodField(read_only=True)
    created_by_name = serializers.SerializerMethodField(read_only=True)
    is_owner = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AppAttachment
        fields = [
            'id',
            'num',
            'name',
            'file',
            'file_url',
            'file_name',
            'description',
            'is_system',
            'created_by',
            'created_by_name',
            'is_owner',
            'created_at',
            'updated_at',
        ]
        read_only_fields = ['id', 'created_at', 'updated_at', 'created_by']
        extra_kwargs = {
            'file': {'required': False, 'allow_null': True}
        }

    def get_file_url(self, obj):
        if obj.file:
            try:
                return obj.file.url
            except Exception:
                return None
        return None

    def get_file_name(self, obj):
        if obj.file:
            return os.path.basename(obj.file.name)
        return ''

    def get_created_by_name(self, obj):
        if obj.created_by:
            first = obj.created_by.first_name
            last = obj.created_by.last_name
            full_name = f"{first} {last}".strip()
            return full_name if full_name else obj.created_by.username
        return 'Системен' if obj.is_system else ''

    def get_is_owner(self, obj):
        request = self.context.get('request')
        if not request or not getattr(request, 'user', None) or not request.user.is_authenticated:
            return False
        return obj.created_by_id == request.user.id
