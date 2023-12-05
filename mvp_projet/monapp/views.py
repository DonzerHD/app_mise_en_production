from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm

# Create your views here.
def index(request):
    return render(request, 'monapp/index.html')


def login_view(request):
    if request.method == 'POST':
        form = CustomAuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect('welcome')  # Rediriger vers la page de bienvenue
    else:
        form = CustomAuthenticationForm()
    return render(request, 'monapp/login.html', {'form': form})

@login_required
def welcome_view(request):
    return render(request, 'monapp/welcome.html', {'first_name': request.user.first_name})
