from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from django.contrib.auth import logout, login
from django.views.decorators.csrf import csrf_protect
from .forms import *
from .backends import *
from .models import *


def index(request):
    '''
    The view responsible for the index AKA the home page.
    Will check if a user has logged in yet.
    '''
    user = request.user
    if not user.is_anonymous:
        return render(request, 'index.html', {'anonymous': False,})
    else:
        return render(request, 'index.html', {'anonymous': True,})

@csrf_protect
def accLogin(request, logout_request):
    '''
    The view responsible for login.
    If a client successfully enters their username and password, the user will be authorized and login.
    They will then be redirected to the Checklist/staff homepage depending on which user they are.
    :param logout_request: 0 if login, 1 if logout
    '''
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            #try to log user in
            try:
                user = User.objects.get(username=username)
            except ObjectDoesNotExist:
                messages.warning(request, 'username does not exist')
                return render(request, 'login.html', {'form': form})

            if not check_password(password, user.password):
                messages.warning(request, 'incorrect password, please try again')
                return render(request, 'login.html', {'form': form})

            user = AuthBackend.authenticate(request, username=username, password=password)
            if user is not None:
                login(request,user)

            username = request.user.username
            user_model = get_object_or_404(User, pk=username)
            if user_model.school_id == -1:
                return HttpResponseRedirect('/checklist/')
            else:
                return HttpResponseRedirect('/staff/')
    else:
        # logout request 1 = true, 0 = false
        if logout_request == 1:
            logout(request)
        form = SignInForm()
    return render(request, 'login.html', {'form': form})

@csrf_protect
def studentCreateAccount(request):
    '''
    The view for creating a student account
    If form is correctly filled in by the client, then a student User object will be created
    and the client will be redirected to the login page.
    '''
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            reenter = form.cleaned_data['password_reenter']

            username_count = len(User.objects.filter(username=username))
            if username_count != 0:
                messages.warning(request, 'username is already taken')
                return render(request, 'studentCreateAccount.html', {'form': form})

            if password != reenter:
                messages.warning(request, 'passwords does not match')
                return render(request, 'studentCreateAccount.html', {'form': form})

            user = User.objects.create_user(username, password)
            user.save()

            return HttpResponseRedirect('/login/0')
    else:
        user = request.user
        if not user.is_anonymous:
            return HttpResponseRedirect('/')
        form = StudentSignUpForm()
    return render(request, 'studentCreateAccount.html', {'form': form})

@csrf_protect
def staffCreateAccount(request):
    '''
    The view for creating a staff account
    If form is correctly filled in by the client, then a staff User object will be created
    and the client will be redirected to the login page.
    If the staff enters a school that is not recognized, a new School object is created
    '''
    if request.method == 'POST':
        form = InstitutionSignUpForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            reenter = form.cleaned_data['password_reenter']
            school_name = form.cleaned_data['institution_name']

            username_count = len(User.objects.filter(username=username))
            if username_count != 0:
                messages.warning(request, 'username is already taken')
                return render(request, 'staffCreateAccount.html', {'form': form})

            if password != reenter:
                messages.warning(request, 'passwords does not match')
                return render(request, 'staffCreateAccount.html', {'form': form})

            try:
                school = School.objects.get(School_name=school_name)
                school_id = school.School_id
                school.Address_city = form.cleaned_data['address_city']
                school.Address_state = form.cleaned_data['address_state']
                school.Address_street = form.cleaned_data['address_street']
                school.Address_zipcode = form.cleaned_data['zipcode']
                school.save()
            except School.DoesNotExist:
                last_school = School.objects.filter().order_by('School_id').last()
                if last_school is not None:
                    school_id = last_school.School_id + 1
                else:
                    school_id = 0
                school = School(School_id=school_id, School_name=school_name, Address_street=form.cleaned_data['address_street'],
                                Address_city=form.cleaned_data['address_city'], Address_state=form.cleaned_data['address_state'],
                                Address_zipcode=form.cleaned_data['zipcode'])
                school.save()

            user = User.objects.create_user(username, password)
            user.school_id = school_id
            user.save()

            return HttpResponseRedirect('/login/0')
    else:
        user = request.user
        if not user.is_anonymous:
            return HttpResponseRedirect('/')
        form = InstitutionSignUpForm()
    return render(request, 'staffCreateAccount.html', {'form': form})


def addToChecklist(request, requirement_id):
    '''
    If a student user is logged in, the requirement will be converted into one of the
    user's checklist items.
    :param requirement_id: the id of the requirement to be added to the Checklist
    '''
    user = request.user
    if not user.is_anonymous:
        try:
            if not user.is_authenticated:
                return HttpResponseRedirect('/')
            elif user.school_id != -1:
                return HttpResponseRedirect('/staff/')
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/login/0')

    requirement = Requirement.objects.get(Requirement_id=requirement_id)
    checklist = Checklist.objects.filter(Student_id=request.user, Requirement_id__Program_id=requirement.Program_id)

    if len(checklist) is 0:
        last_checklist = Checklist.objects.filter().last()
        if last_checklist is None:
            checklist_id = 0
        else:
            checklist_id = last_checklist.Checklist_id + 1

        checklist = Checklist(checklist_id, requirement_id, request.user, requirement.Term_season,
                              requirement.Term_year, False, False, False, False, False)
        checklist.save()

    return HttpResponseRedirect('/checklist/')


@csrf_protect
def checklist(request):
    '''
    The view responsible for the checklist page, the main page for student users.
    The view will list all checklist items associated with the currently logged in student user.
    If not student, then redirected elsewhere.
    '''
    if request.method == 'POST':
        form = ChecklistForm(request.POST)
        if form.is_valid():
            try:
                checklist = Checklist.objects.get(Checklist_id=form.cleaned_data['checklist_id'])
                checklist.Tests = form.cleaned_data['tests']
                checklist.Statement_of_purpose = form.cleaned_data['statement_of_purpose']
                checklist.Personal_statement = form.cleaned_data['personal_statement']
                checklist.Recommendation_letters = form.cleaned_data['references']
                checklist.Transcript = form.cleaned_data['official_transcript']
                checklist.save()

                checklists = Checklist.objects.filter(Student_id=request.user.username)
                requirements = []

                # requirements = list, requirement_id, program_id
                for list in checklists:
                    requirements.append([list, Requirement.objects.get(Requirement_id=list.Requirement_id.Requirement_id), list.Requirement_id.Program_id])
            except ObjectDoesNotExist:
                return HttpResponseRedirect('/')
            return render(request, 'checklist.html', {'user': request.user, 'checklists': requirements})
        return HttpResponseRedirect('/login/0')
    else:
        user = request.user
        if not user.is_anonymous:
            try:
                if not user.is_authenticated:
                    return HttpResponseRedirect('/')
            except ObjectDoesNotExist:
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/login/0')

        # at this point verified that user is authenticated
        username = request.user.username
        user_model = get_object_or_404(User, pk=username)

        #if student
        if user_model.school_id == -1:
            checklists = Checklist.objects.filter(Student_id=username)
            requirements = []

            # requirements = list, requirement_id, program_id
            for list in checklists:
                requirements.append([list, Requirement.objects.get(Requirement_id=list.Requirement_id.Requirement_id), list.Requirement_id.Program_id])

            return render(request, 'checklist.html', {'user': user_model, 'checklists': requirements})

        #if staff, redirect to staff program page
        else:
            return HttpResponseRedirect('/staff/')

@csrf_protect
def search(request):
    '''
    The view responsible for searching for programs.
    After the client fills in the search form, the view will list all programs
    that match what was filled in. The programs are clickable and will take client to
    the specific program page.
    '''
    if request.method == 'POST':
        form = ProgramSearchForm(request.POST)
        if form.is_valid():
            university = form.cleaned_data['university_name']
            degree = form.cleaned_data['degree_type']
            major = form.cleaned_data['major']

            if not university and not degree and not major:
                messages.warning(request, 'Please fill in the search fields')
                return render(request, 'search.html', {'form': form})

            programs = Program.objects.filter(Degree__contains=degree, Major__contains=major, School_id__School_name__contains=university).all()
            if len(programs) == 0:
                messages.warning(request, 'there is no results based on your criteria')
                return render(request, 'search.html', {'form': form})
            return render(request, 'search.html', {'form': form, 'programs': programs})

    form = ProgramSearchForm()

    return render(request, 'search.html', {'form': form})

@csrf_protect
def staff(request):
    '''
    The view responsible for the homepage of staff users.
    Will show info about the staff's school and the programs offered by the school.
    '''
    user = request.user
    if not user.is_anonymous:
        try:
            if not user.is_authenticated:
                return HttpResponseRedirect('/')
            elif user.school_id == -1:
                return HttpResponseRedirect('/')
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/login/0')

    user = User.objects.get(username=user.username)
    requirements = Requirement.objects.filter(Created_by=user)

    return render(request, 'staff.html', {'school': School.objects.get(School_id=user.school_id), 'Requirements': requirements})


def deleteChecklist(request, checklist_id):
    '''
    A view that deletes the checklist item with the given id.
    :param checklist_id: the id of the checklist object to be deleted
    '''
    user = request.user
    if not user.is_anonymous:
        try:
            if not user.is_authenticated:
                return HttpResponseRedirect('/')
            elif user.school_id != -1:
                return HttpResponseRedirect('/staff/')
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/')
    else:
        return HttpResponseRedirect('/login/0')

    cl = get_object_or_404(Checklist, pk=checklist_id)
    if cl.Student_id == user:
        cl.delete()
    return HttpResponseRedirect('/checklist/')


@csrf_protect
def programDetailFilter(request, program_id):
    '''
    A view that filters and cleans up the feedback objects associated
    with the given program object
    :param program_id: the id of the program.
    '''
    if request.method == 'POST':
        form = StatisticFilterForm(request.POST)

        if form.is_valid():
            currentProgram = get_object_or_404(Program, pk=program_id)

            if form.cleaned_data['year'] is not None:
                feedbacks = Feedback.objects.filter(Checklist_id__Requirement_id__Program_id=program_id,
                                                    Feedback_status=form.cleaned_data['admission_result'],
                                                    Checklist_id__Term_season__contains=form.cleaned_data['term'],
                                                    Checklist_id__Term_Year__contains=form.cleaned_data['year'])
            else:
                feedbacks = Feedback.objects.filter(Checklist_id__Requirement_id__Program_id=program_id,
                                                    Feedback_status=form.cleaned_data['admission_result'],
                                                    Checklist_id__Term_season__contains=form.cleaned_data['term'])

            try:
                certified = Requirement.objects.filter(Certified=True, Program_id=currentProgram).latest(
                    'Requirement_id')
            except ObjectDoesNotExist:
                certified = None
            latest = Requirement.objects.filter(Program_id=currentProgram).latest('Requirement_id')

            context = {'program': currentProgram, 'certified': certified, 'latest': latest,
                       'form': RequirementCreateForm(), 'filter_form': StatisticFilterForm(),
                       'university': currentProgram.School_id, 'feedbacks': feedbacks}

            return render(request, 'programDetail.html', context)

    return HttpResponseRedirect('/program/' + str(program_id))


@csrf_protect
def programDetail(request, program_id):
    '''
    The view that provides a detailed version of a program object.
    If a student user is logged in, they will be able to add it to their
    personal checklist
    :param program_id: The id of the program to be looked at
    '''
    if request.method == 'POST':
        user = request.user
        if not user.is_anonymous:
            try:
                if not user.is_authenticated:
                    return HttpResponseRedirect('/')
                elif user.school_id != -1:
                    return HttpResponseRedirect('/staff/')
            except ObjectDoesNotExist:
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/login/0')

        # if add to checklist:
        checklist = Checklist.objects.filter(Student_id=request.user, Requirement_id__Program_id__Program_id=program_id)
        if len(checklist) is 0:
            last_checklist = Checklist.objects.filter().last()
            if last_checklist is None:
                checklist_id = 0
            else:
                checklist_id = last_checklist.Checklist_id + 1
            form = RequirementCreateForm(request.POST)
            if form.is_valid():
                last_requirement = Requirement.objects.filter().order_by('Requirement_id').last()
                if last_requirement is not None:
                    req_id = last_requirement.Requirement_id + 1
                else:
                    req_id = 0

                requirement = Requirement(Requirement_id=req_id, Program_id=Program.objects.get(Program_id=program_id),
                                          Created_by=User.objects.get(username=user.username),
                                          Term_season=form.cleaned_data['term'], Term_year=form.cleaned_data['year'],
                                          Recommendation_letters=form.cleaned_data['references'],
                                          Transcript=form.cleaned_data['official_transcript'],
                                          Tests=form.cleaned_data['tests'],
                                          Statement_of_purpose=form.cleaned_data['statement_of_purpose'],
                                          Personal_statement=form.cleaned_data['personal_statement'])
                requirement.save()
                checklist = Checklist(checklist_id, requirement.Requirement_id, request.user, requirement.Term_season,
                                  requirement.Term_year, False, False, False, False, False)
                checklist.save()

        return HttpResponseRedirect('/checklist/')

    currentProgram = get_object_or_404(Program, pk=program_id)
    feedbacks = Feedback.objects.filter(Checklist_id__Requirement_id__Program_id=program_id)

    try:
        certified = Requirement.objects.filter(Certified=True, Program_id=currentProgram).latest('Requirement_id')
    except ObjectDoesNotExist:
        certified = None
    latest = Requirement.objects.filter(Program_id=currentProgram).latest('Requirement_id')

    context = {'program': currentProgram, 'certified': certified,'latest': latest,
               'form': RequirementCreateForm(),'filter_form': StatisticFilterForm(),'university':currentProgram.School_id, 'feedbacks': feedbacks}

    return render(request, 'programDetail.html', context)


@csrf_protect
def createProgram(request):
    '''
    Allow users to create a Program object if the form is filled
    in without issues. If the entered school does not exist in the database,
    a new School object will be created.
    '''
    user = request.user
    if not user.is_anonymous:
        try:
            if not user.is_authenticated:
                return HttpResponseRedirect('/')
        except ObjectDoesNotExist:
            return HttpResponseRedirect('/staffCreateAccount/')
    else:
        return HttpResponseRedirect('/login/0')

    if request.method == 'POST':

        last_program = Program.objects.filter().order_by('Program_id').last()
        if last_program is None:
            program_id = 0
        else:
            program_id = last_program.Program_id + 1

        # if the program is created by students
        if user.school_id == -1:
            form = ProgramCreateForm(request.POST)
            if form.is_valid():
                #create a new program in db

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

                major = form.cleaned_data['major']
                degree = form.cleaned_data['degree_type']

                try:
                    existing_program = Program.objects.get(Major=major, Degree=degree, School_id_id=school_id)
                    program = existing_program
                except ObjectDoesNotExist:
                    program = Program(Program_id=program_id, Major=major, Degree=degree, School_id_id=school_id)
            else:
                return render(request, 'createProgram.html', {'form': ProgramCreateForm()})
        # if the program is created by staff
        else:
            form = StaffCreateProgramForm(request.POST)
            if form.is_valid():
                major = form.cleaned_data['major']
                degree = form.cleaned_data['degree_type']

                try:
                    existing_program = Program.objects.get(Major=major, Degree=degree, School_id_id=user.school_id)
                    program = existing_program
                    program.Certified = True
                except ObjectDoesNotExist:
                    program = Program(Program_id=program_id, Major=major, Degree=degree, School_id_id=user.school_id,
                                      Certified=True)
            else:
                return render(request, 'createProgram.html', {'form': StaffCreateProgramForm()})
        program.save()

        last_requirement = Requirement.objects.filter().order_by('Requirement_id').last()
        if last_requirement is not None:
            req_id = last_requirement.Requirement_id + 1
        else:
            req_id = 0

        requirement = Requirement(Requirement_id=req_id, Program_id=program, Created_by=User.objects.get(username=user.username),Term_season=form.cleaned_data['term'], Term_year=form.cleaned_data['year'], Recommendation_letters=form.cleaned_data['references'], Transcript=form.cleaned_data['official_transcript'],
                                  Tests=form.cleaned_data['tests'], Statement_of_purpose=form.cleaned_data['statement_of_purpose'], Personal_statement=form.cleaned_data['personal_statement'])
        if user.school_id != -1:
            requirement.Certified = True
        requirement.save()

        return HttpResponseRedirect('/checklist/')

    if user.school_id == -1:
        form = ProgramCreateForm()
    else:
        form = StaffCreateProgramForm()

    return render(request, 'createProgram.html', {'form': form})

@csrf_protect
def feedback(request, checklist_id):
    '''
    This view lets student users create new Feedback objects.
    Given a checklist, the user will fill out a form and create a new
    feedback about a program if their are no issues will filling out the form.
    If a non-student user is logged in, they will be redirected.
    :param checklist_id: the id of the checklist from which users are given feedback about
    '''
    if request.method == 'POST':
        print(request.POST)
        form = FeedbackForm(request.POST)
        # create a new program in db
        if form.is_valid():
            print(form.cleaned_data['admission_result'])
            print(form.cleaned_data['tests'])
            feedback = Feedback(Checklist_id=Checklist.objects.get(Checklist_id=checklist_id), Feedback_status=form.cleaned_data['admission_result'], Former_school=form.cleaned_data['school_name'], GPA=form.cleaned_data['gpa'],
                                Standardized_Test=form.cleaned_data['tests'], Recommendation=form.cleaned_data['reference'], Research=form.cleaned_data['research'],
                                Publication=form.cleaned_data['publication'], Other_comments=form.cleaned_data['other_comment'])
            feedback.save()
            return HttpResponseRedirect('/checklist/')
        else:
            return render(request, 'feedback.html', {'form': FeedbackForm, 'checklist_id': checklist_id})
    else:
        user = request.user
        if not user.is_anonymous:
            try:
                if not user.is_authenticated:
                    return HttpResponseRedirect('/')
                elif user.school_id == 1:
                    return HttpResponseRedirect('/')
            except ObjectDoesNotExist:
                return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/login/0')

        previous_feedback = Feedback.objects.filter(Checklist_id_id=checklist_id)
        checklist = Checklist.objects.get(Checklist_id=checklist_id)
        if checklist.Student_id.username != user.username:
            messages.warning(request, 'You can only provide feedback on your own checklist')
            return HttpResponseRedirect('/checklist/')
        elif len(previous_feedback) is not 0:
            messages.warning(request, 'You already provided feedback for this checklist')
            return HttpResponseRedirect('/checklist/')
        else:
            form = FeedbackForm()
            return render(request, 'feedback.html', {'form': form, 'checklist_id': checklist_id})
