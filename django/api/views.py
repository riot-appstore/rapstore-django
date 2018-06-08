# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2018 FU Berlin and HAW Hamburg
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""

import base64
import requests
from riot_apps import settings

from api import tasks
from api.models import Application
from api.models import ApplicationInstance
from api.models import Board
from api.models import Feedback
from api.permissions import IsAppOwnerOrReadOnly
from api.permissions import IsAdminUserOrReadOnly
from api.serializers import ApplicationInstanceSerializer
from api.serializers import ApplicationSerializer
from api.serializers import BoardSerializer
from api.serializers import CreateUserSerializer
from api.serializers import UserSerializer
from api.serializers import FeedbackSerializer
from celery.result import AsyncResult
from django.db import IntegrityError
from django.db.models import F
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.utils.text import slugify
from rest_framework import parsers
from rest_framework import status
from rest_framework import mixins
from rest_framework import viewsets
from rest_framework.decorators import api_view
from rest_framework import permissions
from rest_framework.decorators import detail_route, list_route
from rest_framework.parsers import FormParser
from rest_framework.permissions import IsAdminUser
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.response import Response
from rest_social_auth.views import SocialTokenUserAuthView

from django import forms
import json

import uuid
from hashlib import md5
import os


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


class BuildManagerViewSet(viewsets.ViewSet):

    @detail_route(methods=['GET'])
    def status(self, request, pk=None):
        r = AsyncResult(pk)
        if(r.status == "FAILURE"):
            r.forget()
        return Response({"status": r.status})

    @detail_route(methods=['GET'])
    def fetch(self, request, pk=None):
        r = AsyncResult(pk)
        if not r.result:
            return Response({"error": "Link expired or request not found"}, status=status.HTTP_404_NOT_FOUND)

        if r.status != "SUCCESS":
            return Response({"error": "Job failed or not ready"}, status=status.HTTP_400_BAD_REQUEST)

        filename = r.result.get("filename")
        b64 = r.result.get("b64")
        r.forget()
        response = HttpResponse(base64.b64decode(b64), content_type='application/octet-stream')
        response['Content-Disposition'] = "attachment; filename={}".format(filename)
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        return response


class ApplicationViewSet(viewsets.ModelViewSet):

    queryset = Application.objects.order_by('name')
    serializer_class = ApplicationSerializer
    parser_classes = (NestedMultipartParser, FormParser,)
    permission_classes = (IsAuthenticatedOrReadOnly, IsAppOwnerOrReadOnly,)

    def get_queryset(self):
        queryset = self.queryset.filter(applicationinstance__is_public=True)
        return queryset

    #TODO: Serializers here...
    @detail_route(methods=['GET'], permission_classes=[permissions.IsAuthenticated])
    def build(self, request, pk=None):
        app = get_object_or_404(Application, pk=pk)
        f = app.applicationinstance_set.last().app_tarball
        files = {'file': f}

        board = request.GET.get('board', None)
        if not board:
            return Response('Board not found', status=status.HTTP_400_BAD_REQUEST)

        bin_type = request.GET.get('type', None)
        if not bin_type or bin_type not in ['bin', 'hex', 'elf']:
            return Response('Missing type', status=status.HTTP_400_BAD_REQUEST)

        board_name = Board.objects.get(pk=board).internal_name
        r=tasks.build.delay(app.name, board_name, bin_type, base64.b64encode(f.read()).decode('utf-8'))

        # build was successful, increment download counter now
        app.download_count = F('download_count') + 1
        app.save()
        return Response({"task_id": r.task_id})

    @detail_route(methods=['GET'], permission_classes=[permissions.IsAuthenticated,])
    def supported_boards(self, request, pk=None):
        app = get_object_or_404(Application, pk=pk)
        f = app.applicationinstance_set.last().app_tarball
        files = {'file': f}

        r = requests.post('http://builder:8000/supported_boards/', files=files)
        supported_boards = json.loads(r.text)["supported_boards"]
        queryset = Board.objects.filter(internal_name__in=supported_boards).order_by('display_name')
        serializer = BoardSerializer(queryset, many=True)
        return Response(serializer.data)


    @detail_route(methods=['GET'], permission_classes=[permissions.AllowAny, ])
    def download(self, request, pk=None):
        app = get_object_or_404(Application, pk=pk)
        f = app.applicationinstance_set.last().app_tarball
        response = HttpResponse(f, content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=%s.tar.gz' % app.name

        return response

    def perform_create(self, serializer):

        app_tarball = self.request.data.pop('app_tarball', None)
        initial_instance = self.request.data.pop("initial_instance", {})

        if app_tarball:
            initial_instance["app_tarball"] = app_tarball[0]

        app_instance_serializer = ApplicationInstanceSerializer(
            data = initial_instance,
            context = {'application_id': ApplicationInstanceSerializer.APPLICATION_ID_DOES_NOT_EXIST}
        )
        app_instance_serializer.is_valid(raise_exception=True)

        serializer.save(author=self.request.user)
        try:
            app_instance_serializer.save(application=serializer.instance)

        except IntegrityError as e:
            serializer.instance.delete()
            raise e

    @detail_route(methods=['POST'])
    def instance(self, request, pk):

        app_tarball = self.request.data.pop('app_tarball', None)

        if app_tarball:
            request.data['app_tarball'] = app_tarball[0]

        serializer = ApplicationInstanceSerializer(data=request.data, context={'application_id': pk})

        if serializer.is_valid():

            try:
                serializer.save(application=Application.objects.get(id=pk))

            except Exception as e:
                print(e)
                return Response('Could not save object', status=status.HTTP_400_BAD_REQUEST)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ApplicationInstanceViewSet(viewsets.ModelViewSet):

    permission_classes = (IsAuthenticatedOrReadOnly,)
    queryset = ApplicationInstance.objects.order_by('version_code')
    serializer_class = ApplicationInstanceSerializer


class BoardViewSet(viewsets.ReadOnlyModelViewSet):

    permission_classes = (IsAdminUserOrReadOnly,)
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
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    @list_route(methods=['POST'])
    def register(self, request):
        serializer = CreateUserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FeedbackViewSet(mixins.CreateModelMixin, viewsets.GenericViewSet):
    queryset = Feedback.objects.all()
    serializer_class = FeedbackSerializer


class SecureSocialLogin(SocialTokenUserAuthView):
    def post(self, request, *args, **kwargs):
        int_state=request.COOKIES.get('state', None)
        if not int_state:
            return Response({"error": "State param not present"}, status=status.HTTP_400_BAD_REQUEST)

        int_state = str(int_state).encode('utf-8')
        v1 = md5(int_state).hexdigest()
        v2 = request.data.get("state")
        if v1 != v2:
            return Response({"error": "State mismatch"}, status=status.HTTP_400_BAD_REQUEST)
        
        return super().post(request, *args, **kwargs)
    pass


#TODO: Get link from social_auth
@api_view(('GET',))
def get_social(request, provider):
    if(provider) == "github":
        int_state=request.COOKIES.get('state', None)

        if not int_state:
            int_state=md5(os.urandom(32)).hexdigest()

        int_state = str(int_state).encode('utf-8')

        response = Response({"url": "https://github.com/login/oauth/authorize/?client_id={}&state={}".format(settings.SOCIAL_AUTH_GITHUB_KEY,md5(int_state).hexdigest())})
        response.set_cookie("state", int_state)
        return response
    return Response({"error": "No provider"}, status=status.HTTP_400_BAD_REQUEST)
