migrate the app

add this to authentication backend

AUTHENTICATION_BACKENDS = [
  'django.contrib.auth.backends.ModelBackend',
  'seconduser.backends.SecondUserAuth', ]


  extend into a model

  EMAIL_SENDER in settings

  urls
