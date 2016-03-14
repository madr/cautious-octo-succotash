import rest_framework_filters as filters
from django.contrib.auth.models import User
from oauth2_provider.ext.rest_framework import TokenHasScope
from rest_framework import permissions, routers, serializers, viewsets
from rest_framework.response import Response

from core.models import Progress, Project


class WhoAmI(object):
    def __init__(self, user_id, email, login, full_name):
        self.pk = user_id
        self.email = email
        self.login = login
        self.name = full_name


class ProjectFilter(filters.FilterSet):
    username = filters.CharFilter(name='username')


class ProgressFilter(filters.FilterSet):
    note = filters.CharFilter(name='note')
    author = filters.RelatedFilter(ProjectFilter, name='project')


class ProgressSerializer(serializers.ModelSerializer):
    class Meta:
        model = Progress


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('url', 'is_staff')


class WhoAmISerializer(serializers.Serializer):
    email = serializers.EmailField()
    login = serializers.CharField()
    name = serializers.CharField()


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

    #def create(self, request, *args, **kwargs):
    #    pass


class UserViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope, permissions.IsAdminUser]
    required_scopes = ['management']
    queryset = User.objects.all()
    serializer_class = UserSerializer


class WhoAmIViewSet(viewsets.ViewSet):
    allowed_methods = ['GET']
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    queryset = User.objects.all()
    required_scopes = ['reporter']
    resource_name = 'user'

    def list(self, request):
        current_user = WhoAmI(request.user.id, request.user.email, request.user.username, request.user.first_name)
        serializer = WhoAmISerializer(current_user)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        pass


httpapi_router = routers.DefaultRouter()
httpapi_router.register(r'projects', ProjectViewSet)
httpapi_router.register(r'progresses', ProgressViewSet)
httpapi_router.register(r'users', UserViewSet)
httpapi_router.register(r'whoami', WhoAmIViewSet)
