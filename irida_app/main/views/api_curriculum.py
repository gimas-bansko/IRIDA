"""
API за учебната програма: предмети, цели, раздели и теми.
"""

import json

from django.db import transaction
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import Goal, SessionTopic, Specialty, Subject, Topic, Unit
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
        subjects = specialty.subjects.all().order_by('name', '-subject_type')

        # Сериализираме предметите
        serializer = SubjectSerializer(subjects, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


# четене/обновяване/изтриване на предмет
@api_view(['GET', 'PUT', 'DELETE'])
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

    # DELETE
    elif request.method == 'DELETE':
        try:
            subject = get_object_or_404(Subject, id=subject_id)
            if sp_id is not None:
                specialty = get_object_or_404(Specialty, id=sp_id)
                specialty.subjects.remove(subject)
            # Премахваме свързаните SessionTopic за темите в този предмет, за да избегнем ProtectedError
            SessionTopic.objects.filter(topic__unit__subject=subject).delete()
            subject.delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
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


class GoalRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Goal.objects.all()
    serializer_class = GoalSerializer


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


class UnitRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer

    def perform_destroy(self, instance):
        # Премахваме свързаните SessionTopic за темите в този раздел, за да избегнем ProtectedError
        SessionTopic.objects.filter(topic__unit=instance).delete()
        instance.delete()


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


class TopicRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Topic.objects.all()
    serializer_class = TopicWriteSerializer

    def perform_destroy(self, instance):
        # Премахваме свързаните SessionTopic, за да избегнем ProtectedError
        SessionTopic.objects.filter(topic=instance).delete()
        instance.delete()


class CurriculumImportView(APIView):
    """
    POST /api/subjects/<int:subject_id>/import-curriculum/
    Импорт на раздели и теми с MoSCoW анализ за даден предмет.
    """
    def post(self, request, subject_id):
        subject = get_object_or_404(Subject, id=subject_id)
        data = request.data

        # Поддръжка както на структуриран обект с ключ "units", така и на директен масив или raw_json низ
        units_data = None
        if isinstance(data, list):
            units_data = data
        elif isinstance(data, dict):
            if 'units' in data:
                units_data = data.get('units')
                if isinstance(units_data, str):
                    try:
                        units_data = json.loads(units_data)
                    except Exception as e:
                        return Response({'error': f'Невалиден JSON в полето "units": {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
            elif 'raw_json' in data:
                try:
                    units_data = json.loads(data['raw_json'])
                except Exception as e:
                    return Response({'error': f'Невалиден JSON формат: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(units_data, list) or len(units_data) == 0:
            return Response(
                {'error': 'Списъкът с раздели е празен или с невалиден формат (очаква се JSON масив от раздели).'},
                status=status.HTTP_400_BAD_REQUEST
            )

        replace_existing = data.get('replace_existing', True) if isinstance(data, dict) else True
        if isinstance(replace_existing, str):
            replace_existing = replace_existing.lower() in ['true', '1', 't', 'yes']

        # Валидация и изчистване на входните данни
        valid_moscow = {'M', 'S', 'C', 'W', ''}
        cleaned_units = []
        for u_idx, u in enumerate(units_data, start=1):
            if not isinstance(u, dict):
                return Response({'error': f'Раздел #{u_idx} не е валиден обект.'}, status=status.HTTP_400_BAD_REQUEST)
            u_name = str(u.get('name', '')).strip()
            if not u_name:
                return Response({'error': f'Раздел #{u_idx} няма въведено наименование (поле "name").'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                u_num = int(u.get('num', u_idx))
                u_hours = int(u.get('hours', 1))
            except (ValueError, TypeError):
                return Response({'error': f'Невалиден номер или брой часове за раздел "{u_name}".'}, status=status.HTTP_400_BAD_REQUEST)

            topics_raw = u.get('topics', [])
            if not isinstance(topics_raw, list):
                topics_raw = []

            cleaned_topics = []
            for t_idx, t in enumerate(topics_raw, start=1):
                if not isinstance(t, dict):
                    continue
                t_name = str(t.get('name', '')).strip()
                if not t_name:
                    continue
                try:
                    t_num = int(t.get('num', t_idx))
                except (ValueError, TypeError):
                    t_num = t_idx
                t_moscow_cat = str(t.get('MoSCoW_cat', 'M')).strip().upper()
                if t_moscow_cat not in valid_moscow:
                    t_moscow_cat = 'M'
                t_moscow_rem = str(t.get('MoSCoW_rem', '') or '')
                cleaned_topics.append({
                    'num': t_num,
                    'name': t_name,
                    'MoSCoW_cat': t_moscow_cat,
                    'MoSCoW_rem': t_moscow_rem
                })

            cleaned_units.append({
                'num': u_num,
                'name': u_name,
                'hours': u_hours,
                'topics': cleaned_topics
            })

        if len(cleaned_units) == 0:
            return Response({'error': 'Не са намерени валидни данни за раздели в подадения JSON.'}, status=status.HTTP_400_BAD_REQUEST)

        # Изпълнение на записа в транзакция
        if replace_existing:
            has_linked_sessions = SessionTopic.objects.filter(topic__unit__subject=subject).exists()
            if has_linked_sessions:
                return Response({
                    'error': 'Не могат да бъдат изтрити съществуващите раздели и теми, тъй като към тях вече има свързани уроци/занятия в системата. Моля, изберете опцията за добавяне към съществуващите.'
                }, status=status.HTTP_400_BAD_REQUEST)

            with transaction.atomic():
                Unit.objects.filter(subject=subject).delete()
                for u in cleaned_units:
                    unit_obj = Unit.objects.create(
                        subject=subject,
                        num=u['num'],
                        name=u['name'],
                        hours=u['hours']
                    )
                    for t in u['topics']:
                        Topic.objects.create(
                            unit=unit_obj,
                            num=t['num'],
                            name=t['name'],
                            MoSCoW_cat=t['MoSCoW_cat'],
                            MoSCoW_rem=t['MoSCoW_rem']
                        )
        else:
            with transaction.atomic():
                max_unit_num = Unit.objects.filter(subject=subject).order_by('-num').values_list('num', flat=True).first() or 0
                for u in cleaned_units:
                    unit_num = u['num']
                    if Unit.objects.filter(subject=subject, num=unit_num).exists():
                        max_unit_num += 1
                        unit_num = max_unit_num
                    else:
                        if unit_num > max_unit_num:
                            max_unit_num = unit_num

                    unit_obj = Unit.objects.create(
                        subject=subject,
                        num=unit_num,
                        name=u['name'],
                        hours=u['hours']
                    )
                    for t in u['topics']:
                        Topic.objects.create(
                            unit=unit_obj,
                            num=t['num'],
                            name=t['name'],
                            MoSCoW_cat=t['MoSCoW_cat'],
                            MoSCoW_rem=t['MoSCoW_rem']
                        )

        # Презареждане и сериализиране на актуализирания списък
        updated_units = (
            Unit.objects
            .filter(subject=subject)
            .order_by('num', 'id')
            .prefetch_related(Prefetch('unit_topic', queryset=Topic.objects.order_by('num', 'id')))
        )
        serializer = UnitSerializer(updated_units, many=True)
        total_topics = sum(len(u['topics']) for u in cleaned_units)

        return Response({
            'message': f'Успешно бяха импортирани {len(cleaned_units)} раздела и {total_topics} теми по предмета.',
            'units': serializer.data
        }, status=status.HTTP_200_OK)


class GoalImportView(APIView):
    """
    POST /api/subjects/<int:subject_id>/import-goals/
    Импорт на образователни/педагогически цели за даден предмет.
    """
    def post(self, request, subject_id):
        subject = get_object_or_404(Subject, id=subject_id)
        data = request.data

        # Поддръжка както на структуриран обект с ключ "goals", така и на директен масив или raw_json низ
        goals_data = None
        if isinstance(data, list):
            goals_data = data
        elif isinstance(data, dict):
            if 'goals' in data:
                goals_data = data.get('goals')
                if isinstance(goals_data, str):
                    try:
                        goals_data = json.loads(goals_data)
                    except Exception as e:
                        return Response({'error': f'Невалиден JSON в полето "goals": {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
            elif 'raw_json' in data:
                try:
                    goals_data = json.loads(data['raw_json'])
                except Exception as e:
                    return Response({'error': f'Невалиден JSON формат: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(goals_data, list) or len(goals_data) == 0:
            return Response(
                {'error': 'Списъкът с цели е празен или с невалиден формат (очаква се JSON масив от цели).'},
                status=status.HTTP_400_BAD_REQUEST
            )

        replace_existing = data.get('replace_existing', True) if isinstance(data, dict) else True
        if isinstance(replace_existing, str):
            replace_existing = replace_existing.lower() in ['true', '1', 't', 'yes']

        # Валидация и изчистване на входните данни
        cleaned_goals = []
        for g_idx, g in enumerate(goals_data, start=1):
            if not isinstance(g, dict):
                return Response({'error': f'Цел #{g_idx} не е валиден обект.'}, status=status.HTTP_400_BAD_REQUEST)
            g_name = str(g.get('name', '')).strip()
            if not g_name:
                return Response({'error': f'Цел #{g_idx} няма въведено наименование (поле "name").'}, status=status.HTTP_400_BAD_REQUEST)
            try:
                g_num = int(g.get('num', g_idx))
                if g_num < 1:
                    g_num = g_idx
            except (ValueError, TypeError):
                g_num = g_idx

            cleaned_goals.append({
                'num': g_num,
                'name': g_name[:200]
            })

        if len(cleaned_goals) == 0:
            return Response({'error': 'Не са намерени валидни данни за цели в подадения JSON.'}, status=status.HTTP_400_BAD_REQUEST)

        # Изпълнение на записа в транзакция
        if replace_existing:
            with transaction.atomic():
                Goal.objects.filter(course=subject).delete()
                for g in cleaned_goals:
                    Goal.objects.create(
                        course=subject,
                        num=g['num'],
                        name=g['name']
                    )
        else:
            with transaction.atomic():
                max_goal_num = Goal.objects.filter(course=subject).order_by('-num').values_list('num', flat=True).first() or 0
                for g in cleaned_goals:
                    goal_num = g['num']
                    if Goal.objects.filter(course=subject, num=goal_num).exists():
                        max_goal_num += 1
                        goal_num = max_goal_num
                    else:
                        if goal_num > max_goal_num:
                            max_goal_num = goal_num

                    Goal.objects.create(
                        course=subject,
                        num=goal_num,
                        name=g['name']
                    )

        # Презареждане и сериализиране на актуализирания списък
        updated_goals = Goal.objects.filter(course=subject).order_by('num', 'id')
        serializer = GoalSerializer(updated_goals, many=True)

        return Response({
            'message': f'Успешно бяха импортирани {len(cleaned_goals)} цели по предмета.',
            'goals': serializer.data
        }, status=status.HTTP_200_OK)
