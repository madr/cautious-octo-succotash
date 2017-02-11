from django.contrib.auth.models import User
from oauth2_provider.ext.rest_framework import TokenHasScope
from rest_framework import permissions, routers, viewsets
from rest_framework.response import Response

from tajm.core.models import Progress, Project, AbsenceCategory, Absence
from tajm.httpapi.lib.filters import ProjectFilter, AbsenceCategoryFilter, ProgressFilter, AbsenceFilter
from tajm.httpapi.lib.serializers import ProjectSerializer, AbsentiaSerializer, ProgressSerializer, AbsenceSerializer, \
    WhoAmISerializer


class WhoAmI(object):
    def __init__(self, user_id, email, login, full_name):
        self.pk = user_id
        self.email = email
        self.login = login
        self.name = full_name


class ProjectViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['reporter']
    queryset = Project.objects.all()
    serializer_class = ProjectSerializer
    filter_class = ProjectFilter


class ProgressViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['reporter']
    queryset = Progress.objects.all()
    serializer_class = ProgressSerializer
    filter_class = ProgressFilter


class AbsenceViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['reporter']
    queryset = Absence.objects.all()
    serializer_class = AbsenceSerializer
    filter_class = AbsenceFilter


class AbsenceCategoryViewSet(viewsets.ModelViewSet):
    permission_classes = [permissions.IsAuthenticated, TokenHasScope]
    required_scopes = ['reporter']
    queryset = AbsenceCategory.objects.all()
    serializer_class = AbsentiaSerializer
    filter_class = AbsenceCategoryFilter


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
httpapi_router.register(r'absence_categories', AbsenceCategoryViewSet)
httpapi_router.register(r'absences', AbsenceViewSet)
httpapi_router.register(r'whoami', WhoAmIViewSet)
