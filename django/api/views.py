from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from api.dummy import dummy_request
from api.serializers import ApplicationSerializer
from api.serializers import BoardSerializer
from api.models import Application
from api.models import Board
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework import viewsets
import requests
from rest_framework.decorators import detail_route, list_route
import base64

from io import StringIO


class ApplicationViewSet(viewsets.ModelViewSet):
    serializer_class = ApplicationSerializer
    queryset = Application.objects.all()
    
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


class ApplicationViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Application.objects.all().order_by('name')
    serializer_class = ApplicationSerializer

class BoardViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Board.objects.all().order_by('display_name')
    serializer_class = BoardSerializer
