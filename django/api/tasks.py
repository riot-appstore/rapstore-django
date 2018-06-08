from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from riot_apps.celery_settings import app
import base64
import tempfile
from subprocess import Popen, PIPE, STDOUT
import tarfile
import time

@app.task
def add(x, y):
    return x + y

def write_tar(f):
    try:
        tf = tarfile.open(fileobj=f)

    except:
        return 'Not OK'

    return extract_tar(tf)

def extract_tar(tar):
    # Create temp folder
    folder = tempfile.mkdtemp()
    tar.extractall(path=folder)

    return folder

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

@app.task
def build(app_name, board, bin_type, fb64):

    fc = base64.b64decode(fb64.encode('utf-8'))
    f = tempfile.TemporaryFile()
    f.write(fc)
    f.seek(0)

    dest = write_tar(f)
    f.close()

    #Since we have the folder, let's do stuff
    a=execute_makefile(dest, board, 'test')

    with open("{}/app.{}".format(dest, bin_type), 'rb') as file:
        b64 = base64.b64encode(file.read())

    return {"b64": str(b64), "filename": "{}_{}.{}".format(app_name, board, bin_type)}
