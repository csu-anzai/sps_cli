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

from tempfile import gettempdir

pasta_temporaria = gettempdir()

def create_lockfile(lockf):
	f = open(pasta_temporaria+os.sep+lockf,'w')
	f.close()

def remove_lockfile(lockf):
	os.remove(pasta_temporaria+os.sep+lockf)

def lockfile_name(path_to_file):
	lkf_name = path_to_file.split(os.sep)[-1]
	if lkf_name.find(".") != -1 or lkf_name.find(".") != 0:
		lkf_name = lkf_name.split(".")[0]
	file_name = '~lock_'+str(lkf_name)
	return file_name


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


def save_json(novos_dados, path_to_file, pasta_temporaria=pasta_temporaria):
	lockf = lockfile_name(path_to_file)
	initfolder = os.getcwd()
	nfo = path_to_file.split('/')
	fname = nfo[-1]
	path = path_to_file.replace(fname, '')

	while True:
		if os.path.isfile(pasta_temporaria+os.sep+lockf):
			time.sleep(0.1)
		else:
			create_lockfile(lockf)
			break

	os.chdir(path.replace('/', os.sep))
	with open(path_to_file, 'w') as f:
		f.write(json.dumps(novos_dados, ensure_ascii=False, indent=4))		

	os.chdir(initfolder)
	remove_lockfile(lockf)
