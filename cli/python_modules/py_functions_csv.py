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
import re
import time

from .py_euristic_tools import merge_lists, join_dictArray_intersection, join_dictArray_union, show_each_dictArray_block
from .cli_tools import limpar_tela, select_ops, create_lockfile, remove_lockfile, lockfile_name
from .cli_machine_info import tmpdir
from collections import OrderedDict
from copy import copy


def show_each_csv_line(csv_file, print_fields, index_pos):
	info_file = read_csv('./{}'.format(csv_file))
	show_each_dictArray_block(info_file, print_fields, index_pos)


def read_csv(csv_file, delimiter=',', lineterminator='\n'):
	'''
	Acessa o conteúdo do arquivo CSV e o armazena na memória como um dict_array.
	'''
	o = []
	fields = read_csv_head(csv_file, delimiter=delimiter, lineterminator=lineterminator)
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




def read_csv_head(csv_file, delimiter=',', lineterminator='\n'):
	f = open(csv_file)
	f_csv_obj = csv.DictReader(f, delimiter=delimiter, lineterminator=lineterminator)
	header = f_csv_obj.fieldnames
	f.close()
	return header




def read_csv_col(col, csv_file, delimiter=',', lineterminator='\n', sort_r=False):
	fd = read_csv(csv_file, delimiter=delimiter, lineterminator=lineterminator)
	o = []
	for i in fd:
		o.append(i[col])
	if sort_r == True:
		o.sort()
	return o




def join_csv_intersection(csvfile1, csvfile2, col, output_file=True):
	'''
	Realiza a junção de dois dicionários distintos que compartilhem uma mesma chave/col.
	Retorna as linhas em que os valores da chave selecionada correspondem nos dois dicionários.
	'''
	csvdata1 = read_csv(csvfile1)
	csvdata2 = read_csv(csvfile2)
	output = join_dictArray_intersection(csvdata1, csvdata2, col)
	if output_file == True:
		fname = input("Qual o nome do arquivo de saída?")
		write_csv(output, fname)
	else:
		return output



def join_csv_union(csvfile1, csvfile2, col, output_file=True):
	'''
	Realiza a junção de dois dicionários distintos que compartilhem uma mesma chave/col.
	Retorna as linhas em que os valores da chave selecionada correspondem nos dois dicionários.
	'''
	csvdata1 = read_csv(csvfile1)
	csvdata2 = read_csv(csvfile2)
	output = join_dictArray_union(csvdata1, csvdata2, col)
	if output_file == True:
		fname = input("Qual o nome do arquivo de saída?")
		write_csv(output, fname)
	else:
		return output




def obter_frq_abs(csv_file, col=False):
	'''Retorna os diferentes valores existentes na coluna 'col' para a 'tabela' do mysql selecionada junto com suas respectivas quantidades.'''
	fields = read_csv_head(csv_file)
	if col != False:
		selected_cols = [col]
	else:
		selected_cols = select_ops(fields, 2)
	content = read_csv(csv_file)
	o = OrderedDict()
	for f in selected_cols:
		query_list = []
		for line in content:
			query_list.append(line[f])
		query_list_entries = set(query_list)
		itens_count = OrderedDict()
		for itens in query_list_entries:
			o[itens]=query_list.count(itens)
	return o




def obter_frq_abs_e_rel(csv_file, col=False):
	f = open(os.path.join(os.getcwd(), csv_file), 'r')
	n = int(len(f.readlines())-1)
	r = obter_frq_abs(csv_file, col)
	o = OrderedDict()
	for cols in r.keys():
		o[cols] = (r[cols], float((r[cols]/n)*100))
	return o



def cruzar_variaveis(csv_file):
	arquivo_de_saida = input("Salvar resultado como...: ")
	limpar_tela()
	fields = read_csv_head(csv_file)
	selected_cols = select_ops(fields, 2)
	selected_cols_len = len(selected_cols)
	print("Selecionadas: ", selected_cols, selected_cols_len)
	set_of_values = []
	while selected_cols_len != 0:
		col_values = read_csv_col(selected_cols[selected_cols_len-1], csv_file)
		set_of_values.append(set(col_values))
		selected_cols_len -= 1
	print("Valores encontrados: ", set_of_values)
	o = OrderedDict()
	set_of_values_len = []
	for i in set_of_values:
		set_of_values_len.append(len(i))
	print("Número de valores diferentes: ", set_of_values_len)
	list_of_cross_values = []
	list_of_cross_values_len = 0

	r = []
	if len(selected_cols) == 1:
		print("É necessário escolher mais de uma coluna para efetuar o cruzamento...")
	elif len(selected_cols) == 2:
		for lines in read_csv(csv_file):
			r.append(" e ".join([lines[selected_cols[0]],lines[selected_cols[1]]]))
	elif len(selected_cols) == 3:
		for lines in read_csv(csv_file):
			r.append(" e ".join([lines[selected_cols[0]],lines[selected_cols[1]],lines[selected_cols[2]]]))
	elif len(selected_cols) == 4:
		for lines in read_csv(csv_file):
			r.append(" e ".join([lines[selected_cols[0]],lines[selected_cols[1]],lines[selected_cols[2]],lines[selected_cols[3]]]))
	elif len(selected_cols) == 5:
		for lines in read_csv(csv_file):
			r.append(" e ".join([lines[selected_cols[0]],lines[selected_cols[1]],lines[selected_cols[2]],lines[selected_cols[3]],lines[selected_cols[4]]]))
	elif len(selected_cols) == 6:
		for lines in read_csv(csv_file):
			r.append(" e ".join([lines[selected_cols[0]],lines[selected_cols[1]],lines[selected_cols[2]],lines[selected_cols[3]],lines[selected_cols[4]],lines[selected_cols[5]]]))
	elif len(selected_cols) == 7:
		for lines in read_csv(csv_file):
			r.append(" e ".join([lines[selected_cols[0]],lines[selected_cols[1]],lines[selected_cols[2]],lines[selected_cols[3]],lines[selected_cols[4]],lines[selected_cols[5]],lines[selected_cols[6]]]))
	elif len(selected_cols) == 8:
		for lines in read_csv(csv_file):
			r.append(" e ".join([lines[selected_cols[0]],lines[selected_cols[1]],lines[selected_cols[2]],lines[selected_cols[3]],lines[selected_cols[4]],lines[selected_cols[5]],lines[selected_cols[6]],lines[selected_cols[7]]]))
	elif len(selected_cols) == 9:
		for lines in read_csv(csv_file):
			r.append(" e ".join([lines[selected_cols[0]],lines[selected_cols[1]],lines[selected_cols[2]],lines[selected_cols[3]],lines[selected_cols[4]],lines[selected_cols[5]],lines[selected_cols[6]],lines[selected_cols[7]],lines[selected_cols[8]]]))
	elif len(selected_cols) == 10:
		for lines in read_csv(csv_file):
			r.append(" e ".join([lines[selected_cols[0]],lines[selected_cols[1]],lines[selected_cols[2]],lines[selected_cols[3]],lines[selected_cols[4]],lines[selected_cols[5]],lines[selected_cols[6]],lines[selected_cols[7]],lines[selected_cols[8]],lines[selected_cols[9]]]))
	else:
		print("Quantidade máxima de cruzamentos atingida...")

	r_set = set(r)
	o = OrderedDict()
	n = len(r)

	for i in r_set:
		o[i] = (r.count(i), float((r.count(i)/n)*100))

	o_file_data = ''
	for i in o.keys():
		o_file_data += str(i) + "," + str(o[i][0]) + "," + str(o[i][1]) + os.linesep
	f = open(arquivo_de_saida, 'w')
	f.write(o_file_data)
	f.close()

	return o




def fill_gaps(csv_file,refcol=[],targetcol=[],targetcolops=[]):
	conteudo = read_csv(csv_file)
	cols = read_csv_head(csv_file)
	linha_editada = OrderedDict()
	
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
						limpar_tela()
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
							limpar_tela()
							for r in refcol:
								print(l[r])
						try:
							op_grp = tergetcol.index(c)
							o = select_ops(targetcolops[op_grp], 2)
						except:
							l[selected] = input(selected+': ')
					else:
						white_cels += 1			
		
		if white_cels < len(cols)-1:
			while True:
				op = input("Gravar alterações e continuar? s/n : ")
				if (op == 's') or (op == 'S'):
					write_csv(conteudo,csv_file)
					break
				elif (op == 'n') or (op == 'N'):
					keep_working = False
					break
				else:
					print('Responda [s] para sim ou [n] para não...')
			
		print_refcol = True
	
	return conteudo




def remove_lines(csv_file, csv_col, test_value, delimiter='\t', backup_2_trash=True):
	conteudo = read_csv(csv_file, delimiter=delimiter)
	keep_this = []
	remove_that = []
	for line in conteudo:
		if line[csv_col] == test_value:
			remove_that.append(line)
		else:
			keep_this.append(line)
	op = input("Deseja remover as {} linhas encontradas na tabela? (s/n)".format(len(remove_that)))
	if op == "s" or op == "S":
		write_csv(keep_this, csv_file)
		if backup_2_trash == True:
			new_csv_file = time.ctime().replace(' ','_') + "_rmLines_from_" + csv_file
			write_csv(remove_that, new_csv_file)




def copy_col(csv_file, source_col, destination_col):
	"Copia o conteúdo de uma coluna alvo para uma coluna de destino se a célula do destino ainda não estiver preechida"
	conteudo = read_csv(csv_file)
	novo_conteudo = []
	cols = read_csv_head(csv_file)
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
		write_csv(conteudo, csv_file)
	else:
		print("Não há o que alterar...")




def add_line(csv_file, refcols=[]):
	limpar_tela()
	conteudo = read_csv(csv_file)
	cols = read_csv_head(csv_file)
	nova_linha = OrderedDict()
	for c in cols:
		v = input(c+": ")
		nova_linha[c] = v
		
	conteudo.append(nova_linha)
	write_csv(conteudo, csv_file)
	v = input("Adicionar outro? (s/n) ")
	if v == "s" or v == "S":
		add_line(csv_file)



def convert_csv_type(csv_file, old_delimiter, new_delimiter, old_lineterminator=os.linesep, new_lineterminator=os.linesep):
	conteudo = read_csv(csv_file, delimiter=old_delimiter, lineterminator=old_lineterminator)
	write_csv(conteudo, csv_file, delimiter=new_delimiter, lineterminator=new_lineterminator)


def write_csv(novos_dados, path_to_file, header=None, delimiter=',', lineterminator='\n', tmpdir=tmpdir):
	'''
	write_csv(csv_data_list, csv_file, header=None) -> escreve o conteudo de uma lista de dicionários em um arquivo CSV.
	
	Esta função gera um arquivo de trava até que o processo seja concluído impossibilitanto a realização de cópias simultâneas. A ordem do cabeçalho pode ser definido arbitrariamente mediante a inclusão de uma lista com o come das colunas na argumento "header".
	'''

	fields = novos_dados[0].keys()
	lockf = lockfile_name(path_to_file)
	initfolder = os.getcwd()
	nfo = path_to_file.split('/')
	fname = nfo[-1]
	path = path_to_file.replace(fname, '')

	while True:
		if os.path.isfile(tmpdir+os.sep+lockf):
			time.sleep(0.1)
		else:
			create_lockfile(lockf)
			break

	os.chdir(path.replace('/', os.sep))
	with open(path_to_file, 'w') as f:
		w = csv.DictWriter(f, fields, delimiter=delimiter, lineterminator=lineterminator)
		w.writeheader()
		w.writerows(novos_dados)

	os.chdir(initfolder)
	remove_lockfile(lockf)




def make_complete_stat_from_csv(csv_file,printout=True):
	fields = read_csv_head(csv_file)
	o = OrderedDict()
	for field in fields:
		colcount = obter_frq_abs_e_rel(csv_file, field)
		o[field] = colcount
	
	printcontent = ''
	
	for k in o.keys():
		if printout == True:
			print("Variável: "+k)
		printcontent += "Variável: " + k + os.linesep
		for v in o[k].keys():
			if printout == True:
				print("  » "+v, o[k][v])
			printcontent += "  » " + v + ' ' + str(o[k][v]) + os.linesep
		if printout == True:
			print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="+os.linesep)
		printcontent += "=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=" + os.linesep
		
	if printout == 'file':
		fn = input("Escolha o nome do arquivo de destino: ")
		f = open(fn, 'w')
		f.write(printcontent)
		f.close()
				
	return o



def map_values_in_csv_col(csv_file):#map_values_in_csv_col(col, csv_file):
	'''Retorna os diferentes valores existentes na coluna 'col' para a 'tabela' do mysql selecionada.'''
	output = obter_frq_abs(csv_file)#, col)
	output = output.keys()
	return output





