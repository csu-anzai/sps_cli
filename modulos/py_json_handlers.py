#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
#  Copyright 2017 Daniel Cruz <bwb0de@bwb0dePC>
#  Version 0.1
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


import os
import json
import time

from .py_euristic_tools import show_each_dictArray_block
from .py_console_tools import create_lockfile, remove_lockfile, lockfile_name 

def show_each_json_block(json_file, print_fields, index_pos):
	info_file = load_json('./{}'.format(json_file))
	show_each_dictArray_block(info_file, print_fields, index_pos)


def load_json(path_to_file):
    initfolder = os.getcwd()
    nfo = path_to_file.split('/')
    fname = nfo[-1]
    path = path_to_file.replace(fname, '')
    os.chdir(path.replace('/', os.sep))
    f = open(fname)
    data = f.read()
    f.close()
    os.chdir(initfolder)
    return json.loads(data)


def save_json(novos_dados, path_to_file):
	lockf = lockfile_name(path_to_file)
	initfolder = os.getcwd()
	nfo = path_to_file.split('/')
	fname = nfo[-1]
	path = path_to_file.replace(fname, '')

	while True:
		if os.path.isfile(lockf):
			time.sleep(0.1)
		else:
			create_lockfile(lockf)
			break

	os.chdir(path.replace('/', os.sep))
	with open(path_to_file, 'w') as f:
		f.write(json.dumps(novos_dados, ensure_ascii=False, indent=4))		

	os.chdir(initfolder)
	remove_lockfile(lockf)
