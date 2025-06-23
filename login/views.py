# Create your views here.
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required


def login_view(request):
    if request.user.is_authenticated:
        return redirect('inicio')
        
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                try:
                    if hasattr(user, 'cliente'):
                        return redirect('inicio')  # Cliente ve el home
                    elif hasattr(user, 'operadorsistema'):
                        # Cambiamos esta línea para usar la URL correcta del operador
                        return redirect('/operador/')  # URL absoluta al dashboard de operador
                    elif hasattr(user, 'directivo'):
                        return redirect('vista_directivo')
                except Exception as e:
                    print(f"Error en redirección: {e}")  # Para debugging
                return redirect('inicio')
    else:
        form = AuthenticationForm()
    return render(request, 'login/login.html', {'form': form})

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def home(request):
    return HttpResponse(f"Hola, {request.user.username}! Estás logueado.")

@login_required
def operador_dashboard(request):
    return render(request, 'operador/dashboard.html')

@login_required
def vista_directivo(request):
    return render(request, 'reporte/vista_directivo.html')