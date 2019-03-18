from django import forms
from . import models

class SignInForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)


class StudentSignUpForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
    password_reenter = forms.CharField(label='Re-enter Password', max_length=100, widget=forms.PasswordInput)


class InstitutionSignUpForm(forms.Form):
    institution_name = forms.CharField(label='Institution Name', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
    password_reenter = forms.CharField(label='Re-enter Password', max_length=100, widget=forms.PasswordInput)


class ProgramSearchForm(forms.Form):
    university_name = forms.CharField(label='University Name', max_length=100)
    degree_type = forms.CharField(label='Degree Type', max_length=100)
    major = forms.CharField(label='Major', max_length=100)


class ProgramCreateForm(forms.Form):
    university_name = forms.CharField(label='University Name', max_length=100)
    degree_type = forms.CharField(label='Degree Type', max_length=100)
    major = forms.CharField(label='Major', max_length=100)
    tests = forms.BooleanField(label='Standardized Test')
    statement_of_purpose = forms.BooleanField(label='Statement of Purpose')
    personal_statement = forms.BooleanField(label='Personal Statement')
    references = forms.BooleanField(label='References')
    official_transcript = forms.BooleanField(label='Official Transcript')


class FeedbackForm(forms.Form):
    school_name = forms.CharField(label='Former Institution Name', max_length=100)
    gpa = forms.FloatField(label='GPA')
    tests = forms.CharField(label='Standardized Test', max_length=100)
    reference = forms.CharField(label='Reference', max_length=100)
    research = forms.CharField(label='Research', max_length=100)
    publication = forms.CharField(label='Publication', max_length=100)
    other_comment = forms.CharField(label='Other Comment', max_length=100)
    admission_result = forms.ChoiceField(label='Admission Result', choices=(
                                                                        ("ACCEPTED", "Accepted"),
                                                                        ("WAITLISTED", "Waitlisted"),
                                                                        ("DENIED", 'Denied')
                                                                        ))
