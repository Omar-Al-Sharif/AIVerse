from rest_framework.response import Response
from rest_framework_mongoengine import viewsets

from .models import User
from .serializers import UserSerializer

# Create your views here.


# What shall we do here?
# Create a view for login
class UserSetView(viewsets.ModelViewSet):
    serializer_class = UserSerializer
    queryset = User.objects

    # signup
    def create(self, request, *args, **kwargs):
        pass


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
