"""
Сериализатори за урок/занятие: темите, точките от плана,
бележките и задачите.
"""

from rest_framework import serializers

from ..models import (
    Session,
    SessionAttachment,
    SessionNote,
    SessionPoint,
    SessionTask,
    SessionTopic,
)
from .curriculum import TopicSerializer


class SessionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'course', 'num', 'name', 'focus', 'goals', 'duration', 'session_type', 'basic_level', 'collapsed']


class SessionMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'num', 'name', 'focus', 'goals', 'duration', 'session_type', 'basic_level')


class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'num', 'name']


class SessionTopicWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionTopic
        fields = ['id', 'session', 'topic', 'description']


class SessionTopicReadSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True)

    class Meta:
        model = SessionTopic
        fields = ['id', 'description', 'topic', 'session']


# ВНИМАНИЕ: идентичен на SessionTopicReadSerializer. Пази се само защото
# SessionTopicsForSessionView го ползва по това име. При следващо минаване
# през views/api_lessons.py може да се обедини с горния.
class SessionTopicReadSerializerDetailed(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True)

    class Meta:
        model = SessionTopic
        fields = ['id', 'description', 'topic', 'session']


# Занятие - точки от плана
class SessionPointSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionPoint
        fields = ['id','session', 'num',  'name', 'description', 'duration', 'content']


class SessionNoteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionNote
        fields = ['id', 'session', 'point', 'num', 'name', 'content']


class SessionTaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionTask
        fields = ['id', 'session', 'point', 'num', 'name', 'condition', 'answer']


import os


class SessionAttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField(read_only=True)
    file_name = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SessionAttachment
        fields = ['id', 'session', 'point', 'num', 'name', 'attachment_type', 'file', 'file_url', 'file_name', 'description']
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


class SessionReadSerializer(serializers.ModelSerializer):
    session_topics = SessionTopicReadSerializer(many=True, read_only=True)
    session_tasks = SessionTaskSerializer(many=True, read_only=True)
    session_attachments = SessionAttachmentSerializer(many=True, read_only=True)
    session_points = SessionPointSerializer(many=True, read_only=True)

    class Meta:
        model = Session
        fields = [
            'id', 'course', 'num', 'name', 'focus', 'goals', 'duration',
            'session_type', 'basic_level', 'collapsed',
            'session_topics', 'session_tasks', 'session_attachments', 'session_points'
        ]
