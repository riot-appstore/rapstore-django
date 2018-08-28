import base64

from django.http import HttpResponse
from django.shortcuts import render
from api.models import Application
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.decorators import list_route
from rest_framework.permissions import IsAuthenticated
from api import tasks

class CodeViewSet(viewsets.ViewSet):
    permission_classes = (IsAuthenticated,)

    @list_route(methods=['POST'])
    def build(self, request):
        code = request.POST.get('code')
        board = request.POST.get('board')

        app_instance = Application.objects.get(name='lua_basic').applicationinstance_set.last()

        bin_type = request.POST.get('type', None)
        if not bin_type or bin_type not in ['bin', 'hex', 'elf']:
            return Response('Missing type', status=status.HTTP_400_BAD_REQUEST)

        task = tasks.lua_build.delay(code, board, bin_type, app_instance.pk)
        result = task.get()
        filename = result['filename']
        b64 = result['b64']
        task.forget()
        
        response = HttpResponse(base64.b64decode(b64), content_type='application/octet-stream')
        response['Content-Disposition'] = "attachment; filename={}".format(filename)
        response["Access-Control-Expose-Headers"] = "Content-Disposition"
        return response
