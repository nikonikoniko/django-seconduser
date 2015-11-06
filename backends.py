from .models import SecondUser


class SecondUserAuth(object):
    def authenticate(self, email=None, password=None):
        try:
            user = SecondUser.objects.get(email=email)
            print user
            print password
            print email
            if user.check_password(password):
                return user
        except SecondUser.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = SecondUser.objects.get(pk=user_id)
            return user
        except SecondUser.DoesNotExist:
            return None
