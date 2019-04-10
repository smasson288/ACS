from django import forms


class SignInForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)


class StudentSignUpForm(forms.Form):
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
    password_reenter = forms.CharField(label='Re-enter Password', max_length=100, widget=forms.PasswordInput)


class InstitutionSignUpForm(forms.Form):
    institution_name = forms.CharField(label='Institution Name', max_length=100)
    address_street = forms.CharField(label='Street Address', max_length=100)
    address_city = forms.CharField(label='City', max_length=100)
    address_state = forms.CharField(label='State', max_length=100)
    zipcode = forms.CharField(label='Zip Code', max_length=100)
    username = forms.CharField(label='Username', max_length=100)
    password = forms.CharField(label='Password', max_length=100, widget=forms.PasswordInput)
    password_reenter = forms.CharField(label='Re-enter Password', max_length=100, widget=forms.PasswordInput)


class ProgramSearchForm(forms.Form):
    university_name = forms.CharField(label='University Name', max_length=100, required=False)
    degree_type = forms.CharField(label='Degree Type', max_length=100, required=False)
    major = forms.CharField(label='Major', max_length=100, required=False)


class ProgramCreateForm(forms.Form):
    university_name = forms.CharField(label='University Name', max_length=100)
    degree_type = forms.CharField(label='Degree Type', max_length=100)
    major = forms.CharField(label='Major', max_length=100)
    term = forms.CharField(label='Term', max_length=100)
    year = forms.IntegerField(label='Year')
    tests = forms.BooleanField(label='Standardized Test', required=False)
    statement_of_purpose = forms.BooleanField(label='Statement of Purpose', required=False)
    personal_statement = forms.BooleanField(label='Personal Statement', required=False)
    references = forms.BooleanField(label='References', required=False)
    official_transcript = forms.BooleanField(label='Official Transcript', required=False)


class StaffCreateProgramForm(forms.Form):
    degree_type = forms.CharField(label='Degree Type', max_length=100)
    major = forms.CharField(label='Major', max_length=100)
    term = forms.CharField(label='Term', max_length=100)
    year = forms.IntegerField(label='Year')
    tests = forms.BooleanField(label='Standardized Test', required=False)
    statement_of_purpose = forms.BooleanField(label='Statement of Purpose', required=False)
    personal_statement = forms.BooleanField(label='Personal Statement', required=False)
    references = forms.BooleanField(label='References', required=False)
    official_transcript = forms.BooleanField(label='Official Transcript', required=False)


class RequirementCreateForm(forms.Form):
    term = forms.CharField(label='Term', max_length=100)
    year = forms.IntegerField(label='Year')
    tests = forms.BooleanField(label='Standardized Test', required=False)
    statement_of_purpose = forms.BooleanField(label='Statement of Purpose', required=False)
    personal_statement = forms.BooleanField(label='Personal Statement', required=False)
    references = forms.BooleanField(label='References', required=False)
    official_transcript = forms.BooleanField(label='Official Transcript', required=False)


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


class StatisticFilterForm(forms.Form):
    term = forms.CharField(label='Term', max_length=100)
    year = forms.IntegerField(label='Year')
    admission_result = forms.ChoiceField(label='Admission Result', choices=(
        ("ACCEPTED", "Accepted"),
        ("WAITLISTED", "Waitlisted"),
        ("DENIED", 'Denied')
    ))


class ChecklistForm(forms.Form):
    checklist_id = forms.CharField(max_length=100)
    tests = forms.BooleanField(label='Standardized Test', required=False)
    statement_of_purpose = forms.BooleanField(label='Statement of Purpose', required=False)
    personal_statement = forms.BooleanField(label='Personal Statement', required=False)
    references = forms.BooleanField(label='References', required=False)
    official_transcript = forms.BooleanField(label='Official Transcript', required=False)