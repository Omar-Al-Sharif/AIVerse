# from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from .models import User
from .serializers import UserSerializer

# from rest_framework_simplejwt_mongoengine.serializers import TokenObtainPairSerializer
# from rest_framework_simplejwt_mongoengine.views import TokenObtainPairView


# Create your views here.

# class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#     @classmethod
#     def validate(self, attrs):
#         self.user = None
#         username = attrs.get("email")
#         password = attrs.get("password")

#         # Authenticate user by email and password
#         if username and password:
#             self.user = self.authenticate(email=username, password=password)
#         else:
#             raise exceptions.AuthenticationFailed(
#                 self.error_messages["no_active_account"],
#                 "no_active_account",
#             )

#         # You can add additional checks here
#         return {}

#     @classmethod
#     def authenticate(self, email, password):
#         """
#         Authenticate the request and return a user.
#         You need to implement this method to authenticate by email and password.
#         """

#         # Here you can write your logic to authenticate the user by email and password
#         # For example:
#         user = User.objects.filter(email=email).first()
#         if user and user.check_password(password):
#             return user
#         return None

#     class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
#         @classmethod
#         def get_token(cls, user):
#             token = super().get_token(user)

#             # Add custom claims
#             token["full_name"] = user.full_name
#             # ...

#             return token


# class MyTokenObtainPairView(TokenObtainPairView):
#     serializer_class = MyTokenObtainPairSerializer


# What shall we do here?
# Create a view for login
class UserViewSet(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects


# Create a view for signup
# Create a view for logout
# Create a view for changing password
# Create a view for changing profile picture
# Create a view for changing email
# Create a view for Email Verification
# Create a view for Password Reset


# Create a view for Updating (Recommending) for user's current feed
# Create a view for Updating user's liked articles
# Create a view for Updating user's disliked articles
# Create a view for Updating user's reading list
# Create a view for Updating user's liked tags
# Create a view for Updating user's disliked tags


# Create a view for getting user's reading list
# Create a view for getting user's liked articles
# Create a view for getting user's disliked articles
# Create a view for getting user's current feed
