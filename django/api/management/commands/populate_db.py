# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2018 FU Berlin and HAW Hamburg
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""

import os
import sys
import requests
import tarfile
import tempfile
import io

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

# append root of the python code tree to sys.apth so that imports are working
#   alternative: add path to rapstore_backend to the PYTHONPATH environment variable, but this includes one more step
#   which could be forget
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT_DIR = os.path.normpath(os.path.join(CUR_DIR, os.pardir, os.pardir, os.pardir))
sys.path.append(PROJECT_ROOT_DIR)

CRON_ENCODING="utf-8"

import api.settings as config
from api.models import Transaction
from api.models import Module
from api.models import Board
from api.models import Application, ApplicationInstance
from django.utils.html import escape
from api.db_initial_data.board_display_name_replacement import internalname_displayname_dict
from api.db_initial_data.board_storage_flash_support_addition import internalname_storageflashsupport_dict


def update_modules(transaction):
    """
    Update table "modules". The table is truncated and data is re-imported
    """

    for i in range(len(config.module_directories)):
        module_directory = config.module_directories[i]
        module_path = os.path.join(PROJECT_ROOT_DIR, config.path_root, module_directory)

        for name in os.listdir(module_path):
            if not os.path.isfile(os.path.join(module_path, name)):

                # ignoring include directories
                if name == 'include':
                    continue

                description = get_description(module_path, name)

                module_name = get_name(os.path.join(module_path, name), name)

                data = {'name': module_name, 'path': os.path.join(module_path, name), 'description': escape(description), 'group_identifier': module_directory, 'transaction': transaction}
                Module.objects.update_or_create(name=module_name, defaults=data)


def update_boards(transaction):
    """
    Update table "boards". The table is truncated and data is re-imported
    """

    def is_valid_board(path, item):
        """
        A board is valid if:
            1. path is a directory
            2. path doesn't end with "<prefix>-common"
            3. board is not native
        """
        return (
                not os.path.isfile(os.path.join(path, item))
                and not item.endswith('-common')
                and not item == 'common'
                and not item == 'native'
        )

    path = os.path.join(PROJECT_ROOT_DIR, config.path_root, 'boards')

    for board_internalname in os.listdir(path):
        if is_valid_board(path, board_internalname):

            displayname = internalname_displayname_dict.get(board_internalname, board_internalname)
            storageflashsupport = internalname_storageflashsupport_dict.get(board_internalname, False)

            data = {
                "internal_name": board_internalname,
                "display_name": displayname,
                "flash_program": 'openocd',
                "storage_flash_support": storageflashsupport,
                "transaction": transaction
            }

            Board.objects.update_or_create(internal_name=board_internalname, defaults=data)


def update_riot_apps():

    for i in range(len(config.application_directories)):

        application_set_dir = config.application_directories[i]
        application_set_path = os.path.join(PROJECT_ROOT_DIR, config.path_root, application_set_dir)

        for name in os.listdir(application_set_path):

            application_path = os.path.join(application_set_path, name)

            if not os.path.isfile(application_path):

                # ignoring include directories
                if name == 'include':
                    continue

                application_name = get_name(application_path, name)
                description = get_description(application_set_path, name)

                tmp_fd, tmp_file_path = tempfile.mkstemp()
                make_tarfile(tmp_file_path, application_path)

                # always upload riot applications by user "RIOT-community"
                author_user = User.objects.get(username='RIOT-community')
                token = Token.objects.get(user=author_user).key

                try:
                    existing_app = Application.objects.get(name=application_name)
                    update_application(token, existing_app.id, application_name, description, None, 'https://www.riot-os.org/', 'https://github.com/RIOT-OS/RIOT')
                    upload_application_instance(token, existing_app, '0.0.0', 1, tmp_file_path)

                except Application.DoesNotExist:
                    register_new_riot_app(token, application_name, description, tmp_file_path)


def update_application(token, app_id, application_name, description, licences, project_page, app_repo_url):

    headers = {
        'Authorization': 'Token ' + token,
    }
    payload = {
        'name': application_name,
        'description': escape(description),
        'licences': licences,
        'project_page': project_page,
        'app_repo_url': app_repo_url
    }

    r = requests.put('http://localhost:8000/api/app/%s/' % app_id, headers=headers, data=payload)

    if r.status_code not in {200, 201}:
        print('update for app {0} failed!'.format(application_name))
        print(r.content)


def upload_application_instance(token, app, version_name, version_code, tmp_file_path):

    headers = {
        'Authorization': 'Token ' + token,
    }
    payload = {
        'application': app.id,
        'version_name': version_name,
        'version_code': version_code
    }
    files = {'app_tarball': io.open(tmp_file_path, 'rb')}

    r = requests.post('http://localhost:8000/api/app_instance/', headers=headers, data=payload, files=files)

    if r.status_code not in {200, 201}:
        print('uploading app instance for app {0} failed!'.format(app.name))
        print(r.content)


def register_new_riot_app(token, application_name, description, tmp_file_path):

    headers = {
        'Authorization': 'Token ' + token,
    }
    payload = {
        'name': application_name,
        'description': escape(description),
        'licences': None,
        'project_page': 'https://www.riot-os.org/',
        'app_repo_url': 'https://github.com/RIOT-OS/RIOT',
        'initial_instance.version_name': '0.0.0',
        'initial_instance.version_code': '0'
    }
    files = {'app_tarball': io.open(tmp_file_path, 'rb')}

    r = requests.post('http://localhost:8000/api/app/', headers=headers, data=payload, files=files)

    os.remove(tmp_file_path)

    if r.status_code not in {200, 201}:
        print('posting app {0} failed!'.format(application_name))
        print(r.content)
        
    else:
        # riot specific modifications

        app = Application.objects.get(name=application_name)
        app_instance = ApplicationInstance.objects.get(application=app)

        # set riot as source
        app.source = 'R'

        # auto public
        app_instance.is_public = True

        app.save()
        app_instance.save()


def make_tarfile(output_path, source_dir):
    with tarfile.open(output_path, "w:gz") as tar:
        tar.add(source_dir, arcname=".")


def get_description(path, name):
    """
    Collection of rules executing inner function to search for a description
    Parameters
    ----------
    path: string
        Path in which the search is done
    name: string
        Name of a directory
    Returns
    -------
    string
        Description of item, None if not found
    """

    def get_description_helper(path):
        """
        Get description from line which contains "@brief"
        Parameters
        ----------
        path: string
            Path to file
        Returns
        -------
        string
            Description of item, None if not found
        """

        description = ''

        try:
            with io.open(path, 'r', encoding=CRON_ENCODING) as file:

                brief_active = False
                for line in file:

                    if brief_active:
                        if not '* @' in line:
                            description += line.replace('*', '', 1).strip()
                        else:
                            break

                    if '@brief' in line:
                        index = line.find('@brief') + len('@brief')
                        description = line[index:].strip()
                        brief_active = True

        except IOError:
            return None

        if description == '':
            description = None

        return description

    # try rule 1
    description = get_description_helper(os.path.join(path, 'include', name + '.h'))

    # try rule 2
    if description is None:
        description = get_description_helper(os.path.join(path, name, 'doc.txt'))

    # try rule 3
    if description is None:
        description = get_description_helper(os.path.join(path, name, name + '.c'))

    # try rule 4
    if description is None:
        description = get_description_helper(os.path.join(path, name, 'main.c'))

    return description if description is not None else 'There is no description yet'


def get_name(path, application_directory):
    """"
    Get the name of an application
    Parameters
    ----------
    path: string
        Path containing file called "Makefile"
    application_directory: string
        Replacement if nothing found or IOError is raised internally
    Returns
    -------
    string
        Name of the application
    """
    name = ''

    try:
        with io.open(os.path.join(path, 'Makefile'), 'r', encoding=CRON_ENCODING) as makefile:
            for line in makefile:

                line = line.replace(' ', '')

                if 'APPLICATION=' in line:
                    index = line.find('APPLICATION=') + len('APPLICATION=')
                    name = line[index:]
                    break

                elif 'PKG_NAME=' in line:
                    index = line.find('PKG_NAME=') + len('PKG_NAME=')
                    name = line[index:]
                    break

    except IOError:
        return application_directory

    if name == '':
        name = application_directory

    # remove \n and stuff like that
    return name.strip()


class Command(BaseCommand):
    help = 'Populate Boards, Modules, Apps with RIOT'

    def handle(self, *args, **options):
        transaction = Transaction.objects.create()
        try:
            update_modules(transaction)
            update_boards(transaction)
            update_riot_apps()
            print('OK')

        except Exception as e:
            transaction.delete()
            print('FAIL: {}'.format(str(e)))

