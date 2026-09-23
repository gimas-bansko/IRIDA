"""
Сериализатори за потребител и профил.
"""

from django.contrib.auth.models import User
from rest_framework import serializers

from ..models import UserProfile
from .curriculum import SubjectMiniSerializer, SubjectSerializer
from .lessons import SessionMiniSerializer, SessionSerializer
from .schools import (
    SchoolMiniSerializer,
    SpecialtyMiniSerializer,
    SpecialtySerializer,
)


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
        extra_kwargs = {
            'school': {'required': False, 'allow_null': True},
            'speciality': {'required': False, 'allow_null': True},
            'subject': {'required': False, 'allow_null': True},
            'session': {'required': False, 'allow_null': True},
            'grade': {'required': False},
            'section': {'required': False},
        }

    def to_internal_value(self, data):
        if isinstance(data, dict):
            data = data.copy()
            for fk_field in ['school', 'speciality', 'subject', 'session']:
                val = data.get(fk_field)
                if val == 0 or val == '0' or val == '':
                    data[fk_field] = None
            if 'section' in data and data['section']:
                sec = str(data['section']).strip().lower()
                latin_to_cyrillic = {
                    'a': 'а', 'b': 'б', 'c': 'ц', 'd': 'д', 'e': 'е',
                    'f': 'ф', 'g': 'г', 'h': 'х', 'i': 'и', 'j': 'й',
                    'k': 'к', 'l': 'л', 'm': 'м', 'n': 'н', 'o': 'о',
                    'p': 'п', 'q': 'я', 'r': 'р', 's': 'с', 't': 'т',
                    'u': 'у', 'v': 'в', 'w': 'в', 'x': 'х', 'y': 'ъ', 'z': 'з'
                }
                if sec in latin_to_cyrillic:
                    sec = latin_to_cyrillic[sec]
                data['section'] = sec
        return super().to_internal_value(data)


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


class UserProfileSpecSerializer(serializers.ModelSerializer):
    speciality = SpecialtySerializer()  # Включваме сериализатора за Specialty
    subject = SubjectSerializer()
    session = SessionSerializer()

    class Meta:
        model = UserProfile
        fields = ['gender', 'school', 'access_level', 'session_screen', 'grade', 'section', 'speciality', 'subject', 'session']


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
