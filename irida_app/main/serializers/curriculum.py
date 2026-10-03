"""
Сериализатори за учебната програма: предмет, раздели, теми, цели.
"""

from rest_framework import serializers

from ..constants import SUPERADMIN, GUESTADMIN, SCHOOLADMIN, TEACHER, STUDENT
from ..models import Goal, Subject, Topic, Unit


def get_user_display_name(user):
    if not user:
        return 'Анонимен автор'
    first = getattr(user, 'first_name', '')
    last = getattr(user, 'last_name', '')
    full_name = f"{first} {last}".strip()
    return full_name if full_name else user.username


def check_subject_can_edit(request, obj):
    if not request or not getattr(request, 'user', None) or not request.user.is_authenticated:
        return False
    user = request.user
    if user.is_superuser:
        return True
    user_profile = getattr(user, 'userprofile', None)
    role = getattr(user_profile, 'access_level', None)
    if role in [SUPERADMIN, GUESTADMIN, SCHOOLADMIN]:
        return True
    if getattr(obj, 'creator_id', None) is not None:
        return obj.creator_id == user.id
    return True


class SubjectSerializer(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField(read_only=True)
    is_author = serializers.SerializerMethodField(read_only=True)
    can_edit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subject
        fields = [
            'id',
            'name',
            'grade',
            'subject_type',
            'hpy',
            'wpy',
            'hpw1',
            'hpw2',
            'creator',
            'creator_name',
            'is_author',
            'can_edit',
        ]
        extra_kwargs = {
            'creator': {'required': False, 'allow_null': True}
        }

    def get_creator_name(self, obj):
        return get_user_display_name(obj.creator)

    def get_is_author(self, obj):
        request = self.context.get('request')
        if not request or not getattr(request, 'user', None) or not request.user.is_authenticated:
            return False
        return obj.creator_id == request.user.id

    def get_can_edit(self, obj):
        request = self.context.get('request')
        return check_subject_can_edit(request, obj)


class SubjectMiniSerializer(serializers.ModelSerializer):
    creator_name = serializers.SerializerMethodField(read_only=True)
    is_author = serializers.SerializerMethodField(read_only=True)
    can_edit = serializers.SerializerMethodField(read_only=True)

    class Meta:
        model = Subject
        fields = ('id', 'name', 'grade', 'subject_type', 'creator', 'creator_name', 'is_author', 'can_edit')

    def get_creator_name(self, obj):
        return get_user_display_name(obj.creator)

    def get_is_author(self, obj):
        request = self.context.get('request')
        if not request or not getattr(request, 'user', None) or not request.user.is_authenticated:
            return False
        return obj.creator_id == request.user.id

    def get_can_edit(self, obj):
        request = self.context.get('request')
        return check_subject_can_edit(request, obj)


#   Цели за предмет
class GoalSerializer(serializers.ModelSerializer):
    class Meta:
        model = Goal
        fields = ['id', 'num', 'name', 'course']
        read_only_fields = ['id']


# Раздели и теми
class TopicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Topic
        fields = ['id', 'num', 'name', 'MoSCoW_cat', 'MoSCoW_rem']


class UnitSerializer(serializers.ModelSerializer):
    # вложени теми
    topics = TopicSerializer(source='unit_topic', many=True, read_only=True)

    class Meta:
        model = Unit
        fields = ['id', 'num', 'name', 'hours', 'topics']


class UnitWriteSerializer(serializers.ModelSerializer):
    # subject се подава като ID
    subject = serializers.PrimaryKeyRelatedField(queryset=Subject.objects.all())

    class Meta:
        model = Unit
        fields = ['id', 'num', 'name', 'hours', 'subject']
        read_only_fields = ['id']


class TopicWriteSerializer(serializers.ModelSerializer):
    # unit се подава като ID
    unit = serializers.PrimaryKeyRelatedField(queryset=Unit.objects.all())

    class Meta:
        model = Topic
        fields = ['id', 'num', 'name', 'MoSCoW_cat', 'MoSCoW_rem', 'unit']
        read_only_fields = ['id']
