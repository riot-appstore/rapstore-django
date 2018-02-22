from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from uploader.forms import UploadFileForm
from django.contrib.auth.decorators import login_required

@login_required
def uploader(request):
    t = get_template('uploader.html')
    form = UploadFileForm()
    html = t.render(context={"form": form}, request=request)
    return HttpResponse(html)

# Create your views here.
