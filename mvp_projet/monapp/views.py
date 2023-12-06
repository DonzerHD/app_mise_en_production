from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm

def index(request):
    return render(request, 'monapp/index.html')

def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], 
                                password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('welcome')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'monapp/login.html', {'form': form})

@login_required
def welcome_view(request):
    return render(request, 'monapp/welcome.html')

def logout_view(request):
    logout(request)
    return redirect('index')
