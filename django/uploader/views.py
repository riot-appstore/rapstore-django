from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from uploader.forms import UploadFileForm
from django.contrib.auth.decorators import login_required

@login_required
def uploader(request):
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.save()
            return HttpResponseRedirect('/success/')
        else:
            return HttpResponseRedirect('/failure/')
    else:
        form = UploadFileForm()

    t = get_template('uploader.html')
    html = t.render(context={"form": form}, request=request)
    return HttpResponse(html)

# Create your views here.
