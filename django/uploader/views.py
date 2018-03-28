from django.shortcuts import render
from django.template.loader import get_template
from django.http import HttpResponse
from django.http import HttpResponseRedirect
#from uploader.forms import UploadFileForm
from django.contrib.auth.decorators import login_required

#@login_required
#def uploader(request):
#    if request.method == 'POST':
#        form = UploadFileForm(request.POST, request.FILES)
#        # At the moment, the file takes precidence if present, and if a file and URL are both present, an error is not raised. (Is there a built in way to check that only one or other of certain fields are returned in a django form?)
#        if form.data.get('app_repo_url', False) and not form.data.get('app_tarball', False): form.instance.download_tar(form.data.get('app_repo_url'))
#        
#        # checking validity should include checking that a tar.gz file is definitely attached to app_folder. Also that the app name is unique. In general, failure should include some output to the user. app_repo_url, on the other hand, isn't necessary
#        if form.is_valid():
#            obj = form.save(commit=False)
#            obj.author = request.user
#            obj.save()
#            return HttpResponseRedirect('/success/')
#        else:
#            return HttpResponseRedirect('/failure/')
#    else:
#        form = UploadFileForm()
#
#    t = get_template('uploader.html')
#    html = t.render(context={"form": form}, request=request)
#    return HttpResponse(html)

# Create your views here.
