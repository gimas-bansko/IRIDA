from rest_framework import serializers
from .models import *

from django.contrib.auth.models import User

class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = [
            'id',
            'specialty_num',
            'specialty_name',
            'level',
        ]

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

class UserProfileSpecSerializer(serializers.ModelSerializer):
    speciality = SpecialtySerializer()  # Включваме сериализатора за Specialty

    class Meta:
        model = UserProfile
        fields = ['gender', 'school', 'access_level', 'session_screen', 'session_theme', 'speciality', 'subject']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['gender', 'school', 'access_level', 'session_screen', 'session_theme', 'speciality', 'subject']

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'userprofile']
        extra_kwargs = {
            'password': {'write_only': True},  # Паролата не трябва да се връща в отговорите
        }

    def create(self, validated_data):
        # Извличаме данните за профила
        userprofile_data = validated_data.pop('userprofile', None)

        # Създаваме потребителя
        user = User.objects.create_user(**validated_data)

        # Актуализираме автоматично създадения профил, ако има данни за userprofile
        if userprofile_data:
            for attr, value in userprofile_data.items():
                setattr(user.userprofile, attr, value)
            user.userprofile.save()

        return user

    def update(self, instance, validated_data):
        # Извличаме данните за профила
        userprofile_data = validated_data.pop('userprofile', None)

        # Актуализираме основните данни на потребителя
        instance.username = validated_data.get('username', instance.username)
        instance.email = validated_data.get('email', instance.email)
        instance.first_name = validated_data.get('first_name', instance.first_name)
        instance.last_name = validated_data.get('last_name', instance.last_name)

        instance.save()

        # Актуализираме профила на потребителя, ако има данни за него
        if userprofile_data:
            userprofile = instance.userprofile
            userprofile.gender = userprofile_data.get('gender', userprofile.gender)
            userprofile.save()

        return instance


class UserReadSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSpecSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'userprofile']

# данни за училище
class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = (
            'id', 'short_name', 'full_name', 'city', 'logo', 'address',
            'phone_number', 'email', 'boss'
        )

class SchoolSerializer2(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            'id', 'short_name', 'full_name', 'city', 'address', 'phone_number', 'email', 'boss'
        ]

# Училище - обновяваане на лого
class SchoolLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('id', 'logo')

    def create(self, validated_data):
        image = validated_data.get('logo')
        item = School.objects.update_or_create(id=validated_data.get("id"), defaults={'logo': image})
        return item

# ******************
#     Предмети
# ******************

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

# serializers.py

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

class SessionTopicWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = SessionTopic
        fields = ['id', 'session', 'topic', 'description']

class SessionTopicReadSerializer(serializers.ModelSerializer):
    topic = TopicSerializer(read_only=True)

    class Meta:
        model = SessionTopic
        fields = ['id', 'description', 'topic', 'session']

class SessionWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'course', 'num', 'name', 'focus', 'goals', 'duration', 'session_type', 'basic_level', 'collapsed']

class SessionReadSerializer(serializers.ModelSerializer):
    session_topics = SessionTopicReadSerializer(many=True, read_only=True)

    class Meta:
        model = Session
        fields = ['id', 'course', 'num', 'name', 'focus', 'goals', 'duration', 'session_type', 'basic_level', 'collapsed', 'session_topics']

class SchoolMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('id', 'short_name', 'full_name', 'city', 'logo')

class SpecialtyMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ('id', 'specialty_num', 'specialty_name', 'level')

class KlassMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Klass
        fields = ('id', 'grade', 'section')

class SubjectMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Subject
        fields = ('id', 'name', 'grade', 'subject_type')

class SessionMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ('id', 'num', 'name', 'focus', 'goals', 'duration', 'session_type', 'basic_level')

class UserProfileExpandedSerializer(serializers.ModelSerializer):
    school = SchoolMiniSerializer(read_only=True)
    speciality = SpecialtyMiniSerializer(read_only=True)
    grade_section = KlassMiniSerializer(read_only=True)
    subject = SubjectMiniSerializer(read_only=True)
    session = SessionMiniSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            'access_level', 'session_screen',
            'school', 'speciality', 'grade_section', 'subject', 'session',
        )

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