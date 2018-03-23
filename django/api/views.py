from django.shortcuts import render
from django.http import HttpResponse
from api.dummy import dummy_request
from api.serializers import ApplicationSerializer
from api.models import Application
from django.contrib.auth.decorators import login_required
from rest_framework import generics
from rest_framework import viewsets

from io import StringIO


@login_required
def request_download(request):
    # Read request. For now, just read dummy request
    #TODO:
    build_request = dummy_request()

    # Decode base64
    elf_file = StringIO()
    elf_file.write(build_request["files"]["elf"])

    # generate the file
    response = HttpResponse(elf_file.getvalue(), content_type='application/zip')
    response['Content-Disposition'] = 'attachment; filename=riot.zip'
    return response


class ApplicationViewSet(viewsets.ModelViewSet):
    queryset = Application.objects.all()
    serializer_class = ApplicationSerializer
