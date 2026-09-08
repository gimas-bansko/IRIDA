"""
Вход и изход от системата.
"""

from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import redirect, render
from django.views.decorators.csrf import csrf_protect


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


def logout_view(request):
    logout(request)
    return redirect('login')


# ЗАСЕГА НЕ СЕ ПОЛЗВА: няма запис в urls.py. login_view прави същото,
# но и обработва формата.
def sign_in(request):
    return render(request, 'main/sign-in.html')
