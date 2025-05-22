from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.http import datetime
import requests
# Create your views here.

def index(request):
    return render(request,'frontend/index.html',context={
        'year' : datetime.datetime.now().year,
        'title' : 'Topsis Home',
        })
def dashboard(request):
    if not request.session.get('token'):
        return redirect('frontend:login')
    return render(request, 'frontend/dashboard.html', context={
        'title' : 'dashboard'
        })

def signup(request):
    if request.session.get('token'):
        return redirect('frontend:dashboard')
    if request.method == 'POST' :
        nama_lengkap = request.POST.get('nama_lengkap')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        # headers = {'Content-Type': 'application/json'}
        payload = {
                'nama_lengkap' : nama_lengkap,
                'email' : email,
                'password' : password,
                'confirm_password' : confirm_password
                }
        try :
            response = requests.post('http://localhost:8080/api/signup', json=payload)
            if response.status_code == 200 :
                json_response = response.json()
                message = json_response.get('message', 'Succes')
            else:
                message = f'Error {response.status_code}'
        except Exception as e:
            message = f'terjadi Error{e}'

        return render(request, 'frontend/signup.html', context={
            'title' : 'signup',
            'message' : message
            })
    else:
        return render(request, 'frontend/signup.html', context={
            'title' : 'signup',
            })

def login(request):
    if request.session.get('token'):
        return redirect('frontend:dashboard')
    if request.method == 'POST' :
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        payload = {
                'email' : email,
                'password' : password,
                'confirm_password' : confirm_password
                } 
        try:
            # headers = {'Content-Type': 'application/json'}
            response = requests.post(
                'http://localhost:8080/api/login',
                json=payload
            )

            if response.status_code == 200 :
                token = response.cookies.get('Authorization')
                if token:
                    request.session['token'] = token
                    return redirect('frontend:dashboard')
                else:
                    message = 'Login Gagal'
            else:
                message = f'login gagal: {response.status_code}'
        except Exception as e:
            message = f'Error : {e}'
        return render(request, 'frontend/login.html', context={
            'title' : 'login',
            'message' : message,
            })
    return render(request, 'frontend/login.html', context={
        'title' : 'login'
        })

def logout(request):
    if request.session.get('token'):
        del request.session['token']
    return redirect('frontend:login')


