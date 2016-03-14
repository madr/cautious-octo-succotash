import rest_framework_filters as filters
from django.contrib.auth.models import User
from oauth2_provider.ext.rest_framework import TokenHasScope
from rest_framework import permissions, routers, serializers, viewsets
from rest_framework.response import Response
from rest_framework_json_api import relations

from core.models import Progress, Project


class WhoAmI(object):
    def __init__(self, user_id, email, login, full_name):
        self.pk = user_id
        self.email = email
        self.login = login
        self.name = full_name


class ProjectFilter(filters.FilterSet):
    name = filters.AllLookupsFilter()

    class Meta:
        model = Project


class ProgressFilter(filters.FilterSet):
    done_at = filters.DateFilter()
    done_at__gte = filters.DateFilter(name='done_at', lookup_expr='gte')
    done_at__lte = filters.DateFilter(name='done_at', lookup_expr='lte')
    done_at__gt = filters.DateFilter(name='done_at', lookup_expr='gt')
    done_at__lt = filters.DateFilter(name='done_at', lookup_expr='lt')

    created_at = filters.DateFilter()
    created__gte = filters.DateFilter(name='created_at', lookup_expr='gte')
    created__lte = filters.DateFilter(name='created_at', lookup_expr='lte')
    created__gt = filters.DateFilter(name='created_at', lookup_expr='gt')
    created__lt = filters.DateFilter(name='created_at', lookup_expr='lt')

    note = filters.AllLookupsFilter()
    project = filters.RelatedFilter(ProjectFilter, name='project')

    class Meta:
        model = Progress


class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Project
        exclude = ['created_at']


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        exclude = ('password', 'last_login', 'is_staff', 'date_joined', 'first_name',
                   'last_name', 'groups', 'user_permissions')


class ProgressSerializer(serializers.ModelSerializer):
    included_serializers = {
        'project': ProjectSerializer,
        'user': UserSerializer,
    }

    class Meta:
        model = Progress


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
    filter_class = ProgressFilter

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
#httpapi_router.register(r'users', UserViewSet)
httpapi_router.register(r'whoami', WhoAmIViewSet)
