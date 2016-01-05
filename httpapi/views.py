from django.contrib.auth.models import User, Group
from oauth2_provider.ext.rest_framework import TokenHasScope
from rest_framework import permissions, routers, serializers, viewsets


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope, permissions.IsAdminUser]
    queryset = User.objects.all()
    serializer_class = UserSerializer


class GroupViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope, permissions.IsAdminUser]
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


httpapi_router = routers.DefaultRouter()
httpapi_router.register(r'users', UserViewSet)
httpapi_router.register(r'groups', GroupViewSet)
