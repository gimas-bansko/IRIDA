"""
Сериализатори за урок/занятие: темите, точките от плана,
бележките и задачите.
"""

import os
from rest_framework import serializers

from ..constants import SUPERADMIN, GUESTADMIN, SCHOOLADMIN, TEACHER, STUDENT
from ..models import (
    Session,
    SessionAttachment,
    SessionNote,
    SessionPoint,
    SessionTask,
    SessionTopic,
)
from .curriculum import TopicSerializer


def get_author_name_display(author):
    if not author:
        return 'Анонимен автор'
    first = getattr(author, 'first_name', '')
    last = getattr(author, 'last_name', '')
    full_name = f"{first} {last}".strip()
    return full_name if full_name else author.username


def check_user_can_edit(request, obj):
    if not request or not getattr(request, 'user', None) or not request.user.is_authenticated:
        return False
    user = request.user
    if user.is_superuser:
        return True
    user_profile = getattr(user, 'userprofile', None)
    role = getattr(user_profile, 'access_level', None)
    if role in [SUPERADMIN, GUESTADMIN, SCHOOLADMIN]:
        return True
    author_id = getattr(obj, 'author_id', None)
    if author_id is not None:
        return author_id == user.id
    # Ако няма зададен автор, всеки аутентикиран потребител може да редактира и да придобие авторство
    return True


class SessionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = [
            'id', 'course', 'num', 'name', 'focus', 'goals', 'social_emotional_goals',
            'duration', 'session_type', 'basic_level', 'collapsed', 'author'
        ]
        extra_kwargs = {
            'author': {'required': False, 'allow_null': True}
        }


class SessionMiniSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField(read_only=True)
    is_author = serializers.SerializerMethodField(read_only=True)
    can_edit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Session
        fields = (
            'id', 'num', 'name', 'focus', 'goals', 'social_emotional_goals',
            'duration', 'session_type', 'basic_level', 'author', 'author_name',
            'is_author', 'can_edit'
        )

    def get_author_name(self, obj):
        return get_author_name_display(obj.author)

    def get_is_author(self, obj):
        request = self.context.get('request')
        if not request or not getattr(request, 'user', None) or not request.user.is_authenticated:
            return False
        return obj.author_id == request.user.id

    def get_can_edit(self, obj):
        request = self.context.get('request')
        return check_user_can_edit(request, obj)


class SessionSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField(read_only=True)
    is_author = serializers.SerializerMethodField(read_only=True)
    can_edit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Session
        fields = ['id', 'num', 'name', 'author', 'author_name', 'is_author', 'can_edit']

    def get_author_name(self, obj):
        return get_author_name_display(obj.author)

    def get_is_author(self, obj):
        request = self.context.get('request')
        if not request or not getattr(request, 'user', None) or not request.user.is_authenticated:
            return False
        return obj.author_id == request.user.id

    def get_can_edit(self, obj):
        request = self.context.get('request')
        return check_user_can_edit(request, obj)


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
# SessionTopicsForSessionView го ползва по това име.
class SessionTopicReadSerializerDetailed(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True)

    class Meta:
        model = SessionTopic
        fields = ['id', 'description', 'topic', 'session']


# Занятие - точки от плана
class SessionPointSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField(read_only=True)
    is_author = serializers.SerializerMethodField(read_only=True)
    can_edit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SessionPoint
        fields = [
            'id', 'session', 'num', 'name', 'description', 'duration', 'content',
            'author', 'author_name', 'is_author', 'can_edit'
        ]
        extra_kwargs = {
            'author': {'required': False, 'allow_null': True}
        }

    def get_author_name(self, obj):
        return get_author_name_display(obj.author)

    def get_is_author(self, obj):
        request = self.context.get('request')
        if not request or not getattr(request, 'user', None) or not request.user.is_authenticated:
            return False
        return obj.author_id == request.user.id

    def get_can_edit(self, obj):
        request = self.context.get('request')
        return check_user_can_edit(request, obj)


class SessionNoteSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField(read_only=True)
    is_author = serializers.SerializerMethodField(read_only=True)
    can_edit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SessionNote
        fields = [
            'id', 'session', 'point', 'num', 'name', 'content',
            'author', 'author_name', 'is_author', 'can_edit'
        ]
        extra_kwargs = {
            'author': {'required': False, 'allow_null': True}
        }

    def get_author_name(self, obj):
        return get_author_name_display(obj.author)

    def get_is_author(self, obj):
        request = self.context.get('request')
        if not request or not getattr(request, 'user', None) or not request.user.is_authenticated:
            return False
        return obj.author_id == request.user.id

    def get_can_edit(self, obj):
        request = self.context.get('request')
        return check_user_can_edit(request, obj)


class SessionTaskSerializer(serializers.ModelSerializer):
    author_name = serializers.SerializerMethodField(read_only=True)
    is_author = serializers.SerializerMethodField(read_only=True)
    can_edit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SessionTask
        fields = [
            'id', 'session', 'point', 'num', 'name', 'condition', 'answer',
            'author', 'author_name', 'is_author', 'can_edit'
        ]
        extra_kwargs = {
            'author': {'required': False, 'allow_null': True}
        }

    def get_author_name(self, obj):
        return get_author_name_display(obj.author)

    def get_is_author(self, obj):
        request = self.context.get('request')
        if not request or not getattr(request, 'user', None) or not request.user.is_authenticated:
            return False
        return obj.author_id == request.user.id

    def get_can_edit(self, obj):
        request = self.context.get('request')
        return check_user_can_edit(request, obj)


class SessionAttachmentSerializer(serializers.ModelSerializer):
    file_url = serializers.SerializerMethodField(read_only=True)
    file_name = serializers.SerializerMethodField(read_only=True)
    author_name = serializers.SerializerMethodField(read_only=True)
    is_author = serializers.SerializerMethodField(read_only=True)
    can_edit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = SessionAttachment
        fields = [
            'id', 'session', 'point', 'num', 'name', 'attachment_type', 'is_student_visible',
            'file', 'file_url', 'file_name', 'original_filename', 'description',
            'author', 'author_name', 'is_author', 'can_edit'
        ]
        extra_kwargs = {
            'file': {'required': False, 'allow_null': True},
            'author': {'required': False, 'allow_null': True}
        }

    def get_file_url(self, obj):
        if obj.file:
            try:
                return obj.file.url
            except Exception:
                return None
        return None

    def get_file_name(self, obj):
        if obj.original_filename:
            return obj.original_filename
        if obj.file:
            return os.path.basename(obj.file.name)
        return ''

    def get_author_name(self, obj):
        return get_author_name_display(obj.author)

    def get_is_author(self, obj):
        request = self.context.get('request')
        if not request or not getattr(request, 'user', None) or not request.user.is_authenticated:
            return False
        return obj.author_id == request.user.id

    def get_can_edit(self, obj):
        request = self.context.get('request')
        return check_user_can_edit(request, obj)


class SessionReadSerializer(serializers.ModelSerializer):
    session_topics = SessionTopicReadSerializer(many=True, read_only=True)
    session_tasks = SessionTaskSerializer(many=True, read_only=True)
    session_attachments = SessionAttachmentSerializer(many=True, read_only=True)
    session_points = SessionPointSerializer(many=True, read_only=True)
    author_name = serializers.SerializerMethodField(read_only=True)
    is_author = serializers.SerializerMethodField(read_only=True)
    can_edit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Session
        fields = [
            'id', 'course', 'num', 'name', 'focus', 'goals', 'social_emotional_goals', 'duration',
            'session_type', 'basic_level', 'collapsed', 'author', 'author_name', 'is_author', 'can_edit',
            'session_topics', 'session_tasks', 'session_attachments', 'session_points'
        ]

    def get_author_name(self, obj):
        return get_author_name_display(obj.author)

    def get_is_author(self, obj):
        request = self.context.get('request')
        if not request or not getattr(request, 'user', None) or not request.user.is_authenticated:
            return False
        return obj.author_id == request.user.id

    def get_can_edit(self, obj):
        request = self.context.get('request')
        return check_user_can_edit(request, obj)
