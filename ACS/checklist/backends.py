
from django.contrib.auth.hashers import check_password

from checklist.models import Staff, Student

class AuthBackend(object):

    def authenticate(self, username, password):
        try:
            user = Staff.objects.get(username=username)
            if check_password(password, user.password):
                return user
            return None
        except Staff.DoesNotExist:
            try:
                user = Student.objects.get(username=username)
                if check_password(password, user.password):
                    return user
            except Student.DoesNotExist:
                return None
    def get_user(self, username):
        try:
            user = Staff.objects.get(username=username)
            if user.is_active:
                return user
            return None
        except Staff.DoesNotExist:
            try:
                user = Student.objects.get(username=username)
                if user.is_active:
                    return user
                return None
            except Student.DoesNotExist:
                return None
