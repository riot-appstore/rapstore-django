from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from api.serializers import ApplicationSerializer
from api.serializers import BoardSerializer
from api.models import Application
from api.models import Board
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from rest_framework import generics
from rest_framework import viewsets
from rest_framework.response import Response
import requests
from rest_framework.decorators import detail_route, list_route
import base64
from django import forms
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAuthenticatedOrReadOnly

from io import StringIO


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all().order_by('name')
    serializer_class = ApplicationSerializer
    parser_classes = (MultiPartParser, FormParser,)
    permission_classes = (IsAuthenticatedOrReadOnly,)

    @detail_route(methods=['get'])
    def build(self, request, pk=None):
        app = get_object_or_404(Application, pk=pk)
        f=app.app_tarball
        files = {'file': f}
        board = request.GET.get('board', None)
        if not board:
            return HttpResponse("Board not found")

        r = requests.post("http://builder:8000/build/", data={"board": board}, files=files)

        if(r.status_code != 200):
            return HttpResponse("Error")

        response = HttpResponse(base64.b64decode(r.text), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=file.elf'
        return response

    def perform_create(self, serializer):
        serializer.save(app_tarball=self.request.data.get('app_tarball'))


class BoardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Board.objects.all().order_by('display_name')
    serializer_class = BoardSerializer

class UploadFileForm(forms.ModelForm):
    class Meta:
        model=Application
        fields=('name', 'description', 'licences', 'project_page', 'app_tarball', 'app_repo_url') 
