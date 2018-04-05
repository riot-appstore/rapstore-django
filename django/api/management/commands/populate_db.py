# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2018 FU Berlin
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

from django.contrib.auth.models import User
from django.core.management.base import BaseCommand
from rest_framework.authtoken.models import Token

# append root of the python code tree to sys.apth so that imports are working
#   alternative: add path to rapstore_backend to the PYTHONPATH environment variable, but this includes one more step
#   which could be forget
CUR_DIR = os.path.abspath(os.path.dirname(__file__))
PROJECT_ROOT_DIR = os.path.normpath(os.path.join(CUR_DIR, os.pardir, os.pardir, os.pardir))
sys.path.append(PROJECT_ROOT_DIR)

import api.settings as config
from api.models import Transaction
from api.models import Module
from api.models import Board
from api.models import Application
from django.utils.html import escape

replacement_dict = {
    'acd52832': 'aconno ACD52832',
    'airfy-beacon': 'Airfy Beacon',
    'arduino-due': 'Arduino Due',
    'arduino-duemilanove': 'Arduino Duemilanove',
    'arduino-mega2560': 'Arduino Mega2560',
    'arduino-mkr1000': 'Arduino MKR1000',
    'arduino-mkrzero': 'Arduino MKR ZERO',
    'arduino-uno': 'Arduino Uno',
    'arduino-zero': 'Arduino Zero',
    'avsextrem': 'AVS Extrem',
    'b-l072z-lrwan1': 'STMicroelectronics B-L072Z-LRWAN1',
    'b-l475e-iot01a': 'STMicroelectronics B-L475E-IOT01A',
    'bluepill': 'Blue Pill',
    'calliope-mini': 'Calliope Mini',
    'cc2538dk': 'CC2538DK',
    'cc2650-launchpad': 'CC2650 LaunchPad',
    'cc2650stk': 'CC2650STK',
    'chronos': 'eZ430 Chronos',
    'ek-lm4f120xl': 'EK-LM4F120XL',
    'f4vi1': 'F4VI1',
    'feather-m0': 'Adafruit Feather M0',
    'fox': 'HikoB Fox',
    'frdm-k22f': 'FRDM-K22F',
    'frdm-k64f': 'FRDM-K64F',
    'ikea-tradfri': 'IKEA TRÅDFRI',
    'iotlab-a8-m3': 'IoT LAB A8-M3',
    'iotlab-m3': 'IoT LAB M3',
    'limifrog-v1': 'LimiFrog-v1',
    'maple-mini': 'Maple Mini',
    'mbed_lpc1768': 'mbed_lpc1768',
    'microbit': 'micro:bit',
    'mips-malta': 'MIPS Malta',
    'msb-430': 'MSB-430',
    'msb-430h': 'MSB-430H',
    'msba2': 'MSBA2',
    'msbiot': 'MSB-IoT',
    'mulle': 'Mulle',
    'nrf51dongle': 'nRF51 Dongle',
    'nrf52840dk': 'NRF52840DK',
    'nrf52dk': 'NRF52DK',
    'nrf6310': 'NRF6310',
    'nucleo-f030': 'Nucleo-F030',
    'nucleo-f070': 'Nucleo-F070',
    'nucleo-f072': 'Nucleo-F072',
    'nucleo-f091': 'Nucleo-F091',
    'nucleo-f103': 'Nucleo-F103',
    'nucleo-f302': 'Nucleo-F302',
    'nucleo-f303': 'Nucleo-F303',
    'nucleo-f334': 'Nucleo-F334',
    'nucleo-f401': 'Nucleo-F401',
    'nucleo-f410': 'Nucleo-F410',
    'nucleo-f411': 'Nucleo-F411',
    'nucleo-f446': 'Nucleo-F446',
    'nucleo-l053': 'Nucleo-L053',
    'nucleo-l073': 'Nucleo-L073',
    'nucleo-l152': 'Nucleo-L152',
    'nucleo-l476': 'Nucleo-L467',
    'nucleo144-f207': 'Nucleo144-F207',
    'nucleo144-f303': 'Nucleo144-F303',
    'nucleo144-f412': 'Nucleo144-F412',
    'nucleo144-f413': 'Nucleo144-F413',
    'nucleo144-f429': 'Nucleo144-F429',
    'nucleo144-f446': 'Nucleo144-F446',
    'nucleo144-f722': 'Nucleo144-F722',
    'nucleo144-f746': 'Nucleo144-F746',
    'nucleo144-f767': 'Nucleo144-F767',
    'nucleo32-f031': 'Nucleo144-F031',
    'nucleo32-f042': 'Nucleo144-F042',
    'nucleo32-f303': 'Nucleo144-F303',
    'nucleo32-l031': 'Nucleo144-F031',
    'nucleo32-l432': 'Nucleo144-F432',
    'nz32-sc151': 'NZ32-SC151',
    'opencm904': 'OpenCM9.04',
    'openmote-cc2538': 'OpenMote',
    'pba-d-01-kw2x': 'Phytec phyWAVE-KW22',
    'pca10000': 'PCA10000',
    'pca10005': 'PCA10005',
    'pic32-clicker': 'PIC32 Clicker',
    'pic32-wifire': 'PIC32 WiFire',
'qemu-i386': 'qemu-i386',
    'remote-pa': 'Zolertia remote (Prototype)',
    'remote-reva': 'Zolertia remote Rev. A',
    'remote-revb': 'Zolertia remote Rev. B',
    'ruuvitag': 'RuuviTag',
    'samd21-xpro': 'SAMD21-xpro',
    'saml21-xpro': 'SAML21-xpro',
    'samr21-xpro': 'SAMR21-xpro',
    'seeeduino_arch-pro': 'Seeeduino Arch-Pro',
    'sltb001a': 'Silicon Labs',
    'slwstk6220a': 'SLWSSTK6220A',
    'sodaq-autonomo': 'SODAQ Autonomo',
    'sodaq-explorer': 'SODAQ ExpLoRer',
    'spark-core': 'Spark Core',
    'stm32f0discovery': 'STM32F0discovery',
    'stm32f3discovery': 'STM32F3discovery',
    'stm32f4discovery': 'STM32F4discovery',
    'stm32f7discovery': 'STM32F7discovery',
    'telosb': 'TelosB',
    'thingy52': 'Nordic Thingy:52',
    'udoo': 'UDOO',
    'waspmote-pro': 'Waspmote Pro',
    'wsn430-v1_3b': 'WSN430 v1_3b',
    'wsn430-v1_4': 'WSN430 v1_4',
    'yunjia-nrf51822': 'yunjia-nrf51822',
    'z1': 'Zolertia Z1',
}


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

    for item in os.listdir(path):
        if is_valid_board(path, item):

            data = {'internal_name': item, 'display_name': replacement_dict.get(item, item), 'flash_program': 'openocd', 'transaction': transaction}
            Board.objects.update_or_create(internal_name=item, defaults=data)


def register_riot_apps():
    """
    "upload" riot applications by user "riot-community"
    """

    for i in range(len(config.application_directories)):

        application_set_dir = config.application_directories[i]
        application_set_path = os.path.join(PROJECT_ROOT_DIR, config.path_root, application_set_dir)

        for name in os.listdir(application_set_path):

            application_path = os.path.join(application_set_path, name)

            if not os.path.isfile(application_path):

                # ignoring include directories
                if name == 'include':
                    continue

                description = get_description(application_set_path, name)

                application_name = get_name(application_path, name)

                tmp_fd, tmp_file_path = tempfile.mkstemp()
                make_tarfile(tmp_file_path, application_path)

                author_user = User.objects.get(username='RIOT-community')
                token = Token.objects.get(user=author_user).key

                headers = {
                    'Authorization': 'Token ' + token,
                    'Accept': 'application/json',
                }
                payload = {
                    'name': application_name,
                    'description': escape(description),
                    'licences': None,
                    'project_page': 'https://www.riot-os.org/',
                    'app_repo_url': 'https://github.com/RIOT-OS/RIOT'
                }
                files = {'app_tarball': open(tmp_file_path, 'rb')}

                r = requests.post('http://localhost:8000/api/app/', headers=headers, data=payload, files=files)

                os.remove(tmp_file_path)

                if r.status_code not in {200, 201}:
                    print('posting app {0} failed!'.format(application_name))
                    print(r.content)

                else:
                    # auto public
                    object = Application.objects.get(name=application_name)
                    object.is_public = True
                    object.save()


def make_tarfile(output_path, source_dir):
    with tarfile.open(output_path, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


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
            with open(path) as file:

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
        with open(os.path.join(path, 'Makefile')) as makefile:
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
            register_riot_apps()
            print('OK')

        except Exception as e:
            transaction.delete()
            print('FAIL: {}'.format(str(e)))

