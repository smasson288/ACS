from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, password):
        user = self.model(
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_staff_user(self, username, password, school):
        user = self.model(
            username=username,
            School_id_id=school,
        )
        user.set_password(password)
        user.save(using=self._db)

        return user


class Student(AbstractBaseUser):
    username = models.CharField(primary_key=True, max_length=100)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    password = models.CharField(max_length=100)

    objects = UserManager()

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']


class School(models.Model):
    School_id = models.IntegerField(primary_key=True, auto_created=True)
    School_desc = models.CharField(max_length=100)
    School_name = models.CharField(max_length=100, unique=True)
    Address_street = models.CharField(max_length=100)
    Address_city = models.CharField(max_length=100)
    Address_state = models.CharField(max_length=100)
    Address_zipcode = models.CharField(max_length=100)

class Staff(Student):
    School_id = models.ForeignKey(School, on_delete=models.CASCADE)

    REQUIRED_FIELDS = ['password', 'School_id']

class Program(models.Model):
    Program_id = models.IntegerField(primary_key=True, auto_created=True)
    Major = models.CharField(max_length=100)
    Degree = models.CharField(max_length=100)
    School_id = models.ForeignKey(School, on_delete=models.CASCADE)

class Requirement(models.Model):
    Requirement_id = models.IntegerField(primary_key=True, auto_created=True)
    Program_id = models.ForeignKey(Program, on_delete=models.CASCADE)
    Term_season = models.CharField(max_length=6)
    Term_year = models.IntegerField()
    Recommendation_letters = models.BooleanField(default=False)
    Transcript = models.BooleanField(default=False)
    Tests = models.BooleanField(default=False)
    Statement_of_purpose = models.BooleanField(default=False)
    Personal_statement = models.BooleanField(default=False)

class Checklist(models.Model):
    Checklist_id = models.IntegerField(primary_key=True, auto_created=True)
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
    Feedback_id = models.IntegerField(primary_key=True, auto_created=True)
    Checklist_id = models.ForeignKey(Checklist, on_delete=models.CASCADE)
    STATUS_CHOICES = (
        ("ACCEPTED","Accepted"),
        ("WAITLISTED", "Waitlisted"),
        ("DENIED", 'Denied'),
    )
    Feedback_status = models.CharField(max_length=1, choices=STATUS_CHOICES)
    GPA = models.FloatField()
    Standardized_Test = models.IntegerField()
    Recommendation = models.CharField(max_length=1000)
    Research = models.CharField(max_length=1000)

