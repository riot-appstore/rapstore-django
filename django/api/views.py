from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse
from api.dummy import dummy_request
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
        r = requests.post("http://builder:8000/test/", files=files)
        response = HttpResponse(base64.b64decode(r.text), content_type='application/force-download')
        response['Content-Disposition'] = 'attachment; filename=file.elf'
        return response

@login_required
def request_download(request):
    # Read request. For now, just read dummy request
    #TODO:
    #build_request = dummy_request()

    # Decode base64
    #elf_file = StringIO()
    #elf_file.write(build_request["files"]["elf"])

    # generate the file
    #response = HttpResponse(elf_file.getvalue(), content_type='application/zip')
    #response['Content-Disposition'] = 'attachment; filename=riot.zip'
    #return response
    #files = {'file': ('report.csv', open("file","rb"))}
    
    return None
