from django.conf import settings
from django.core.mail import EmailMultiAlternatives
from riot_apps.celery_settings import app
import base64
import tempfile
from subprocess import Popen, PIPE, STDOUT
import tarfile
import time
from io import BytesIO
from urllib.request import urlopen
import os
import json

RAW_LOCATION = "/raw"
@app.task
def add(x, y):
    return x + y

def write_tar(f):
    try:
        tf = tarfile.open(fileobj=f)

    except:
        return None

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

    tmp_dir = tempfile.mkdtemp()
    cmd = ['make',
           '-j4',
           '-C', app_build_dir,
           'binfile',
           'RIOTBASE=/RIOT',
           'BINDIR=%s' % tmp_dir,
           'ELFFILE=%s/app.elf' % tmp_dir,
           'BOARD=%s' % board]
    #logging.debug('make: %s', cmd)

    process = Popen(cmd, stdout=PIPE, stderr=STDOUT)

    process.communicate()
    return tmp_dir

def handle_file(instance_id):
    #TODO: Catch
    directory = "{}/{}".format(RAW_LOCATION, instance_id)
    if not os.path.isdir(directory):
        #Create folder and extract
        os.makedirs(directory)
        url = "http://web:8000/api/instance/{}/fetch/".format(instance_id)
        response = urlopen(url)
        tf = tarfile.open(fileobj=BytesIO(response.read()))
        tf.extractall(path=directory)
    return directory

@app.task
def supported_boards(instance_id):
    directory = handle_file(instance_id)

    #Since we have the folder, let's do stuff
    cmd = ['make',
           '-C', directory,
           'RIOTBASE=/RIOT',
           'info-boards-supported']

    process = Popen(cmd, stdout=PIPE, stderr=STDOUT)

    output = process.communicate()[0].decode('utf-8').split("\n")

    for l in range(len(output)):
        if output[l].find(":") < 0:
            break

    return json.dumps({"supported_boards": output[l].split(" ")})

@app.task
def build(app_name, board, bin_type, instance_id):

    directory = handle_file(instance_id)

    #Since we have the folder, let's do stuff
    tmp_dir=execute_makefile(directory, board, 'test')

    with open("{}/app.{}".format(tmp_dir, bin_type), 'rb') as file:
        b64 = base64.b64encode(file.read())

    return {"b64": b64.decode('utf-8'), "filename": "{}_{}.{}".format(app_name, board, bin_type)}

@app.task
def lua_build(code, board, bin_type, instance_id):
    directory = handle_file(instance_id)

    f = open("{}/main.lua".format(directory), "w+")
    f.write(code)
    f.close()

    tmp_dir = execute_makefile(directory, board, 'test')

    with open("{}/app.{}".format(tmp_dir, bin_type), 'rb') as file:
        b64 = base64.b64encode(file.read())

    return {"b64": b64.decode('utf-8'), "filename": "lua_{}.{}".format(board, bin_type)}