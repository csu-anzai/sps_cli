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
import csv
import time

from tempfile import gettempdir
from collections import OrderedDict

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


def load_csv(csv_file, delimiter='\t', lineterminator='\n'):
	'''
	Acessa o conteúdo do arquivo CSV e o armazena na memória como um list_of_dicts.
	'''
	o = []
	fields = load_csv_head(csv_file, delimiter=delimiter, lineterminator=lineterminator)
	try:
		with open(os.path.join(os.getcwd(), csv_file), encoding="utf8") as csv_fileobj:
			rd = csv.DictReader(csv_fileobj, delimiter=delimiter, lineterminator=lineterminator)
			for row in rd:
				ordered_row = OrderedDict()
				for col in fields:
					ordered_row[col] = row[col]
				o.append(ordered_row)
	except:
		with open(os.path.join(os.getcwd(), csv_file), encoding="cp1252") as csv_fileobj:
			rd = csv.DictReader(csv_fileobj, delimiter=delimiter, lineterminator=lineterminator)
			for row in rd:
				ordered_row = OrderedDict()
				for col in fields:
					ordered_row[col] = row[col]
				o.append(ordered_row)
	return o




def load_csv_head(csv_file, delimiter='\t', lineterminator='\n'):
	f = open(csv_file)
	f_csv_obj = csv.DictReader(f, delimiter=delimiter, lineterminator=lineterminator)
	header = f_csv_obj.fieldnames
	f.close()
	return header




def load_csv_col(col, csv_file, delimiter='\t', lineterminator='\n', sort_r=False):
	fd = load_csv(csv_file, delimiter=delimiter, lineterminator=lineterminator)
	o = []
	for i in fd:
		o.append(i[col])
	if sort_r == True:
		o.sort()
	return o




def fill_gaps(csv_file,refcol=[],targetcol=[],targetcolops=[]):
	conteudo = load_csv(csv_file)
	cols = load_csv_head(csv_file)
	
	print_refcol = True
	keep_working = True
	
	for l in conteudo:
		if keep_working == False:
			break
		white_cels = 0
		if targetcol == []:
			for c in l:
				if l[c] == '':
					if print_refcol == True:
						print_refcol = False
						for r in refcol:
							print(l[r])
					l[c] = input(c+': ')
				else:
					white_cels += 1
		else:
			for c in l:
				for selected in targetcol:
					print(c)
					print(selected)
					if l[selected] == '':
						if print_refcol == True:
							print_refcol = False
							for r in refcol:
								print(l[r])
					else:
						white_cels += 1			
		
		if white_cels < len(cols)-1:
			while True:
				op = input("Gravar alterações e continuar? s/n : ")
				if (op == 's') or (op == 'S'):
					save_csv(conteudo,csv_file)
					break
				elif (op == 'n') or (op == 'N'):
					keep_working = False
					break
				else:
					print('Responda [s] para sim ou [n] para não...')
			
		print_refcol = True
	
	return conteudo




def extract_lines(csv_file, csv_col, test_value, delimiter='\t', backup_2_trash=True):
	conteudo = load_csv(csv_file, delimiter=delimiter)
	keep_this = []
	remove_that = []
	for line in conteudo:
		if line[csv_col] == test_value:
			remove_that.append(line)
		else:
			keep_this.append(line)
	op = input("Deseja remover as {} linhas encontradas na tabela? (s/n)".format(len(remove_that)))
	if op == "s" or op == "S":
		save_csv(keep_this, csv_file)
		if backup_2_trash == True:
			new_csv_file = time.ctime().replace(' ','_') + "_rmLines_from_" + csv_file
			save_csv(remove_that, new_csv_file)




def copy_col(csv_file, source_col, destination_col):
	"Copia o conteúdo de uma coluna alvo para uma coluna de destino se a célula do destino ainda não estiver preechida"
	conteudo = load_csv(csv_file)
	cols = load_csv_head(csv_file)
	change_info = False
	if destination_col in cols:
		for line in conteudo:
			if line[source_col] != '' and line[destination_col] == '':
				change_info = True
				line[destination_col] = line[source_col]
	else:
		for line in conteudo:
			line[destination_col] = ''
			if line[source_col] != '' and line[destination_col] == '':
				change_info = True
				line[destination_col] = line[source_col]		
	
	if change_info == True:
		print("Cópia efetuada...")
		save_csv(conteudo, csv_file)
	else:
		print("Não há o que alterar...")




def add_line(csv_file, refcols=[]):
	conteudo = load_csv(csv_file)
	cols = load_csv_head(csv_file)
	nova_linha = OrderedDict()
	for c in cols:
		v = input(c+": ")
		nova_linha[c] = v
		
	conteudo.append(nova_linha)
	save_csv(conteudo, csv_file)
	v = input("Adicionar outro? (s/n) ")
	if v == "s" or v == "S":
		add_line(csv_file)



def convert_csv_type(csv_file, old_delimiter, new_delimiter, old_lineterminator=os.linesep, new_lineterminator=os.linesep):
	conteudo = load_csv(csv_file, delimiter=old_delimiter, lineterminator=old_lineterminator)
	save_csv(conteudo, csv_file, delimiter=new_delimiter, lineterminator=new_lineterminator)



def save_csv(list_of_dicts, path_to_file, header=None, delimiter='\t', lineterminator='\n', pasta_temporaria=pasta_temporaria):
	'''
	Escreve o conteudo de uma lista de dicionários em um arquivo CSV.
	Esta função gera um arquivo de trava até que o processo seja concluído impossibilitanto a realização de cópias simultâneas.
	A ordem do cabeçalho pode ser definido arbitrariamente mediante a inclusão de uma lista com o come das colunas na argumento "header".
	'''

	fields = list_of_dicts[0].keys()
	lockf = lockfile_name(path_to_file)
	initfolder = os.getcwd()

	while True:
		if os.path.isfile(pasta_temporaria+os.sep+lockf):
			time.sleep(0.1)
		else:
			create_lockfile(lockf)
			break

	with open(path_to_file, 'w') as f:
		w = csv.DictWriter(f, fields, delimiter=delimiter, lineterminator=lineterminator)
		w.writeheader()
		w.writerows(list_of_dicts)

	os.chdir(initfolder)
	remove_lockfile(lockf)

