
from django.urls import path
from . import views

app_name = 'checklist'
urlpatterns = [
    path('', views.index, name='index'),
    path('login/<int:logout_request>', views.accLogin, name='login'),
    path('studentCreateAccount/', views.studentCreateAccount, name='studentCreateAccount'),
    path('staffCreateAccount/', views.staffCreateAccount, name='staffCreateAccount'),
    path('checklist/', views.checklist, name='checklist'),
    path('search/', views.search, name='search'),
    path('staff/', views.program, name='staff'),
    path('program/', views.program, name='program'),
    path('program/<int:program_id>', views.programDetail, name='detail_program'),
    path('addToChecklist/<int:requirement_id>', views.addToChecklist, name='addToChecklist'),
    path('createProgram/', views.createProgram, name='createProgram'),
    path('feedback/<int:checklist_id>', views.feedback, name='feedback')
]
