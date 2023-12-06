from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .forms import CustomAuthenticationForm
from opentelemetry import trace


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

                # Instrumentation avec OpenTelemetry
                tracer = trace.get_tracer(__name__)
                with tracer.start_as_current_span("login") as span:
                    span.set_attribute("user_first_name", user.first_name)
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
