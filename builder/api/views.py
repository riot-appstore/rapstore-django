from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import tempfile
import tarfile
from subprocess import Popen, PIPE, STDOUT
import base64
import json


def extract_tar(tar):
    # Create temp folder
    folder = tempfile.mkdtemp()
    tar.extractall(path=folder)

    return folder


def write_tar(f):
    try:
        tf = tarfile.open(fileobj=f)

    except:
        return 'Not OK'

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

    cmd = ['make',
           '-j4',
           '-C', app_build_dir,
           'binfile',
           'RIOTBASE=/RIOT',
           'ELFFILE=app.elf',
           'BOARD=%s' % board]
    #logging.debug('make: %s', cmd)

    process = Popen(cmd, stdout=PIPE, stderr=STDOUT)

    return process.communicate()[0]


@csrf_exempt
def supported_boards(request):
    f = request.FILES['file']
    dest = write_tar(f)

    #Since we have the folder, let's do stuff
    cmd = ['make',
           '-C', dest,
           'RIOTBASE=/RIOT',
           'info-boards-supported']

    process = Popen(cmd, stdout=PIPE, stderr=STDOUT)

    output = process.communicate()[0].split("\n")

    for l in range(len(output)):
        if output[l].find(":") < 0:
            break

    return HttpResponse(json.dumps({"supported_boards": output[l].split(" ")}))


@csrf_exempt
def build(request):
    #TODO: Validation...
    f = request.FILES['file']
    board = request.POST['board']
    bin_type = request.POST['type']
    dest = write_tar(f)

    #Since we have the folder, let's do stuff
    execute_makefile(dest, board, 'test')

    with open("{}/app.{}".format(dest, bin_type), 'rb') as file:
        b64 = base64.b64encode(file.read())

    return HttpResponse(b64)
