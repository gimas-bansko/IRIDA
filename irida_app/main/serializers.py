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
            'plan',
        ]

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        request = self.context.get('request')

        if representation['plan'] and request:
            representation['plan'] = request.build_absolute_uri(instance.nip.url)

        return representation


class UserProfileSpecSerializer(serializers.ModelSerializer):
    speciality = SpecialtySerializer()  # Включваме сериализатора за Specialty

    class Meta:
        model = UserProfile
        fields = ['gender', 'school', 'access_level', 'session_screen', 'session_theme', 'speciality']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserProfile
        fields = ['gender', 'school', 'access_level', 'session_screen', 'session_theme', 'speciality']

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

