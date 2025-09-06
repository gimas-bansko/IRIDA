from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect, get_object_or_404
from rest_framework.decorators import api_view, permission_classes

from django.views.decorators.csrf import csrf_protect
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .serializers import *
from rest_framework import status
from rest_framework.permissions import IsAuthenticated


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

    # Подавам form за да покаа грешки/values без да променям визията
    return render(request, 'main/sign-in.html', {'form': form, 'next': next_url})

def sign_in(request):
    return render(request, 'main/sign-in.html')

def logout_view(request):
    logout(request)
    return redirect('login')

def welcome_view(request):
    user = request.user
    user_profile = user.userprofile
    schools = School.objects.all()

    context = {
        'tab_title': 'начало',
        'user_nick': user.username,
        'user_name': user.first_name+' '+user.last_name,
        'user_first_name': user.first_name,
        'user_level': USER_LEVEL[user_profile.access_level-1][1],
        'user_profile': user_profile,
        'schools': schools,
        'specialities': user_profile.school.specialities.all(),
    }
    print(f'context={context}')
    return render(request, 'main/welcome.html', context)

def subjects_list_view(request):
    user = request.user
    user_profile = user.userprofile
    specialty = user_profile.speciality
    subject = user_profile.subject

    context = {
        'user_nick': user.username,
        'user_name': user.first_name+' '+user.last_name,
        'user_level': USER_LEVEL[user_profile.access_level-1][1],
        'user_profile': user_profile,
        'specialty': specialty,
        'subject': subject,
        }

    print(f'context={context}')
    return render(request, 'main/subjects.html', context)

def specialties_list_view(request):
    user = request.user
    user_profile = user.userprofile
    context = {
        'user_nick': user.username,
        'user_name': user.first_name+' '+user.last_name,
        'user_level': USER_LEVEL[user_profile.access_level-1][1],
        'user_profile': user_profile,
        }
    print(f'context={context}')
    return render(request, 'main/specialties.html', context)

def schools_list_view(request):
    user = request.user
    user_profile = user.userprofile
    context = {
        'user_nick': user.username,
        'user_name': user.first_name+' '+user.last_name,
        'user_level': USER_LEVEL[user_profile.access_level-1][1],
        'user_profile': user_profile,
        }
    print(f'context={context}')
    return render(request, 'main/schools.html', context)

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
            'speciality': user_profile.speciality.id if user_profile.speciality else 0,
            'grade_section': user_profile.grade_section.id if user_profile.grade_section else 0,
            'subject': user_profile.subject.id if user_profile.subject else 0,
            }
        return Response(context)

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


# изпобор на специалност по подразбиране
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
