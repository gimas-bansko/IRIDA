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
