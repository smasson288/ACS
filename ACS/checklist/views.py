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
                    return render(request, 'login.html', {'form': form})

            if not check_password(password, user.password):
                messages.warning(request, 'incorrect password, please try again')
                return render(request, 'login.html', {'form': form})

            user = AuthBackend.authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)

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
                return render(request, 'studentCreateAccount.html', {'form': form})

            if password != reenter:
                messages.warning(request, 'passwords does not match')
                return render(request, 'studentCreateAccount.html', {'form': form})

            user = Student.objects.create_user(username, password)
            user.save()

            return HttpResponseRedirect('/login/')
    else:
        form = StudentSignUpForm()
    return render(request, 'studentCreateAccount.html', {'form': form})

def staffCreateAccount(request):
    if request.method == 'POST':
        form = InstitutionSignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            reenter = form.cleaned_data['password_reenter']
            school_name = form.cleaned_data['institution_name']

            username_count = len(Staff.objects.filter(username=username))
            if username_count != 0:
                messages.warning(request, 'username is already taken')
                return render(request, 'staffCreateAccount.html', {'form': form})

            if password != reenter:
                messages.warning(request, 'passwords does not match')
                return render(request, 'staffCreateAccount.html', {'form': form})

            try:
                school = School.objects.get(School_name=school_name)
                school_id = school.School_id
            except School.DoesNotExist:
                last_school = School.objects.filter().order_by('School_id').last()
                if last_school is not None:
                    school_id = last_school.School_id + 1
                else:
                    school_id = 0
                school = School(School_id=school_id, School_name=school_name)
                school.save()

            user = Staff.objects.create_user(username, password, school_id)
            user.save()

            return HttpResponseRedirect('/login/')
    else:
        form = InstitutionSignUpForm()
    return render(request, 'staffCreateAccount.html', {'form': form})

@csrf_protect
def checklist(request):
    if request.method == 'POST':
        form = ChecklistForm(request.POST)

        if form.is_valid():
            checklist = Checklist.objects.get(Checklist_id=form.cleaned_data['checklist_id'])
            checklist.Tests = form.cleaned_data['tests']
            checklist.Statement_of_purpose = form.cleaned_data['statement_of_purpose']
            checklist.Personal_statement = form.cleaned_data['personal_statement']
            checklist.Recommendation_letters = form.cleaned_data['references']
            checklist.Transcript = form.cleaned_data['official_transcript']
            checklist.save()

            checklists = Checklist.objects.filter(Student_id=request.user.username)
            requirements = []

            for list in checklists:
                requirements.append([list, Requirement.objects.get(Requirement_id=list.Requirement_id.Requirement_id)])

            return render(request, 'checklist.html', {'user': request.user, 'checklists': requirements})
        return HttpResponseRedirect('/login/')
    else:
        if request.user.is_authenticated:
            username = request.user.username
            user_model = get_object_or_404(Student, pk=username)
            checklists = Checklist.objects.filter(Student_id=username)
            requirements = []

            for list in checklists:
                requirements.append([list, Requirement.objects.get(Requirement_id=list.Requirement_id.Requirement_id)])

            return render(request, 'checklist.html', {'user': user_model, 'checklists': requirements})
        else:
            return HttpResponseRedirect('/login/')


def search(request):
    if request.method == 'POST':
        form = ProgramSearchForm(request.POST)
        if form.is_valid():
            university = form.cleaned_data['university_name']
            degree = form.cleaned_data['degree_type']
            major = form.cleaned_data['major']

            programs = Program.objects.filter(Degree__contains=degree, Major__contains=major, School_id__School_name__contains=university).all()
            if len(programs) == 0:
                messages.warning(request, 'there is no results based on your criteria')
                return render(request, 'search.html', {'form': form})
            return render(request, 'search.html', {'form':form,'programs':programs})

    form = ProgramSearchForm()

    return render(request, 'search.html', {'form': form})


def program(request):
    return render(request, 'program.html')

@csrf_protect
def programDetail(request, program_id):
    if request.method == 'POST':
        # if add to checklist:
        checklist = Checklist.objects.filter(Student_id=request.user, Requirement_id__Program_id__Program_id=program_id)

        if len(checklist) is 0:
            last_checklist = Checklist.objects.filter().last()
            if last_checklist is None:
                checklist_id = 0
            else:
                checklist_id = last_checklist.Checklist_id + 1

            requirement = Requirement.objects.filter(Program_id=program_id).last()
            checklist = Checklist(checklist_id, requirement.Requirement_id, request.user, requirement.Term_season,
                                  requirement.Term_year, False, False, False, False, False)
            checklist.save()

        return HttpResponseRedirect('/checklist/')

    currentProgram = get_object_or_404(Program, pk=program_id)
    requirements = Requirement.objects.filter(Program_id=program_id)
    context = {'program': currentProgram, 'requirements': requirements}

    return render(request, 'programDetail.html', context)

@csrf_protect
def createProgram(request):
    user = request.user
    if not user.is_anonymous:
        try:
            if not user.is_authenticated:
                return HttpResponseRedirect('/')
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/staffCreateAccount/')
    else:
        return HttpResponseRedirect('/accLogin/')

    if request.method == 'POST':
        form = ProgramCreateForm(request.POST)
        if form.is_valid():
            #create a new program in db

            last_program = Program.objects.filter().order_by('Program_id').last()
            if last_program is None:
                program_id = 0
            else:
                program_id = last_program.Program_id + 1

            university_name = form.cleaned_data['university_name']
            try:
                school = School.objects.get(School_name=university_name)
                school_id = school.School_id
            except School.DoesNotExist:
                last_school = School.objects.filter().order_by('School_id').last()
                if last_school is not None:
                    school_id = last_school.School_id + 1
                else:
                    school_id = 0
                school = School(School_id=school_id, School_name=university_name)
                school.save()


            program = Program(Program_id=program_id, Major=form.cleaned_data['major'], Degree=form.cleaned_data['degree_type'], School_id_id=school_id)
            program.save()

            last_requirement = Requirement.objects.filter().order_by('Requirement_id').last()
            if last_requirement is not None:
                req_id = last_requirement.Requirement_id + 1
            else:
                req_id = 0

            requirement = Requirement(Requirement_id=req_id, Program_id=program,Term_season="Fall", Term_year=2019, Recommendation_letters=form.cleaned_data['references'], Transcript=form.cleaned_data['official_transcript'],
                                      Tests=form.cleaned_data['tests'], Statement_of_purpose=form.cleaned_data['statement_of_purpose'], Personal_statement=form.cleaned_data['personal_statement'])
            requirement.save()

            return HttpResponseRedirect('/checklist/')

    form = ProgramCreateForm()
    return render(request, 'createProgram.html', {'form': form})
def feedback(request):
    form = FeedbackForm()
    return render(request, 'feedback.html', {'form': form})
