
from django.urls import path
from . import views

app_name = 'checklist'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/', views.login, name='login'),
    path('studentCreateAccount/', views.studentCreateAccount, name='studentCreateAccount'),
    path('staffCreateAccount/', views.staffCreateAccount, name='staffCreateAccount'),
    path('checklist/', views.checklist, name='checklist'),
    path('search/', views.search, name='search'),
    path('program/', views.program, name='program'),
    path('createProgram/', views.createProgram, name='createProgram'),
    path('feedback/', views.feedback, name='feedback')
]
