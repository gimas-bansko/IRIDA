"""
API за контекста на текущия потребител: кой е, и какви са му избраните
по подразбиране училище / специалност / предмет / клас / занятие.
"""

from django.shortcuts import get_object_or_404
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from ..constants import USER_LEVEL
from ..models import Session, Specialty, Subject
from ..serializers import UserProfileExpandedSerializer


class UserDataAPIView(APIView):
    def get(self, request):
        user = request.user
        user_profile = user.userprofile
        context = {
            'user_id': user.id,
            'user_nick': user.username,
            'user_name': user.first_name + ' ' + user.last_name,
            'user_level_text': USER_LEVEL[user_profile.access_level - 1][1],
            'user_level_num': user_profile.access_level,
            'school':  user_profile.school.id if user_profile.school else 0,
            'specialty': user_profile.speciality.id if user_profile.speciality else 0,
            'grade': user_profile.grade,
            'section': user_profile.section,
            'subject': user_profile.subject.id if user_profile.subject else 0,
            'session': user_profile.session.id if user_profile.session else 0,
            }
        return Response(context)


class UserDataExpandedAPIView(APIView):
    def get(self, request):
        user = request.user
        up = user.userprofile  # имаш сигнал за auto-create

        data = {
            'user_id': user.id,
            'user_nick': user.username,
            'user_name': f'{user.first_name} {user.last_name}'.strip(),
            'user_level_num': up.access_level,
            'user_level_text': USER_LEVEL[up.access_level - 1][1] if up.access_level else '',
            'profile': UserProfileExpandedSerializer(up).data,
        }
        return Response(data)


# избор на специалност по подразбиране
@api_view(['GET', 'POST'])  # позволяваме и POST, ако решите да не пращате id в URL
@permission_classes([IsAuthenticated])
def set_speciality(request, sp=None):
    user = request.user
    user_profile = user.userprofile

    # Ако искате да вземете sp от body при POST
    if request.method == 'POST':
        sp = request.data.get('sp') or request.data.get('specialty_id')

    # Валидация
    try:
        sp = int(sp) if sp is not None else 0
    except (TypeError, ValueError):
        return Response({'ok': False, 'error': 'Невалиден параметър sp'}, status=400)

    if sp > 0:
        specialty = get_object_or_404(Specialty, id=sp)
        user_profile.speciality = specialty
        user_profile.save()

    return Response({'ok': True})


# избор на предмет по подразбиране
@api_view(['GET', 'POST'])  # позволяваме и POST, ако решите да не пращате id в URL
@permission_classes([IsAuthenticated])
def set_subject(request, sb=None):
    user = request.user
    user_profile = user.userprofile

    # Ако искате да вземете sb от body при POST
    if request.method == 'POST':
        # BUG (запазено поведение): резултатът се присвоява на `sp`, а
        # надолу се ползва `sb` - тоест при POST без sb в URL нищо
        # не се сменя. Виж бележката в README.
        sp = request.data.get('sb') or request.data.get('subject_id')  # noqa: F841

    # Валидация
    try:
        sb = int(sb) if sb is not None else 0
    except (TypeError, ValueError):
        return Response({'ok': False, 'error': 'Невалиден параметър sb'}, status=400)

    if sb > 0:
        subject = get_object_or_404(Subject, id=sb)
        user_profile.subject = subject
        user_profile.save()

    return Response({'ok': True})


# избор на клас и паралелка по подразбиране
@api_view(['GET', 'POST'])  # позволяваме и POST, ако решите да не пращате id в URL
@permission_classes([IsAuthenticated])
def set_grade_section(request, gr=None, se=None):
    user = request.user
    user_profile = user.userprofile

    # Ако вземем gr и se от body при POST
    if request.method == 'POST':
        gr = request.data.get('gr') or request.data.get('grade')
        se = request.data.get('se') or request.data.get('section')

    user_profile.grade = gr
    user_profile.section = se
    user_profile.save()

    return Response({'ok': True})


# избор на занятие по подразбиране
@api_view(['GET', 'POST'])  # позволяваме и POST, ако решите да не пращате id в URL
@permission_classes([IsAuthenticated])
def set_session(request, se=None):
    user = request.user
    user_profile = user.userprofile

    # Ако искам да взема se от body при POST
    if request.method == 'POST':
        se = request.data.get('se') or request.data.get('session_id')

    # Валидация
    try:
        se = int(se) if se is not None else 0
    except (TypeError, ValueError):
        return Response({'ok': False, 'error': 'Невалиден параметър se'}, status=400)

    if se > 0:
        session = get_object_or_404(Session, id=se)
        user_profile.session = session
        user_profile.save()

    return Response({'ok': True})


# задаване на предмет по подразбиране
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def set_course(request, sb=None):
    user = request.user
    user_profile = user.userprofile

    # Ако искате да вземете sb от body при POST
    if request.method == 'POST':
        # BUG (запазено поведение): чете ключ 'sp' вместо 'sb'.
        # Виж бележката в README.
        sb = request.data.get('sp') or request.data.get('subject_id')

    # Валидация
    try:
        sb = int(sb) if sb is not None else 0
    except (TypeError, ValueError):
        return Response({'ok': False, 'error': 'Невалиден параметър sb'}, status=400)

    if sb > 0:
        subject = get_object_or_404(Subject, id=sb)
        user_profile.subject = subject
        user_profile.save()

    return Response({'ok': True})
