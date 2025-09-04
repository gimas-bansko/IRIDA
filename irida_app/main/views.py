from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_protect
from .models import *
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response


@csrf_protect
def login_view(request):
    next_url = request.GET.get('next') or request.POST.get('next') or 'subject_list'
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect(next_url)
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
            'theme': user_profile.session_theme,
            'speciality': user_profile.speciality.id if user_profile.speciality else 0,
        }
        return Response(context)
