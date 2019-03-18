from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import logout, login
from django.views.decorators.csrf import csrf_protect
from .forms import *
from .backends import *
from .models import *


def index(request):
    return render(request, 'index.html')

@csrf_protect
def accLogin(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            #try to log user in
            try:
                user = Staff.objects.get(username=username)
            except ObjectDoesNotExist:
                try:
                    user = Student.objects.get(username=username)
                except ObjectDoesNotExist:
                    messages.warning(request, 'username does not exist')
                    return render(request, 'login.html', {'form': SignInForm()})

            if not check_password(password, user.password):
                messages.warning(request, 'incorrect password, please try again')
                return render(request, 'login.html', {'form': SignInForm()})

            user = AuthBackend.authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)

            return HttpResponseRedirect('/checklist/')
    else:
        form = SignInForm()
    return render(request, 'login.html', {'form': form})


def studentCreateAccount(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            reenter = form.cleaned_data['password_reenter']

            username_count = len(Student.objects.filter(username=username))
            if username_count != 0:
                messages.warning(request, 'username is already taken')
                return render(request, 'studentCreateAccount.html')

            if password != reenter:
                messages.warning(request, 'passwords does not match')
                return render(request, 'studentCreateAccount.html')

            user = Student.objects.create_user(username, password)
            user.save()
            #user = Student.objects.create_user(username=username, first_name="firstname", last_name="lastname", password=password)


            return HttpResponseRedirect('/login/')
    else:
        form = StudentSignUpForm()
    return render(request, 'studentCreateAccount.html', {'form': form})


def staffCreateAccount(request):
    return render(request, 'staffCreateAccount.html', {'form': InstitutionSignUpForm()})


def checklist(request):
    if request.user.is_authenticated:
        username = request.user.username
        user_model = get_object_or_404(Student, pk=username)
        checklists = Checklist.objects.filter(Student_id=user_model.username)
        return render(request, 'checklist.html', {'user': user_model, 'checklists': checklists})
    else:
        return HttpResponseRedirect('/login/')



def search(request):
    if request.method == 'POST':
        form = ProgramSearchForm(request.POST)
        if form.is_valid():
            #search program in db
            return HttpResponseRedirect('/program/')
    form = ProgramSearchForm()

    return render(request, 'search.html', {'form': form})


def program(request):
    return render(request, 'program.html')

def programDetail(request, program_id):
    currentProgram = get_object_or_404(Program, pk=program_id)
    Requirements = Requirement.objects.filter(program_id=program_id)
    context = {'program': currentProgram, 'requirements': Requirements}
    return render(request, 'programDetail.html', context)

def createProgram(request):
    if request.method == 'POST':
        form = ProgramCreateForm(request.POST)
        if form.is_valid():
            #create a new program in db
            return HttpResponseRedirect('/checklist/')
    form = ProgramCreateForm()
    return render(request, 'createProgram.html', {'form': form})


def feedback(request):
    form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})
