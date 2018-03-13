from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from rest_framework import viewsets
from api.serializers import ApplicationSerializer
from uploader.models import Application
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

        r = requests.post("http://builder:8000/test/", data={"board": board}, files=files)

        #TODO:
        if(r.status_code != 200):
            return HttpResponse("Error")

        response = HttpResponse(base64.b64decode(r.text), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=file.elf'
        return response
