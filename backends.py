from .models import Member


class MemberAuth(object):
    def authenticate(self, email=None, password=None):
        try:
            user = Member.objects.get(email=email)
            print user
            print password
            print email
            if user.check_password(password):
                return user
        except Member.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            user = Member.objects.get(pk=user_id)
            return user
        except Member.DoesNotExist:
            return None
