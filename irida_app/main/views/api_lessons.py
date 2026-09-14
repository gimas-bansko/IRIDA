"""
API за урок/занятие: самите уроци, темите към тях, точките от плана
и бележките/задачите към точките.
"""

import json

from django.db import transaction
from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from rest_framework.views import APIView

from ..models import (
    Session,
    SessionAttachment,
    SessionNote,
    SessionPoint,
    SessionTask,
    SessionTopic,
    Subject,
    Topic,
)
from ..serializers import (
    SessionAttachmentSerializer,
    SessionNoteSerializer,
    SessionPointSerializer,
    SessionReadSerializer,
    SessionTaskSerializer,
    SessionTopicReadSerializerDetailed,
    SessionTopicWriteSerializer,
    SessionWriteSerializer,
)


# ***************************
#           Уроци
# ***************************

# Списък и създаване на Session
class SessionListCreateView(generics.ListCreateAPIView):
    serializer_class = SessionWriteSerializer

    def get_queryset(self):
        # Показва всички на текущия потребител course_lessons_view? Или глобално. Ако имаш филтър, добави го.
        return Session.objects.all()


# Изглед за детайли/редакция/изтриване на Session
class SessionRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Session.objects.all()
    serializer_class = SessionWriteSerializer


# Списък на Session за даден Subject (с вложени SessionTopic, SessionTask, SessionAttachment, SessionPoint)
class SubjectSessionsWithTopicsView(generics.ListAPIView):
    serializer_class = SessionReadSerializer

    def get_queryset(self):
        subject_id = self.kwargs['subject_id']
        get_object_or_404(Subject, id=subject_id)
        topics_prefetch = Prefetch(
            'session_topics',
            queryset=SessionTopic.objects.select_related('topic').order_by('id')
        )
        tasks_prefetch = Prefetch(
            'session_tasks',
            queryset=SessionTask.objects.order_by('num', 'id')
        )
        attachments_prefetch = Prefetch(
            'session_attachments',
            queryset=SessionAttachment.objects.order_by('num', 'id')
        )
        points_prefetch = Prefetch(
            'session_points',
            queryset=SessionPoint.objects.order_by('num', 'id')
        )
        return (
            Session.objects
            .filter(course_id=subject_id)
            .order_by('num', 'id')
            .prefetch_related(topics_prefetch, tasks_prefetch, attachments_prefetch, points_prefetch)
        )


# ***************************
#      Теми към урок
# ***************************

# CRUD за SessionTopic
class SessionTopicListCreateView(generics.ListCreateAPIView):
    serializer_class = SessionTopicWriteSerializer

    def get_queryset(self):
        # По избор: филтър по session_id от query параметър
        session_id = self.request.query_params.get('session')
        qs = SessionTopic.objects.all().select_related('topic', 'session')
        if session_id:
            qs = qs.filter(session_id=session_id)
        return qs.order_by('id')


class SessionTopicRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = SessionTopic.objects.all().select_related('topic', 'session')
    serializer_class = SessionTopicWriteSerializer


class SessionTopicsForSessionView(generics.ListAPIView):
    serializer_class = SessionTopicReadSerializerDetailed

    def get_queryset(self):
        session_id = self.kwargs['session_id']
        # Валидация, че сесията съществува (по желание)
        get_object_or_404(Session, id=session_id)
        return (
            SessionTopic.objects
            .filter(session_id=session_id)
            .select_related('topic')   # за да е ефикасно „разгъването“
            .order_by('topic__num', 'id')
        )


# ***************************
#     Точки от плана
# ***************************
class SessionPointsForSessionView(generics.ListAPIView):
    serializer_class = SessionPointSerializer

    def get_queryset(self):
        session_id = self.kwargs['session_id']
        # Уверяваме се, че сесията съществува
        get_object_or_404(Session, id=session_id)
        return (
            SessionPoint.objects
            .filter(session_id=session_id)
            .order_by('num', 'id')
        )


@api_view(['POST'])
@csrf_exempt  # вероятно без ефект - DRF/SessionAuthentication налага CSRF сама
def session_point_upsert(request):
    """
    POST body: { id, session, num, name, description, duration, content }
    - id == 0 или липсва -> create
    - id > 0 -> update
    """
    point_id = request.data.get('id', 0) or 0
    try:
        point_id = int(point_id)
    except (TypeError, ValueError):
        return Response({'detail': 'Invalid id'}, status=status.HTTP_400_BAD_REQUEST)

    if point_id > 0:
        instance = get_object_or_404(SessionPoint, id=point_id)
        serializer = SessionPointSerializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        serializer = SessionPointSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def session_point_delete(request, pk):
    instance = get_object_or_404(SessionPoint, id=pk)
    instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ***************************
#          Бележки
# ***************************
class SessionNotesForSessionView(generics.ListAPIView):
    serializer_class = SessionNoteSerializer

    def get_queryset(self):
        session_id = self.kwargs['session_id']
        get_object_or_404(Session, id=session_id)
        return SessionNote.objects.filter(session_id=session_id).order_by('num', 'id')


@api_view(['POST'])
@csrf_exempt  # вероятно без ефект - виж бележката при session_point_upsert
def session_note_upsert(request):
    """
    POST body: { id, session, point, num, name, content }
    id == 0/missing -> create; id > 0 -> update
    """
    note_id = request.data.get('id', 0) or 0
    try:
        note_id = int(note_id)
    except (TypeError, ValueError):
        return Response({'detail': 'Invalid id'}, status=status.HTTP_400_BAD_REQUEST)

    if note_id > 0:
        instance = get_object_or_404(SessionNote, id=note_id)
        serializer = SessionNoteSerializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        serializer = SessionNoteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def session_note_delete(request, pk):
    instance = get_object_or_404(SessionNote, id=pk)
    instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ***************************
#          Задачи
# ***************************
class SessionTasksForSessionView(generics.ListAPIView):
    serializer_class = SessionTaskSerializer

    def get_queryset(self):
        session_id = self.kwargs['session_id']
        get_object_or_404(Session, id=session_id)
        return SessionTask.objects.filter(session_id=session_id).order_by('num', 'id')


@api_view(['POST'])
@csrf_exempt  # вероятно без ефект - виж бележката при session_point_upsert
def session_task_upsert(request):
    """
    POST body: { id, session, point, num, name, condition, answer }
    id == 0/missing -> create; id > 0 -> update
    """
    task_id = request.data.get('id', 0) or 0
    try:
        task_id = int(task_id)
    except (TypeError, ValueError):
        return Response({'detail': 'Invalid id'}, status=status.HTTP_400_BAD_REQUEST)

    if task_id > 0:
        instance = get_object_or_404(SessionTask, id=task_id)
        serializer = SessionTaskSerializer(instance, data=request.data, partial=False)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        serializer = SessionTaskSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def session_task_delete(request, pk):
    instance = get_object_or_404(SessionTask, id=pk)
    instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


# ***************************
#         Приложения
# ***************************
class SessionAttachmentsForSessionView(generics.ListAPIView):
    serializer_class = SessionAttachmentSerializer

    def get_queryset(self):
        session_id = self.kwargs['session_id']
        get_object_or_404(Session, id=session_id)
        qs = SessionAttachment.objects.filter(session_id=session_id)
        attachment_type = self.request.query_params.get('type')
        if attachment_type:
            qs = qs.filter(attachment_type=attachment_type)
        return qs.order_by('num', 'id')


@api_view(['POST'])
@csrf_exempt
def session_attachment_upsert(request):
    """
    POST body: { id, session, point, num, name, attachment_type, file, description }
    id == 0/missing -> create; id > 0 -> update
    """
    attachment_id = request.data.get('id', 0) or 0
    try:
        attachment_id = int(attachment_id)
    except (TypeError, ValueError):
        return Response({'detail': 'Invalid id'}, status=status.HTTP_400_BAD_REQUEST)

    data = request.data.copy() if hasattr(request.data, 'copy') else dict(request.data)
    if data.get('point') in ['', 'null', 'None', None]:
        data['point'] = None

    if attachment_id > 0:
        instance = get_object_or_404(SessionAttachment, id=attachment_id)
        if 'file' not in request.FILES and ('file' not in data or not data['file']):
            data.pop('file', None)
        serializer = SessionAttachmentSerializer(instance, data=data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_200_OK)
    else:
        serializer = SessionAttachmentSerializer(data=data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


@api_view(['DELETE'])
def session_attachment_delete(request, pk):
    instance = get_object_or_404(SessionAttachment, id=pk)
    instance.delete()
    return Response(status=status.HTTP_204_NO_CONTENT)


class SessionImportView(APIView):
    """
    POST /api/subjects/<int:subject_id>/import-sessions/
    Импорт на уроци/занятия за даден предмет с автоматично обвързване на теми от учебната програма.
    """
    def post(self, request, subject_id):
        subject = get_object_or_404(Subject, id=subject_id)
        data = request.data

        # Поддръжка както на структуриран обект с ключ "sessions", така и на директен масив или raw_json низ
        sessions_data = None
        if isinstance(data, list):
            sessions_data = data
        elif isinstance(data, dict):
            if 'sessions' in data:
                sessions_data = data.get('sessions')
                if isinstance(sessions_data, str):
                    try:
                        sessions_data = json.loads(sessions_data)
                    except Exception as e:
                        return Response({'error': f'Невалиден JSON в полето "sessions": {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)
            elif 'raw_json' in data:
                try:
                    sessions_data = json.loads(data['raw_json'])
                except Exception as e:
                    return Response({'error': f'Невалиден JSON формат: {str(e)}'}, status=status.HTTP_400_BAD_REQUEST)

        if not isinstance(sessions_data, list) or len(sessions_data) == 0:
            return Response(
                {'error': 'Списъкът с уроци е празен или с невалиден формат (очаква се JSON масив от уроци).'},
                status=status.HTTP_400_BAD_REQUEST
            )

        replace_existing = data.get('replace_existing', True) if isinstance(data, dict) else True
        if isinstance(replace_existing, str):
            replace_existing = replace_existing.lower() in ['true', '1', 't', 'yes']

        # Презареждане и индексиране на темите за този предмет
        topics_qs = Topic.objects.filter(unit__subject=subject).select_related('unit')
        topics_by_id = {t.id: t for t in topics_qs}
        topics_by_unit_topic_num = {(t.unit.num, t.num): t for t in topics_qs}
        topics_by_name = {t.name.strip().lower(): t for t in topics_qs}
        topics_by_num = {}
        for t in topics_qs:
            topics_by_num.setdefault(t.num, []).append(t)

        SESSION_TYPES = {'НЗ', 'УПР', 'ПК', 'ОС', 'K'}
        TYPE_MAPPING = {
            'нови знания': 'НЗ',
            'нови': 'НЗ',
            'нз': 'НЗ',
            'упражнение': 'УПР',
            'упр': 'УПР',
            'практика': 'УПР',
            'проверка и контрол': 'ПК',
            'проверка': 'ПК',
            'контрол': 'ПК',
            'пк': 'ПК',
            'обобщаване и систематизиране': 'ОС',
            'обобщение': 'ОС',
            'ос': 'ОС',
            'комбиниран': 'K',
            'комбиниран урок': 'K',
            'k': 'K',
            'к': 'K'
        }

        cleaned_sessions = []
        for s_idx, s in enumerate(sessions_data, start=1):
            if not isinstance(s, dict):
                return Response({'error': f'Урок #{s_idx} не е валиден обект.'}, status=status.HTTP_400_BAD_REQUEST)
            s_name = str(s.get('name', '')).strip()
            if not s_name:
                return Response({'error': f'Урок #{s_idx} няма въведено наименование (поле "name").'}, status=status.HTTP_400_BAD_REQUEST)

            try:
                s_num = int(s.get('num', s_idx))
                if s_num < 1:
                    s_num = s_idx
            except (ValueError, TypeError):
                s_num = s_idx

            raw_type = str(s.get('session_type', 'НЗ')).strip()
            session_type = TYPE_MAPPING.get(raw_type.lower(), raw_type.upper())
            if session_type not in SESSION_TYPES:
                session_type = 'НЗ'

            try:
                duration = int(s.get('duration', 2))
                if duration < 1:
                    duration = 1
                elif duration > 7:
                    duration = 7
            except (ValueError, TypeError):
                duration = 2

            raw_basic = s.get('basic_level', True)
            if isinstance(raw_basic, str):
                basic_level = raw_basic.lower() in ['true', '1', 't', 'yes', 'основен']
            else:
                basic_level = bool(raw_basic)

            goals = str(s.get('goals', '')).strip()
            focus = str(s.get('focus', '')).strip()

            # Обработка на темите към урока
            raw_topics = s.get('topics', s.get('session_topics', []))
            if not isinstance(raw_topics, list):
                raw_topics = []

            matched_topics = []
            for t_item in raw_topics:
                matched_topic = None
                desc = ''
                if isinstance(t_item, dict):
                    desc = str(t_item.get('description', '')).strip()
                    t_id = t_item.get('id') or t_item.get('topic_id')
                    u_num = t_item.get('unit_num') or (t_item.get('unit', {}).get('num') if isinstance(t_item.get('unit'), dict) else None)
                    t_num = t_item.get('topic_num') or t_item.get('num')
                    t_name = str(t_item.get('name') or t_item.get('topic_name') or '').strip().lower()

                    if t_id:
                        try:
                            if int(t_id) in topics_by_id:
                                matched_topic = topics_by_id[int(t_id)]
                        except (ValueError, TypeError):
                            pass

                    if not matched_topic and u_num is not None and t_num is not None:
                        try:
                            key = (int(u_num), int(t_num))
                            if key in topics_by_unit_topic_num:
                                matched_topic = topics_by_unit_topic_num[key]
                        except (ValueError, TypeError):
                            pass

                    if not matched_topic and t_name and t_name in topics_by_name:
                        matched_topic = topics_by_name[t_name]

                    if not matched_topic and t_num is not None:
                        try:
                            num_matches = topics_by_num.get(int(t_num), [])
                            if len(num_matches) == 1:
                                matched_topic = num_matches[0]
                        except (ValueError, TypeError):
                            pass
                elif isinstance(t_item, int) and t_item in topics_by_id:
                    matched_topic = topics_by_id[t_item]
                elif isinstance(t_item, str):
                    clean_item = t_item.strip().lower()
                    if clean_item in topics_by_name:
                        matched_topic = topics_by_name[clean_item]

                if matched_topic and matched_topic not in [mt['topic'] for mt in matched_topics]:
                    matched_topics.append({
                        'topic': matched_topic,
                        'description': desc[:200]
                    })

            cleaned_sessions.append({
                'num': s_num,
                'name': s_name[:200],
                'session_type': session_type,
                'duration': duration,
                'basic_level': basic_level,
                'goals': goals,
                'focus': focus,
                'topics': matched_topics
            })

        # Запис в базата данни в транзакция
        if replace_existing:
            with transaction.atomic():
                Session.objects.filter(course=subject).delete()
                for s_data in cleaned_sessions:
                    new_session = Session.objects.create(
                        course=subject,
                        num=s_data['num'],
                        name=s_data['name'],
                        session_type=s_data['session_type'],
                        duration=s_data['duration'],
                        basic_level=s_data['basic_level'],
                        goals=s_data['goals'],
                        focus=s_data['focus']
                    )
                    for t_data in s_data['topics']:
                        SessionTopic.objects.create(
                            session=new_session,
                            topic=t_data['topic'],
                            description=t_data['description']
                        )
        else:
            with transaction.atomic():
                max_session_num = Session.objects.filter(course=subject).order_by('-num').values_list('num', flat=True).first() or 0
                for s_data in cleaned_sessions:
                    session_num = s_data['num']
                    if Session.objects.filter(course=subject, num=session_num).exists():
                        max_session_num += 1
                        session_num = max_session_num
                    else:
                        if session_num > max_session_num:
                            max_session_num = session_num

                    new_session = Session.objects.create(
                        course=subject,
                        num=session_num,
                        name=s_data['name'],
                        session_type=s_data['session_type'],
                        duration=s_data['duration'],
                        basic_level=s_data['basic_level'],
                        goals=s_data['goals'],
                        focus=s_data['focus']
                    )
                    for t_data in s_data['topics']:
                        SessionTopic.objects.create(
                            session=new_session,
                            topic=t_data['topic'],
                            description=t_data['description']
                        )

        # Презареждане и сериализиране на обновения списък с уроци
        topics_prefetch = Prefetch(
            'session_topics',
            queryset=SessionTopic.objects.select_related('topic').order_by('id')
        )
        updated_sessions = (
            Session.objects
            .filter(course=subject)
            .order_by('num', 'id')
            .prefetch_related(topics_prefetch)
        )
        serializer = SessionReadSerializer(updated_sessions, many=True)

        return Response({
            'message': f'Успешно бяха импортирани {len(cleaned_sessions)} урока по предмета.',
            'sessions': serializer.data
        }, status=status.HTTP_200_OK)


# ***************************
#     Импорт на план за урок
# ***************************

class SessionPlanImportView(APIView):
    """
    POST /api/sessions/<session_id>/import-plan/
    Приема JSON със структура на план за урок (точки, бележки, задачи, цели, фокус).
    """

    def post(self, request, session_id):
        session = get_object_or_404(Session, id=session_id)
        data = request.data

        if not data:
            return Response(
                {'detail': 'Моля, изпратете JSON данни за импорт на плана.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if isinstance(data, str):
            try:
                data = json.loads(data)
            except Exception as e:
                return Response(
                    {'detail': f'Невалиден JSON формат: {str(e)}'},
                    status=status.HTTP_400_BAD_REQUEST
                )

        replace_existing = True
        plan_dict = {}

        if isinstance(data, list):
            plan_dict = {'points': data}
            replace_existing = True
        elif isinstance(data, dict):
            replace_existing = data.get('replace_existing', True)
            if 'plan' in data and isinstance(data['plan'], dict):
                plan_dict = data['plan']
            else:
                plan_dict = data
        else:
            return Response(
                {'detail': 'Очаква се JSON обект или масив от точки.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        points_raw = plan_dict.get('points', [])
        notes_raw = plan_dict.get('notes', [])
        tasks_raw = plan_dict.get('tasks', [])
        goals_val = plan_dict.get('goals')
        focus_val = plan_dict.get('focus')

        if not isinstance(points_raw, list):
            return Response(
                {'detail': 'Полето "points" трябва да бъде списък (масив).'},
                status=status.HTTP_400_BAD_REQUEST
            )

        if not points_raw and not notes_raw and not tasks_raw and not goals_val and not focus_val:
            return Response(
                {'detail': 'Предоставеният JSON не съдържа точки от плана, бележки или задачи.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Валидация и изчистване на точките
        cleaned_points = []
        for idx, p_data in enumerate(points_raw, start=1):
            if not isinstance(p_data, dict):
                continue
            name = str(p_data.get('name', '')).strip()
            if not name:
                name = f'Точка {idx}'
            try:
                num = int(p_data.get('num', idx))
            except (TypeError, ValueError):
                num = idx
            try:
                duration = int(p_data.get('duration', 10))
                if duration < 1:
                    duration = 1
                elif duration > 270:
                    duration = 270
            except (TypeError, ValueError):
                duration = 10
            description = str(p_data.get('description', '')).strip()
            content = str(p_data.get('content', '')).strip()

            cleaned_points.append({
                'num': num,
                'name': name,
                'description': description,
                'duration': duration,
                'content': content
            })

        # Валидация на бележките
        cleaned_notes = []
        for idx, n_data in enumerate(notes_raw, start=1):
            if not isinstance(n_data, dict):
                continue
            name = str(n_data.get('name', '')).strip()
            if not name:
                name = f'Бележка {idx}'
            try:
                num = int(n_data.get('num', idx))
            except (TypeError, ValueError):
                num = idx
            point_num = n_data.get('point_num') if 'point_num' in n_data else n_data.get('point')
            if point_num is not None:
                try:
                    point_num = int(point_num)
                except (TypeError, ValueError):
                    point_num = None
            content = str(n_data.get('content', '')).strip()

            cleaned_notes.append({
                'num': num,
                'name': name,
                'point_num': point_num,
                'content': content
            })

        # Валидация на задачите
        cleaned_tasks = []
        for idx, t_data in enumerate(tasks_raw, start=1):
            if not isinstance(t_data, dict):
                continue
            name = str(t_data.get('name', '')).strip()
            if not name:
                name = f'Задача {idx}'
            try:
                num = int(t_data.get('num', idx))
            except (TypeError, ValueError):
                num = idx
            point_num = t_data.get('point_num') if 'point_num' in t_data else t_data.get('point')
            if point_num is not None:
                try:
                    point_num = int(point_num)
                except (TypeError, ValueError):
                    point_num = None
            condition = str(t_data.get('condition', '')).strip()
            answer = str(t_data.get('answer', '')).strip()

            cleaned_tasks.append({
                'num': num,
                'name': name,
                'point_num': point_num,
                'condition': condition,
                'answer': answer
            })

        # Запис в базата данни в транзакция
        with transaction.atomic():
            if replace_existing:
                SessionNote.objects.filter(session=session).delete()
                SessionTask.objects.filter(session=session).delete()
                SessionPoint.objects.filter(session=session).delete()

                if goals_val is not None and str(goals_val).strip():
                    session.goals = str(goals_val).strip()
                if focus_val is not None and str(focus_val).strip():
                    session.focus = str(focus_val).strip()
                session.save()

                # Създаване на точки
                point_map = {}
                for p_data in cleaned_points:
                    pt_obj = SessionPoint.objects.create(
                        session=session,
                        num=p_data['num'],
                        name=p_data['name'],
                        description=p_data['description'],
                        duration=p_data['duration'],
                        content=p_data['content']
                    )
                    point_map[p_data['num']] = pt_obj

                # Създаване на бележки
                for n_data in cleaned_notes:
                    pt_obj = point_map.get(n_data['point_num'])
                    SessionNote.objects.create(
                        session=session,
                        point=pt_obj,
                        num=n_data['num'],
                        name=n_data['name'],
                        content=n_data['content']
                    )

                # Създаване на задачи
                for t_data in cleaned_tasks:
                    pt_obj = point_map.get(t_data['point_num'])
                    SessionTask.objects.create(
                        session=session,
                        point=pt_obj,
                        num=t_data['num'],
                        name=t_data['name'],
                        condition=t_data['condition'],
                        answer=t_data['answer']
                    )
            else:
                # Append режим
                if goals_val is not None and str(goals_val).strip() and not session.goals:
                    session.goals = str(goals_val).strip()
                if focus_val is not None and str(focus_val).strip() and not session.focus:
                    session.focus = str(focus_val).strip()
                session.save()

                max_point_num = SessionPoint.objects.filter(session=session).order_by('-num').values_list('num', flat=True).first() or 0
                point_map = {}
                for p_data in cleaned_points:
                    p_num = p_data['num']
                    if SessionPoint.objects.filter(session=session, num=p_num).exists():
                        max_point_num += 1
                        p_num = max_point_num
                    else:
                        if p_num > max_point_num:
                            max_point_num = p_num

                    pt_obj = SessionPoint.objects.create(
                        session=session,
                        num=p_num,
                        name=p_data['name'],
                        description=p_data['description'],
                        duration=p_data['duration'],
                        content=p_data['content']
                    )
                    point_map[p_data['num']] = pt_obj

                max_note_num = SessionNote.objects.filter(session=session).order_by('-num').values_list('num', flat=True).first() or 0
                for n_data in cleaned_notes:
                    n_num = n_data['num']
                    if SessionNote.objects.filter(session=session, num=n_num).exists():
                        max_note_num += 1
                        n_num = max_note_num
                    else:
                        if n_num > max_note_num:
                            max_note_num = n_num

                    pt_obj = point_map.get(n_data['point_num'])
                    SessionNote.objects.create(
                        session=session,
                        point=pt_obj,
                        num=n_num,
                        name=n_data['name'],
                        content=n_data['content']
                    )

                max_task_num = SessionTask.objects.filter(session=session).order_by('-num').values_list('num', flat=True).first() or 0
                for t_data in cleaned_tasks:
                    t_num = t_data['num']
                    if SessionTask.objects.filter(session=session, num=t_num).exists():
                        max_task_num += 1
                        t_num = max_task_num
                    else:
                        if t_num > max_task_num:
                            max_task_num = t_num

                    pt_obj = point_map.get(t_data['point_num'])
                    SessionTask.objects.create(
                        session=session,
                        point=pt_obj,
                        num=t_num,
                        name=t_data['name'],
                        condition=t_data['condition'],
                        answer=t_data['answer']
                    )

        # Презареждане и връщане на резултата
        points_qs = SessionPoint.objects.filter(session=session).order_by('num', 'id')
        notes_qs = SessionNote.objects.filter(session=session).order_by('num', 'id')
        tasks_qs = SessionTask.objects.filter(session=session).order_by('num', 'id')

        return Response({
            'message': f'Успешно бяха импортирани {len(cleaned_points)} точки, {len(cleaned_notes)} бележки и {len(cleaned_tasks)} задачи към занятието.',
            'session': SessionWriteSerializer(session).data,
            'points': SessionPointSerializer(points_qs, many=True).data,
            'notes': SessionNoteSerializer(notes_qs, many=True).data,
            'tasks': SessionTaskSerializer(tasks_qs, many=True).data
        }, status=status.HTTP_200_OK)
