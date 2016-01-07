from django.contrib.auth.models import User, Group
from oauth2_provider.ext.rest_framework import TokenHasScope
from rest_framework import permissions, routers, serializers, viewsets

from core.models import Progress, Project


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress
        #exclude = ('customer',)


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        #exclude = ('customer',)


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('url', 'is_staff')


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['reporter']
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer


class ProgressViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['reporter']
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope, permissions.IsAdminUser]
    required_scopes = ['management']
    queryset = User.objects.all()
    serializer_class = UserSerializer


httpapi_router = routers.DefaultRouter()
httpapi_router.register(r'projects', ProjectViewSet)
httpapi_router.register(r'progresses', ProgressViewSet)
httpapi_router.register(r'users', UserViewSet)
