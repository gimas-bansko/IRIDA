"""
API за урок/занятие: самите уроци, темите към тях, точките от плана
и бележките/задачите към точките.
"""

from django.db.models import Prefetch
from django.shortcuts import get_object_or_404
from django.views.decorators.csrf import csrf_exempt
from rest_framework import generics, status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from ..models import (
    Session,
    SessionAttachment,
    SessionNote,
    SessionPoint,
    SessionTask,
    SessionTopic,
    Subject,
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


# Списък на Session за даден Subject (с вложени SessionTopic и разгънат Topic)
class SubjectSessionsWithTopicsView(generics.ListAPIView):
    serializer_class = SessionReadSerializer

    def get_queryset(self):
        subject_id = self.kwargs['subject_id']
        get_object_or_404(Subject, id=subject_id)
        topics_prefetch = Prefetch(
            'session_topics',
            queryset=SessionTopic.objects.select_related('topic').order_by('id')
        )
        return (
            Session.objects
            .filter(course_id=subject_id)
            .order_by('num', 'id')
            .prefetch_related(topics_prefetch)
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
