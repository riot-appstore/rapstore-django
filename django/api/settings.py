# -*- coding: UTF-8 -*-

"""
 * Copyright (C) 2018 FU Berlin and HAW Hamburg
 *
 * This file is subject to the terms and conditions of the GNU Lesser
 * General Public License v2.1. See the file LICENSE in the top level
 * directory for more details.
"""

path_root = "/RIOT/"

module_directories = [
    "sys",
    "pkg",
    "drivers"
]

application_directories = [
    "examples"
]

LOGGING_FORMAT = "[%(levelname)s]: %(asctime)s\n"\
                 + "in %(filename)s in %(funcName)s on line %(lineno)d\n"\
                 + "%(message)s\n\n"

APPLICATION_CACHE_DIR = ".application_cache"
