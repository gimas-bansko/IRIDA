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
    subject = SubjectMiniSerializer(read_only=True)
    session = SessionMiniSerializer(read_only=True)

    class Meta:
        model = UserProfile
        fields = (
            'access_level', 'session_screen',
            'school', 'speciality', 'grade', 'section', 'subject', 'session',
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

class SessionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Session
        fields = ['id', 'num', 'name']

class UserProfileSpecSerializer(serializers.ModelSerializer):
    speciality = SpecialtySerializer()  # Включваме сериализатора за Specialty
    subject = SubjectSerializer()
    session = SessionSerializer()
    class Meta:
        model = UserProfile
        fields = ['gender', 'school', 'access_level', 'session_screen', 'grade', 'section', 'speciality', 'subject', 'session']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = [
            'gender',
            'school',
            'access_level',
            'session_screen',
            'session',
            'grade',
            'section',
            'speciality',
            'subject',
        ]

class UserSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSerializer()
    password = serializers.CharField(write_only=True, required=False, allow_blank=True)

    class Meta:
        model = User
        fields = ['id', 'username', 'password', 'email', 'first_name', 'last_name', 'userprofile']
        extra_kwargs = {
            'password': {'write_only': True},
        }

    def create(self, validated_data):
        userprofile_data = validated_data.pop('userprofile', None)
        password = validated_data.pop('password', None)
        user = User(**validated_data)
        if password:
            user.set_password(password)
        else:
            # генерирай временна или остави празно и неразреши login без парола
            user.set_unusable_password()
        user.save()

        # Актуализираме автоматично създадения профил
        if userprofile_data:
            for attr, value in userprofile_data.items():
                setattr(user.userprofile, attr, value)
            user.userprofile.save()

        return user

    def update(self, instance, validated_data):
        userprofile_data = validated_data.pop('userprofile', None)
        password = validated_data.pop('password', None)

        # Основни полета
        for f in ['username', 'email', 'first_name', 'last_name']:
            if f in validated_data:
                setattr(instance, f, validated_data[f])

        if password:
            instance.set_password(password)

        instance.save()

        if userprofile_data:
            up = instance.userprofile
            for attr, value in userprofile_data.items():
                setattr(up, attr, value)
            up.save()

        return instance

class UserReadSerializer(serializers.ModelSerializer):
    userprofile = UserProfileSpecSerializer()

    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'first_name', 'last_name', 'userprofile']
