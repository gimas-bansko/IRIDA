"""
API за учебната програма: предмети, цели, раздели и теми.
"""

from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Goal, Specialty, Subject, Topic, Unit
from ..serializers import (
    GoalSerializer,
    SubjectSerializer,
    TopicWriteSerializer,
    UnitSerializer,
    UnitWriteSerializer,
)


# ***************************
#          Предмети
# ***************************

# предмети по определена специалност (по id)
class SpecialtySubjectsView(APIView):
    def get(self, request, sp_id, *args, **kwargs):
        try:
            # Намираме специалността по зададеното ID
            specialty = Specialty.objects.get(id=sp_id)
        except Specialty.DoesNotExist:
            return Response({'error': 'Специалността не съществува.'}, status=status.HTTP_404_NOT_FOUND)

        # Вземаме всички предмети, свързани със специалността
        subjects = specialty.subjects.all()

        # Сериализираме предметите
        serializer = SubjectSerializer(subjects, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# четене/обновяване на предмет
@api_view(['GET', 'PUT'])
def subject_detail(request, subject_id, sp_id=None):
    # GET
    if request.method == 'GET':
        if int(subject_id) == 0:
            # По избор: върнете празен шаблон за форми
            return Response({
                'id': 0,
                'name': '',
                'grade': 12,
                'subject_type': 'теория',
                'hpy': 18,
                'wpy': 0,
                'hpw1': 0,
                'hpw2': 0,
                })
        subject = get_object_or_404(Subject, id=subject_id)
        serializer = SubjectSerializer(subject, context={'request': request})
        return Response(serializer.data)

    # PUT
    elif request.method == 'PUT':
        data = request.data
        try:
            # Създаване при id == 0
            if int(subject_id) == 0:
                serializer = SubjectSerializer(data=data, context={'request': request})
                if serializer.is_valid():
                    subject = serializer.save()
                    # Ако имаме sp_id в URL, добавяме M2M връзка
                    if sp_id is not None:
                        specialty = get_object_or_404(Specialty, id=sp_id)
                        specialty.subjects.add(subject)
                    return Response(SubjectSerializer(subject, context={'request': request}).data,
                                    status=status.HTTP_201_CREATED)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

            # Обновяване при id != 0
            subject = get_object_or_404(Subject, id=subject_id)
            serializer = SubjectSerializer(subject, data=data, partial=True, context={'request': request})
            if serializer.is_valid():
                subject = serializer.save()
                # По желание: ако sp_id е подаден, уверете се, че връзката съществува
                if sp_id is not None:
                    specialty = get_object_or_404(Specialty, id=sp_id)
                    specialty.subjects.add(subject)
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        except Exception as e:
            import traceback
            traceback.print_exc()
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ***************************
#            Цели
# ***************************

# списък на целите на обучението по предмета по подразбиране на текущия потребител(по id)
class SubjectGoalsView(generics.ListAPIView):
    serializer_class = GoalSerializer

    def get_queryset(self):
        sb_id = self.kwargs['sb_id']
        return Goal.objects.filter(course_id=sb_id).order_by('num', 'id')


class GoalUpsertView(APIView):
    def post(self, request):
        goal_id = request.data.get('id', 0) or 0
        try:
            goal_id = int(goal_id)
        except (TypeError, ValueError):
            return Response({'detail': 'Invalid id'}, status=status.HTTP_400_BAD_REQUEST)

        if goal_id > 0:
            # Update
            instance = get_object_or_404(Goal, id=goal_id)
            serializer = GoalSerializer(instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            # Create
            serializer = GoalSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


# ***************************
#      Раздели и теми
# ***************************
class SubjectUnitsWithTopicsView(generics.ListAPIView):
    serializer_class = UnitSerializer

    def get_queryset(self):
        subject_id = self.kwargs['subject_id']
        get_object_or_404(Subject, id=subject_id)

        # Подредба на вложените теми по num (и id за стабилност)
        topics_prefetch = Prefetch('unit_topic', queryset=Topic.objects.order_by('num', 'id')
        )

        # Подредба на Units по num (и id за стабилност)
        return (
            Unit.objects
            .filter(subject_id=subject_id)
            .order_by('num', 'id')
            .prefetch_related(topics_prefetch)
        )


class UnitUpsertView(APIView):
    """
    POST:
      - id == 0 -> create
      - id > 0 -> update
    Body: { id, num, name, hours, subject }
    """
    def post(self, request):
        unit_id = request.data.get('id', 0) or 0
        try:
            unit_id = int(unit_id)
        except (TypeError, ValueError):
            return Response({'detail': 'Invalid id'}, status=status.HTTP_400_BAD_REQUEST)

        if unit_id > 0:
            instance = get_object_or_404(Unit, id=unit_id)
            serializer = UnitWriteSerializer(instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = UnitWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)


class TopicUpsertView(APIView):
    """
    POST:
      - id == 0  -> create
      - id > 0   -> update
    Body: { id, num, name, MoSCoW_cat, MoSCoW_rem, unit }
    """
    def post(self, request):
        topic_id = request.data.get('id', 0) or 0
        try:
            topic_id = int(topic_id)
        except (TypeError, ValueError):
            return Response({'detail': 'Invalid id'}, status=status.HTTP_400_BAD_REQUEST)

        if topic_id > 0:
            instance = get_object_or_404(Topic, id=topic_id)
            serializer = TopicWriteSerializer(instance, data=request.data, partial=False)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            serializer = TopicWriteSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
