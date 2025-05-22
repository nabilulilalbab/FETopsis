from django.urls import path
from . import views

app_name='frontend'
urlpatterns = [
        path('', views.index, name='index'),
        path('signup/',views.signup, name='signup'),
        path('login/', views.login, name='login'),
        path('dashboard/', views.dashboard, name='dashboard'),
        path('logout/', views.logout, name='logout'),

        # TOPSIS URLs
        path('topsis/', views.topsis_calculate, name='topsis_calculate'),
        path('topsis/save/', views.topsis_save, name='topsis_save'),
        path('topsis/history/', views.topsis_history, name='topsis_history'),
        path('topsis/detail/<int:calculation_id>/', views.topsis_detail, name='topsis_detail'),
        ]
