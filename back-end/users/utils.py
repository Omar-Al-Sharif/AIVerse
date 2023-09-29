from rest_framework_simplejwt_mongoengine.tokens import RefreshToken


def generate_access_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh.access_token)


def generate_refresh_token(user):
    refresh = RefreshToken.for_user(user)
    return str(refresh)
