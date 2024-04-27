from rest_framework.viewsets import ModelViewSet
from django.contrib.auth import get_user_model
from authentication.serializers import UserSerializer
from authentication.permissions import IsUnauthenticatedOrStaffOrNoPost, IsStaffOrUserOrSafeMethods
# Create your views here.


class UserViewSet(ModelViewSet):

    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    permission_classes = (IsUnauthenticatedOrStaffOrNoPost, IsStaffOrUserOrSafeMethods, )
