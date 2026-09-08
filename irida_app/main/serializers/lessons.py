"""
Сериализатори за урок/занятие: темите, точките от плана,
бележките и задачите.
"""

from rest_framework import serializers

from ..models import (
    Session,
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


class SessionReadSerializer(serializers.ModelSerializer):
    session_topics = SessionTopicReadSerializer(many=True, read_only=True)

    class Meta:
        model = Session
        fields = ['id', 'course', 'num', 'name', 'focus', 'goals', 'duration', 'session_type', 'basic_level', 'collapsed', 'session_topics']


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
