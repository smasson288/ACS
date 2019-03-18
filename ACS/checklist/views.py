from django.shortcuts import render, HttpResponseRedirect
from .forms import *


def index(request):
    return render(request, 'index.html')


def login(request):
    if request.method == 'POST':
        form = SignInForm(request.POST)
        if form.is_valid():
            #try to log user in
            return HttpResponseRedirect('/checklist/')
    else:
        form = SignInForm()
    return render(request, 'login.html', {'form': form})


def studentCreateAccount(request):
    if request.method == 'POST':
        form = StudentSignUpForm(request.POST)
        if form.is_valid():
            #try to sign user up
            return HttpResponseRedirect('/login/')
    else:
        form = StudentSignUpForm()
    return render(request, 'studentCreateAccount.html', {'form': form})


def staffCreateAccount(request):
    return render(request, 'staffCreateAccount.html')


def checklist(request):
    return render(request, 'checklist.html')


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
