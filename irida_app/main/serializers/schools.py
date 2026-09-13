"""
Сериализатори за училища и специалности.
"""

from rest_framework import serializers

from ..models import School, Specialty


class SpecialtySerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = [
            'id',
            'specialty_type',
            'specialty_num',
            'specialty_name',
            'level',
        ]


class SpecialtyMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = Specialty
        fields = ('id', 'specialty_type', 'specialty_num', 'specialty_name', 'level')


# данни за училище
class SchoolSerializer(serializers.ModelSerializer):

    class Meta:
        model = School
        fields = (
            'id', 'short_name', 'full_name', 'city', 'logo', 'address',
            'phone_number', 'email', 'boss'
        )


class SchoolMiniSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('id', 'short_name', 'full_name', 'city', 'logo')


# ЗАСЕГА НЕ СЕ ПОЛЗВА: същото като SchoolSerializer, но без 'logo'.
class SchoolSerializer2(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = [
            'id', 'short_name', 'full_name', 'city', 'address', 'phone_number', 'email', 'boss'
        ]


# Училище - обновяваане на лого
# ЗАСЕГА НЕ СЕ ПОЛЗВА от нито едно view.
class SchoolLogoSerializer(serializers.ModelSerializer):
    class Meta:
        model = School
        fields = ('id', 'logo')

    def create(self, validated_data):
        image = validated_data.get('logo')
        item = School.objects.update_or_create(id=validated_data.get("id"), defaults={'logo': image})
        return item
