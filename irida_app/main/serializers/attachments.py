"""
Сериализатори за глобални приложения / файлове.
"""

import os
from rest_framework import serializers

from ..models import AppAttachment


class AppAttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField(read_only=True)
    file_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = AppAttachment
        fields = ['id', 'num', 'name', 'file', 'file_url', 'file_name', 'description', 'created_at', 'updated_at']
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
