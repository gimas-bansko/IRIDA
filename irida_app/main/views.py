from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import generics
from .serializers import *
from rest_framework import status

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

def subjects_list_view(request):
    return render(request, 'main/subjects-list.html')

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
            'user_nick': user.username,
            'user_name': user.first_name + ' ' + user.last_name,
            'user_level_text': USER_LEVEL[user_profile.access_level - 1][1],
            'user_level_num': user_profile.access_level,
            'school':  user_profile.school.id if user_profile.school else 0,
            'grade':  user_profile.grade if user_profile.grade else 0,
            'section':  user_profile.section if user_profile.section else 0,
            'speciality': user_profile.speciality.id if user_profile.speciality else 0,
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
