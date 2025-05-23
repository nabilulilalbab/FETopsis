from django.http import JsonResponse
from django.shortcuts import redirect, render
from django.utils.http import datetime
import requests
import json

def is_logged_in(request):
    return bool(request.session.get('token'))

# Create your views here.
def index(request):
    return render(request,'frontend/index.html',context={
        'year': datetime.datetime.now().year,
        'is_logged_in': is_logged_in(request),
        'title' : 'Topsis Home',
        })

def dashboard(request):
    if not request.session.get('token'):
        return redirect('frontend:login')
    return render(request, 'frontend/dashboard.html', context={
        'title' : 'dashboard',
        'year': datetime.datetime.now().year,
        'is_logged_in': is_logged_in(request)
        })

def signup(request):
    if request.session.get('token'):
        return redirect('frontend:dashboard')
    if request.method == 'POST' :
        nama_lengkap = request.POST.get('nama_lengkap')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
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
            'message' : message,
            'year': datetime.datetime.now().year,
            'is_logged_in': is_logged_in(request)
            })
    else:
        return render(request, 'frontend/signup.html', context={
            'title' : 'signup',
            'year': datetime.datetime.now().year,
        'is_logged_in': is_logged_in(request)
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
            'year': datetime.datetime.now().year,
            'is_logged_in': is_logged_in(request)
            })
    return render(request, 'frontend/login.html', context={
        'title' : 'login',
        'year': datetime.datetime.now().year,
        'is_logged_in': is_logged_in(request)
        })

def logout(request):
    if request.session.get('token'):
        del request.session['token']
    return redirect('frontend:login')

def topsis_calculate(request):
    if not request.session.get('token'):
        return redirect('frontend:login')
    
    if request.method == 'POST':
        try:
            # Get form data
            criteria_names = request.POST.getlist('criteria_name[]')
            criteria_weights = request.POST.getlist('criteria_weight[]')
            criteria_types = request.POST.getlist('criteria_type[]')
            
            alternative_names = request.POST.getlist('alternative_name[]')
            
            # Build criteria
            criteria = []
            for i, name in enumerate(criteria_names):
                if name:  # Only add non-empty criteria
                    criteria.append({
                        'name': name,
                        'weight': float(criteria_weights[i]),
                        'type': criteria_types[i]
                    })
            
            # Build alternatives
            alternatives = []
            for i, alt_name in enumerate(alternative_names):
                if alt_name:  # Only add non-empty alternatives
                    values = {}
                    for j, crit_name in enumerate(criteria_names):
                        if crit_name:
                            field_name = f'alternative_{i}_{crit_name}'
                            value = request.POST.get(field_name)
                            if value:
                                values[crit_name] = float(value)
                    
                    if values:  # Only add if has values
                        alternatives.append({
                            'name': alt_name,
                            'values': values
                        })
            
            # Prepare payload
            payload = {
                'criteria': criteria,
                'alternatives': alternatives
            }
            
            # Send request to API
            # headers = {
            #     'Authorization': request.session.get('token'),
            #     'Content-Type': 'application/json'
            # }
            # 
            response = requests.post(
                'http://localhost:8080/api/topsis',
                json=payload,
                cookies={'Authorization': request.session.get('token')} 
            )
            
            if response.status_code == 200:
                result_data = response.json()
                # Store result in session for saving later
                request.session['topsis_result'] = result_data
                return render(request, 'frontend/topsis_result.html', {
                    'title': 'TOPSIS Result',
                    'result': result_data,
                    'original_criteria': criteria,
                    'original_alternatives': alternatives,
                    'year': datetime.datetime.now().year,
                    'is_logged_in': is_logged_in(request)
                })
            else:
                error_message = f'Error calculating TOPSIS: {response.status_code}'
                return render(request, 'frontend/topsis.html', {
                    'title': 'TOPSIS Calculator',
                    'error': error_message,
                    'year': datetime.datetime.now().year,
            'is_logged_in': is_logged_in(request)
                })
                
        except Exception as e:
            error_message = f'Error: {str(e)}'
            return render(request, 'frontend/topsis.html', {
                'title': 'TOPSIS Calculator',
                'error': error_message,
                'year': datetime.datetime.now().year,
            'is_logged_in': is_logged_in(request)
            })
    
    return render(request, 'frontend/topsis.html', {
        'title': 'TOPSIS Calculator',
        'year': datetime.datetime.now().year,
        'is_logged_in': is_logged_in(request)
    })

def topsis_save(request):
    if not request.session.get('token'):
        return redirect('frontend:login')
    
    if request.method == 'POST':
        try:
            name = request.POST.get('calculation_name')
            result_data = request.session.get('topsis_result')
            
            if not result_data:
                return JsonResponse({'success': False, 'message': 'No calculation result found'})
            
            # Prepare payload for save
            payload = {
                'name': name,
                'data': result_data.get('data', {})
            }
            
            # headers = {
            #     'Authorization': request.session.get('token'),
            #     'Content-Type': 'application/json'
            # }
            
            response = requests.post(
                'http://localhost:8080/api/topsis/save',
                json=payload,
                cookies={'Authorization': request.session.get('token')}
            )
            
            if response.status_code == 200:
                result = response.json()
                # Clear session result after saving
                if 'topsis_result' in request.session:
                    del request.session['topsis_result']
                return JsonResponse({
                    'success': True, 
                    'message': result.get('message', 'Saved successfully'),
                    'calculation_id': result.get('calculation_id')
                })
            else:
                return JsonResponse({'success': False, 'message': f'Error saving: {response.status_code}'})
                
        except Exception as e:
            return JsonResponse({'success': False, 'message': f'Error: {str(e)}'})
    
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

def topsis_history(request):
    if not request.session.get('token'):
        return redirect('frontend:login')
    
    try:
        headers = {
            'Authorization': request.session.get('token'),
        }
        
        response = requests.get(
            'http://localhost:8080/api/topsis/history',
            cookies={'Authorization': request.session.get('token')}
        )
        
        if response.status_code == 200:
            history_data = response.json()
            return render(request, 'frontend/topsis_history.html', {
                'title': 'TOPSIS History',
                'history': history_data.get('data', []),
                'year': datetime.datetime.now().year,
                'is_logged_in': is_logged_in(request)
            })
        else:
            error_message = f'Error fetching history: {response.status_code}'
            return render(request, 'frontend/topsis_history.html', {
                'title': 'TOPSIS History',
                'error': error_message,
                'history': [],
                'year': datetime.datetime.now().year,
                'is_logged_in': is_logged_in(request)
            })
            
    except Exception as e:
        error_message = f'Error: {str(e)}'
        return render(request, 'frontend/topsis_history.html', {
            'title': 'TOPSIS History',
            'error': error_message,
            'history': [],
            'year': datetime.datetime.now().year,
            'is_logged_in': is_logged_in(request)
        })

def topsis_detail(request, calculation_id):
    if not request.session.get('token'):
        return redirect('frontend:login')
    
    try:
        # headers  = {
            # 'Authorization': request.session.get('token'),
        # }
        
        response = requests.get(
            f'http://localhost:8080/api/topsis/{calculation_id}',
            cookies={'Authorization': request.session.get('token')}
        )
        
        if response.status_code == 200:
            detail_data = response.json()
            return render(request, 'frontend/topsis_detail.html', {
                'title': 'TOPSIS Detail',
                'detail': detail_data.get('data', {}),
                'year': datetime.datetime.now().year,
                'is_logged_in': is_logged_in(request)
            })
        else:
            error_message = f'Error fetching detail: {response.status_code}'
            return render(request, 'frontend/topsis_detail.html', {
                'title': 'TOPSIS Detail',
                'error': error_message,
                'detail': {},
                'year': datetime.datetime.now().year,
                'is_logged_in': is_logged_in(request)
            })
            
    except Exception as e:
        error_message = f'Error: {str(e)}'
        return render(request, 'frontend/topsis_detail.html', {
            'title': 'TOPSIS Detail',
            'error': error_message,
            'detail': {},
            'year': datetime.datetime.now().year,
        'is_logged_in': is_logged_in(request)
        })


