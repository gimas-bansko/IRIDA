"""
API за училища и специалности.
"""

from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import School, SchoolDayConfig, Specialty
from ..serializers import (
    SchoolDayConfigSerializer,
    SchoolSerializer,
    SpecialtySerializer,
)


# данни за определено по id училище
class SchoolDetailAPIView(generics.RetrieveAPIView):
    queryset = School.objects.all()
    serializer_class = SchoolSerializer


# специалности за определено по id училище
class SchoolSpecialtiesView(APIView):
    def get(self, request, school_id, *args, **kwargs):
        try:
            # Намираме училището по зададеното ID
            school = School.objects.get(id=school_id)
        except School.DoesNotExist:
            return Response({'error': 'Училището не съществува.'}, status=status.HTTP_404_NOT_FOUND)

        # Вземаме всички специалности, свързани с училището
        specialties = school.specialities.all()

        # Сериализираме специалностите
        serializer = SpecialtySerializer(specialties, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# четене/обновяване/изтриване на специалност
@api_view(['GET', 'PUT', 'DELETE'])
def specialty_detail(request, specialty_id, school_id=None):
    # GET
    if request.method == 'GET':
        if int(specialty_id) == 0:
            # По избор: върнете празен шаблон за форми
            return Response({
                'id': 0,
                'specialty_type': 'специалност',
                'specialty_num': '',
                'specialty_name': '',
                'level': None,
            })
        specialty = get_object_or_404(Specialty, id=specialty_id)
        serializer = SpecialtySerializer(specialty, context={'request': request})
        return Response(serializer.data)

    # PUT
    elif request.method == 'PUT':
        data = request.data
        try:
            # Създаване при id == 0
            if int(specialty_id) == 0:
                serializer = SpecialtySerializer(data=data, context={'request': request})
                if serializer.is_valid():
                    specialty = serializer.save()
                    # Ако имаме school_id в URL, добавяме M2M връзка
                    if school_id is not None:
                        school = get_object_or_404(School, id=school_id)
                        school.specialities.add(specialty)
                    return Response(SpecialtySerializer(specialty, context={'request': request}).data,
                                    status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Обновяване при id != 0
            specialty = get_object_or_404(Specialty, id=specialty_id)
            serializer = SpecialtySerializer(specialty, data=data, partial=True, context={'request': request})
            if serializer.is_valid():
                specialty = serializer.save()
                # По желание: ако school_id е подаден, уверете се, че връзката съществува
                if school_id is not None:
                    school = get_object_or_404(School, id=school_id)
                    school.specialities.add(specialty)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

    # DELETE
    elif request.method == 'DELETE':
        try:
            specialty = get_object_or_404(Specialty, id=specialty_id)
            if school_id is not None:
                school = get_object_or_404(School, id=school_id)
                school.specialities.remove(specialty)
            specialty.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# параметри на учебния ден
class SchoolDayConfigAPIView(APIView):
    def get(self, request, *args, **kwargs):
        config = SchoolDayConfig.get_config()
        serializer = SchoolDayConfigSerializer(config)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def put(self, request, *args, **kwargs):
        config = SchoolDayConfig.get_config()
        serializer = SchoolDayConfigSerializer(config, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def patch(self, request, *args, **kwargs):
        return self.put(request, *args, **kwargs)
