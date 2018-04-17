from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from api.serializers import ApplicationSerializer
from api.serializers import ApplicationInstanceSerializer
from api.serializers import BoardSerializer
from api.serializers import UserSerializer
from api.serializers import CreateUserSerializer
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
from rest_framework import parsers
from rest_framework.exceptions import ValidationError
from django.db import IntegrityError

class NestedMultipartParser(parsers.MultiPartParser):
    def parse(self, stream, media_type=None, parser_context=None):
        result = super().parse(stream=stream, media_type=media_type, parser_context=parser_context)
        data = {}
        for key, value in result.data.items():
            if '.' in key:
                values = key.split('.')                
                nested_dict_key = values[0]
                nested_value_key = values[1]
                if len(nested_dict_key) and len(nested_value_key):
                    if nested_dict_key not in data:
                       data[nested_dict_key] = {}
                    data[nested_dict_key][nested_value_key] = value
            else:
                data[key] = value
        return parsers.DataAndFiles(data, result.files)

class ApplicationViewSet(viewsets.ModelViewSet):

    queryset = Application.objects.order_by('name')
    serializer_class = ApplicationSerializer
    parser_classes = (NestedMultipartParser, FormParser,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    def get_queryset(self):
        queryset = self.queryset
        for app in queryset:
            # needs at least one visible application instance
            app_instances = app.applicationinstance_set.filter(is_public=True)

            if len(app_instances) == 0:
                queryset = queryset.exclude(name=app.name)
        return queryset

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

        response = HttpResponse(base64.b64decode(r.text), content_type='application/octet-stream')
        response['Content-Disposition'] = 'attachment; filename=%s.elf' % app.name
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        return response

    @detail_route(methods=['get'], permission_classes=[IsAdminUser, ])
    def download(self, request, pk=None):
        app = get_object_or_404(Application, pk=pk)
        response = HttpResponse(app.app_tarball, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s' % app.app_tarball.name

        return response

    def perform_create(self, serializer):
        app_tarball = self.request.data.pop('app_tarball', None)
        initial_instance = self.request.data.pop("initial_instance", {})
        if app_tarball:
            initial_instance["app_tarball"] = app_tarball[0]

        app_instance_serializer = ApplicationInstanceSerializer(data=initial_instance)
        app_instance_serializer.is_valid(raise_exception=True)

        serializer.save(author=self.request.user)
        try:
            app_instance_serializer.save(application=serializer.instance)
        except IntegrityError as e:
            serializer.instance.delete()
            raise e


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

    @list_route(methods=['PUT'], url_path="update")
    def update_data(self, request):
        user = request.user
        if user.is_anonymous:
            return Response()

        serializer = UserSerializer(user, data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def register(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if(serializer.is_valid()):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
