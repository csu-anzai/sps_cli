#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
#  Copyright 2017 Daniel Cruz <bwb0de@bwb0dePC>
#  bwb0de Functools Version 0.1
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

from subprocess import getoutput 

def check_config_existance(function):
	def wrapper():
		check_config = bool(getoutput('if [ -f "$(echo $HOME)/.sps-cli.conf" ]; then echo 1; else echo ""; fi'))
		if check_config == False:
			print("Arquivo local de configuração não encontrado... Execute 'sps-install config' para criá-lo... ")
		return function()
	return wrapper


def only_root(function):
	def wrapper():
		if getoutput('whoami') != 'root':
			return print("Apenas o 'root' pode executar essa ação...")
		else:
			return function()
	return wrapper