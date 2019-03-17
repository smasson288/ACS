from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, first_name, last_name, password):
        user = self.model(
            username=username,
            first_name=first_name,
            last_name=last_name,
        )

        user.set_password(password)
        user.save(using=self.db)

        return user


class Student(AbstractBaseUser):
    username = models.CharField(primary_key=True, max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'password']


class School(models.Model):
    School_id = models.IntegerField(primary_key=True)
    School_desc = models.CharField(max_length=100)
    School_name = models.CharField(max_length=100)
    Address_street = models.CharField(max_length=100)
    Address_city = models.CharField(max_length=100)
    Address_state = models.CharField(max_length=100)
    Address_zipcode = models.CharField(max_length=100)


class Staff(Student):
    School_id = models.ForeignKey(School, on_delete=models.CASCADE)


class Program(models.Model):
    Program_id = models.IntegerField(primary_key=True)
    Program_name = models.CharField(max_length=100)
    College = models.CharField(max_length=100)
    Degree = models.CharField(max_length=100)
    School_id = models.ForeignKey(School, on_delete=models.CASCADE)


class Requirement(models.Model):
    Requirement_id = models.IntegerField(primary_key=True)
    Program_id = models.ForeignKey(Program, on_delete=models.CASCADE)
    Term_season = models.CharField(max_length=6)
    Term_year = models.IntegerField()
    Recommendation_letters = models.BooleanField(default=False)
    Transcript = models.BooleanField(default=False)
    Tests = models.BooleanField(default=False)
    Statement_of_purpose = models.BooleanField(default=False)
    Personal_statement = models.BooleanField(default=False)


class Checklist(models.Model):
    Checklist_id = models.IntegerField(primary_key=True)
    Requirement_id = models.ForeignKey(Requirement, on_delete=models.CASCADE)
    Student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    Term_season = models.CharField(max_length=6)
    Term_Year = models.IntegerField()
    Recommendation_letters = models.BooleanField(default=False)
    Transcript = models.BooleanField(default=False)
    Tests = models.BooleanField(default=False)
    Statement_of_purpose = models.BooleanField(default=False)
    Personal_statement = models.BooleanField(default=False)


class Feedback(models.Model):
    Feedback_id = models.IntegerField(primary_key=True)
    Checklist_id = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ("ACCEPTED","Accepted"),
        ("WAITLISTED", "Waitlisted"),
        ("DENIED", 'Denied'),
    )
    Feedback_status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    GPA = models.IntegerField()
    Standardized_Test = models.IntegerField()
    Recommendation = models.CharField(max_length=1000)
    Research = models.CharField(max_length=1000)

