from django.shortcuts import render
from rest_framework import viewsets
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import tempfile
import tarfile
import os
from subprocess import Popen, PIPE, STDOUT
import base64

def extract_tar(tar):
    # Create temp folder
    folder = tempfile.mkdtemp()
    tar.extractall(path=folder)
    return folder

def write_tar(f):
    try:
        tf=tarfile.open(fileobj=f)
    except:
        return "Not OK"
    return extract_tar(tf)

def execute_makefile(app_build_dir, board, app_name):
    """
    Run make on given makefile and override variables
    Parameters
    ----------
    app_build_dir: string
        Path to makefile
    board: string
        Board name
    app_name: string
        Application name
    Returns
    -------
    string
        Output from executing make
    """

    cmd = ["make",
           "-C", app_build_dir,
           "RIOTBASE=/RIOT",
           "ELFFILE=app.elf",
           "BOARD=%s" % board]
    #logging.debug('make: %s', cmd)

    process = Popen(cmd, stdout=PIPE, stderr=STDOUT)
    return process.communicate()[0]

@csrf_exempt
def test(request):
    f = request.FILES['file']
    dest=write_tar(f)

    #Since we have the folder, let's do stuff
    execute_makefile(dest, "samr21-xpro", "test")

    with open(dest+"/app.elf", "rb") as file:
        b64 = base64.b64encode(file.read())

    return HttpResponse(b64)
