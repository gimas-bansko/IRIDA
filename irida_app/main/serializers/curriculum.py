"""
Сериализатори за учебната програма: предмет, раздели, теми, цели.
"""

from rest_framework import serializers

from ..models import Goal, Subject, Topic, Unit


class SubjectSerializer(serializers.ModelSerializer):
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
        ]


class SubjectMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name', 'grade', 'subject_type')


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
