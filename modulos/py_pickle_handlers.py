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


import io
import os
import pickle

from .py_data_tools import create_lockfile, remove_lockfile, lockfile_name


def read_pickle(obj_file, folder):
	obj_file_io = io.open(os.path.join(folder, obj_file),'rb')
	OBJ = pickle.load(obj_file_io)
	return OBJ


def write_pickle(OBJ, folder, filename=None):
	if filename == None:
		obj_file = io.open(os.path.join(folder, str(OBJ.idx).zfill(3)),'wb')
	else:
		obj_file = io.open(os.path.join(folder, filename),'wb')
	pickle.dump(OBJ, obj_file)
	obj_file.close()