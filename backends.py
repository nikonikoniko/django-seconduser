from star.models import Star
from .models import SecondUser


class SecondUserAuth(object):
    def authenticate(self, authmodel=None, email=None, password=None):
        try:
            user = SecondUser.objects.get(email=email)
            print (user)
            print (password)
            print (email)
            print ("yyyyyyyyyyyyyyyyyy")
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
