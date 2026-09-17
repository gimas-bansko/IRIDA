"""
HTML страници (server-rendered). Данните за таблиците се дърпат
после през API-то от frontend/irida/js/*.

Всички view-та тук изискват логнат потребител - make_user_context()
разчита на request.user.userprofile.
"""

from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render

from ..constants import STUDENT, USER_LEVEL
from ..models import School, Session


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
        # ВНИМАНИЕ: user_profile.school е nullable - при потребител без
        # училище тук пада с AttributeError.
        'specialities': user_profile.school.specialities.all(),
        'specialty': specialty,
        'subject': subject,
        'session': session,
    }
    return context


@login_required
def welcome_view(request):
    user_profile = getattr(request.user, 'userprofile', None)
    if user_profile and user_profile.access_level == STUDENT:
        return redirect('student_lessons')
    context = make_user_context(request)
    return render(request, 'main/welcome.html', context)


@login_required
def student_lessons_view(request):
    context = make_user_context(request)
    return render(request, 'main/student_lessons.html', context)


@login_required
def subjects_list_view(request):
    context = make_user_context(request)
    return render(request, 'main/subjects.html', context)


@login_required
def users_list_view(request):
    context = make_user_context(request)
    return render(request, 'main/users.html', context)


@login_required
def specialties_list_view(request):
    context = make_user_context(request)
    return render(request, 'main/specialties.html', context)


@login_required
def schools_list_view(request):
    context = make_user_context(request)
    return render(request, 'main/schools.html', context)


@login_required
def school_day_view(request):
    context = make_user_context(request)
    return render(request, 'main/school_day.html', context)


@login_required
def course_goals_view(request):
    context = make_user_context(request)
    return render(request, 'main/course_goals.html', context)


@login_required
def course_units_view(request):
    context = make_user_context(request)
    return render(request, 'main/course_units.html', context)


@login_required
def course_lessons_view(request):
    context = make_user_context(request)
    return render(request, 'main/course_lessons.html', context)


@login_required
def session_home_view(request):
    context = make_user_context(request)
    return render(request, 'main/session_home.html', context)


@login_required
def session_list_view(request):
    context = make_user_context(request)
    return render(request, 'main/session_list.html', context)


@login_required
def session_main_view(request):
    context = make_user_context(request)
    return render(request, 'main/session_main.html', context)


# ЗАСЕГА НЕ СЕ ПОЛЗВА: в urls.py пътят 'session_main_old' сочи към
# session_main_view, не към това view. Значи нито то, нито шаблонът
# main/session_main_old.html се достигат.
@login_required
def session_main_view_old(request):
    context = make_user_context(request)
    return render(request, 'main/session_main_old.html', context)


@login_required
def lesson_view(request, session_id):
    user = request.user
    user_profile = user.userprofile
    session = Session.objects.get(id=session_id)
    user_profile.session = session
    user_profile.save()

    context = make_user_context(request)
    context['session_id'] = session_id
    return render(request, 'main/lesson.html', context)


@login_required
def attachments_list_view(request):
    context = make_user_context(request)
    return render(request, 'main/attachments.html', context)
