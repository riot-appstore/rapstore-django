from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from api.serializers import ApplicationSerializer
from api.serializers import BoardSerializer
from api.serializers import UserSerializer
from api.models import Application
from api.models import ApplicationInstance
from api.models import Board
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
import requests
from rest_framework.decorators import detail_route, list_route
import base64
from django import forms
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated
from rest_framework.permissions import IsAdminUser
from rest_framework import status


class ApplicationViewSet(viewsets.ModelViewSet):

    queryset = Application.objects.order_by('name')

    for app in queryset:
        # needs at least one visible application instance
        app_instances = app.applicationinstance_set.filter(is_public=True)

        if len(app_instances) == 0:
            queryset = queryset.exclude(name=app.name)

    serializer_class = ApplicationSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    #TODO: Add auth
    @detail_route(methods=['get'])
    def build(self, request, pk=None):
        app = get_object_or_404(Application, pk=pk)
        f = app.app_tarball
        files = {'file': f}
        board = request.GET.get('board', None)
        if not board:
            return HttpResponse('Board not found')

        board_name = Board.objects.get(pk=board).internal_name
        r = requests.post('http://builder:8000/build/', data={'board': board_name}, files=files)

        if r.status_code != 200:
            return HttpResponse('Error')

        response = HttpResponse(base64.b64decode(r.text), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=file.elf'

        return response

    @detail_route(methods=['get'], permission_classes=[IsAdminUser, ])
    def download(self, request, pk=None):
        app = get_object_or_404(Application, pk=pk)
        response = HttpResponse(app.app_tarball, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % app.app_tarball.name

        return response

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, app_tarball=self.request.data.get('app_tarball'))


class BoardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Board.objects.all().order_by('display_name')
    serializer_class = BoardSerializer


class UploadFileForm(forms.ModelForm):
    class Meta:
        model=ApplicationInstance
        fields=('app_tarball', 'version_code', 'version_name')


class UserViewSet(viewsets.ViewSet):
    def list(self, request):
        user = request.user
        if user.is_anonymous:
            return Response()
        serializer = UserSerializer(user)
        return Response(serializer.data)

    @list_route(methods=['POST'])
    def register(self, request):
        serializer = UserSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save(is_active=False)
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
