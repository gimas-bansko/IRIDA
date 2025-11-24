from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.models import User
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view, permission_classes

from django.views.decorators.csrf import csrf_protect, csrf_exempt
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics, status
from .serializers import *
from rest_framework.permissions import IsAuthenticated
from django.db.models import Prefetch

from django.core.files.storage import default_storage
from django.conf import settings
from django.core.files.base import ContentFile


@csrf_protect
def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next') or 'home'
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('home')
    else:
        form = AuthenticationForm(request)

    # Подавам form за да покажа грешки/values без да променям визията
    return render(request, 'main/sign-in.html', {'form': form, 'next': next_url})

def sign_in(request):
    return render(request, 'main/sign-in.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def make_user_context(r):
    user = r.user
    user_profile = user.userprofile
    schools = School.objects.all()
    specialty = user_profile.speciality
    subject = user_profile.subject
    session = user_profile.session

    context = {
        'user_nick': user.username,
        'user_name': user.first_name+' '+user.last_name,
        'user_first_name': user.first_name,
        'user_level': USER_LEVEL[user_profile.access_level-1][1],
        'user_profile': user_profile,
        'schools': schools,
        'specialities': user_profile.school.specialities.all(),
        'specialty': specialty,
        'subject': subject,
        'session': session,
    }
    return context

def welcome_view(request):
    context = make_user_context(request)
    return render(request, 'main/welcome.html', context)

def subjects_list_view(request):
    context = make_user_context(request)
    return render(request, 'main/subjects.html', context)

def users_list_view(request):
    context = make_user_context(request)
    return render(request, 'main/users.html', context)

def specialties_list_view(request):
    context = make_user_context(request)
    return render(request, 'main/specialties.html', context)

def schools_list_view(request):
    context = make_user_context(request)
    return render(request, 'main/schools.html', context)

def course_goals_view(request):
    context = make_user_context(request)
    return render(request, 'main/course_goals.html', context)

def course_units_view(request):
    context = make_user_context(request)
    return render(request, 'main/course_units.html', context)

def course_lessons_view(request):
    context = make_user_context(request)
    return render(request, 'main/course_lessons.html', context)

def session_home_view(request):
    context = make_user_context(request)
    return render(request, 'main/session_home.html', context)

def session_list_view(request):
    context = make_user_context(request)
    return render(request, 'main/session_list.html', context)

def session_main_view(request):
    context = make_user_context(request)
    return render(request, 'main/session_main.html', context)

def lesson_view(request, session_id):
    user = request.user
    user_profile = user.userprofile
    session = Session.objects.get(id=session_id)
    user_profile.session = session
    user_profile.save()

    context = make_user_context(request)
    context['session_id'] = session_id
    return render(request, 'main/lesson.html', context)

def test_view(request, session_id):
    user = request.user
    user_profile = user.userprofile
    session = Session.objects.get(id=session_id)
    user_profile.session = session
    user_profile.save()

    context = make_user_context(request)
    context['session_id'] = session_id
    return render(request, 'main/test.html', context)

""" 
***************************************
               API
***************************************
"""
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

# четене/обновяване на специалност
@api_view(['GET', 'PUT'])
def specialty_detail(request, specialty_id, school_id=None):
    # GET
    if request.method == 'GET':
        if int(specialty_id) == 0:
            # По избор: върнете празен шаблон за форми
            return Response({
                'id': 0,
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
        sp = request.data.get('sb') or request.data.get('subject_id')

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

# задаване на предмет по подразбиране
@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def set_course(request, sb=None):
    user = request.user
    user_profile = user.userprofile

    # Ако искате да вземете sb от body при POST
    if request.method == 'POST':
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

# Раздели и теми
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
@csrf_exempt
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

class SessionNotesForSessionView(generics.ListAPIView):
    serializer_class = SessionNoteSerializer

    def get_queryset(self):
        session_id = self.kwargs['session_id']
        get_object_or_404(Session, id=session_id)
        return SessionNote.objects.filter(session_id=session_id).order_by('num', 'id')

@api_view(['POST'])
@csrf_exempt
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

# -------- Tasks --------
class SessionTasksForSessionView(generics.ListAPIView):
    serializer_class = SessionTaskSerializer

    def get_queryset(self):
        session_id = self.kwargs['session_id']
        get_object_or_404(Session, id=session_id)
        return SessionTask.objects.filter(session_id=session_id).order_by('num', 'id')

@api_view(['POST'])
@csrf_exempt
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

@api_view(['POST'])
@csrf_exempt
def ckeditor_image_upload(request):
    """
    Expects: multipart/form-data with 'upload' field (CKEditor default)
    Returns: { "url": "<absolute-or-relative-url>" }
    """
    f = request.FILES.get('upload')
    if not f:
        return Response({'error': 'No file'}, status=400)

    # записваме файла
    path = default_storage.save(f"session_pics/{f.name}", ContentFile(f.read()))
    url = default_storage.url(path)  # напр. /media/session_pics/...

    # CKEditor expects { url }
    return Response({'url': url}, status=201)

@api_view(['POST'])
@csrf_exempt
def tinymce_image_upload(request):
    """
    TinyMCE default handler expects:
        - multipart/form-data with 'file'
        - Response: { "location": "<absolute-or-relative-url>" }
    """

    f = request.FILES.get('file')
    if not f:
        return Response({'error': 'No file'}, status=400)

    # Запис на файл в MEDIA
    path = default_storage.save(f"session_pics/{f.name}", ContentFile(f.read()))
    url = default_storage.url(path)  # напр. /media/session_pics/...

    # Върни във формат, който TinyMCE очаква
    return Response({'location': url}, status=201)

class UserListView(APIView):
    def get(self, request, sc, lvl):
        # Извличане на параметрите за филтриране от заявката
        school_id = sc
        level = lvl
        # Филтриране на потребителите
        users = User.objects.filter(
            userprofile__school=school_id,
            userprofile__access_level__gt=level,
        )
        # Сериализиране на резултатите
        serializer = UserReadSerializer(users, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class UserListCreateView(generics.ListCreateAPIView):
    """
    GET: (по избор) връща всички или филтрирани по query params:
        ?school=<id>&min_level=<n>&max_level=<m>
    POST: създава потребител {username, password?, email, first_name, last_name, userprofile{...}}
    """
    queryset = User.objects.all().select_related('userprofile').order_by('id')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        return UserReadSerializer if self.request.method == 'GET' else UserSerializer

    def get_queryset(self):
        qs = super().get_queryset()
        school = self.request.query_params.get('school')
        min_level = self.request.query_params.get('min_level')
        max_level = self.request.query_params.get('max_level')

        if school:
            qs = qs.filter(userprofile__school=school)
        if min_level:
            qs = qs.filter(userprofile__access_level__gte=min_level)
        if max_level:
            qs = qs.filter(userprofile__access_level__lte=max_level)
        return qs

class UserRetrieveUpdateDestroyView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all().select_related('userprofile')
    permission_classes = [IsAuthenticated]

    def get_serializer_class(self):
        # GET -> Read; PUT/PATCH -> Write; DELETE -> няма тяло
        return UserReadSerializer if self.request.method == 'GET' else UserSerializer

