from django.db import models

class School(Models.Model):
    School_id = models.IntegerField(primary_key=True)
    School_desc = models.CharField(max_length=100)
    School_name = models.CharField(max_length=100)
    Address_street = models.CharField(max_length=100)
    Address_city = models.CharField(max_length=100)
    Address_state = models.CharField(max_length=100)
    Address_zipcode = models.CharField(max_length=100)

    def ___str___(self):
        return self.School_name

class Program(Models.Model):
    Program_id = models.IntegerField(primary_key=True)
    Program_name = models.CharField(max_length=100)
    College = models.CharField(max_length=100)
    Degree = models.CharField(max_length=100)
    School_id = models.ForeignKey(School, on_delete=models.CASCADE)
    Requirement_id = models.ForeignKey(Requirement, on_delete=models.CASCADE)

    def ___str___(self):
        return self.Program_name

class Feedback(Models.Model):
    Feedback_id = models.IntegerField(primary_Key=True)
    Checklist_id = models.ForeignKey(Checklist, on_delete=CASCADE)
    STATUS_CHOICES = (
        ACCEPTED,
        WAITLISTED,
        DENIED
    )
    Feedback_status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    GPA = models.IntegerField()
    Standardized_Test = models.IntegerField()
    Recommendation = models.CharField(max_length=1000)
    Research = models.CharField(max_length=1000)


class Staff(Models.Model):
    Staff_id = models.IntegerField(primary_Key=True)
    Staff_firstname = models.CharField(max_length=100)
    Staff_lastname = models.CharField(max_length=100)
    Staff_password = models.CharField(max_length=100)

class Requirement(Models.Model):
    Requirement_id = models.IntegerField(primary_key=True)
    Program_id = models.ForeignKey(Program, on_delete=models.CASCADE)
    Term_season = models.CharField(mox_length=6)
    Term_year = models.IntegerField()
    Recommendation_letters = models.BooleanField(default=False)
    Transcript = models.BooleanField(default=False)
    Tests = models.BooleanField(default=False)
    Statement_of_purpose = models.BooleanField(default=False)
    Personal_statement = models.BooleanField(default=False)

class Checklist(Models.Model):
    Checklist_id = models.IntegerField(primary_key=True)
    Requirement_id = models.ForeignKey(Requirement,id, on_delete=models.CASCADE)
    Student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    Term_season = models.CharField(max_length=6)
    Term_Year = models.IntegerField()
    Recommendation_letters = models.BooleanField(default=False)
    Transcript = models.BooleanField(default=False)
    Tests = models.BooleanField(default=False)
    Statement_of_purpose = models.BooleanField(default=False)
    Personal_statement = models.BooleanField(default=False)

class Student(Models.Model):
    Student_id = models.IntegerField(primary_key=True)
    Student_firstname = models.CharField(max_length=100)
    Student_lastname = models.CharField(max_length=100)
    Student_password = models.CharField(max_length=100)

