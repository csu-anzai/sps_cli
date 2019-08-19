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
import io
import pickle
import json
import csv
import tempfile
import time

from colored import fg, bg, attr
from subprocess import getoutput
from random import randrange
from string import whitespace, punctuation, digits
from collections import OrderedDict
from copy import copy

time.strptime('02/01/1986','%d/%m/%Y')

pasta_temporaria = tempfile.gettempdir()

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


def point_to_json(path_to_file):
	print('Generating {}'.format(path_to_file))
	with open(path_to_file) as f:
		for line in f.readlines():
			yield line



def load_text_db_line(text_db_file_generator):
	for line in text_db_file_generator:
		yield line.split(':')



def load_text_db_file(path_to_file):
	with open(path_to_file) as f:
		for line in f.readlines():
			yield line


def save_text_db_file(novos_dados, path_to_file, pasta_temporaria=pasta_temporaria):
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
		f.write(novos_dados)

	os.chdir(initfolder)
	remove_lockfile(lockf)



def load_json(path_to_file):
	with open(path_to_file) as f:
		data = f.read()
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



def listagem_cli(linhas_selecionadas, cols):
	visual_count = len(linhas_selecionadas)
	for linha in linhas_selecionadas:
		visual_nfo = ""
		w = 0
		li = ""
		linha_sem_quebra = True
		for col in cols:
			if linha.get(col[0]):
				li += linha[col[0]].ljust(col[1])
				if linha[col[0]].find(';') == -1:
					w += col[1]
				else:
					linha_sem_quebra = False
					lii = li.split(';')
					if len(lii) > 1:
						pri = True
						for i in lii:
							if pri == True:
								visual_nfo += i + os.linesep
								pri = False
							else:
								visual_nfo += "".ljust(w-1) + i + os.linesep
								yield visual_nfo
			else:
				li += "".ljust(col[1])

		
		if linha_sem_quebra == True:
			visual_nfo += li 
			yield visual_nfo
	
	yield "Total: {}".format(visual_count)


def listagem_json(linhas_selecionadas, cols):
	selected_cols = []
	for linha in linhas_selecionadas:
		l = {}
		for col in cols:
			l[col[0]] = linha[col[0]]
		selected_cols.append(l)
	return json.dumps(selected_cols, ensure_ascii=False, indent=4)


def listar_dicionario(dicionario, cols, marcadores=[], tipo_output='cli'):
	'''
	Lista o conteúdo de um dicionário retornando uma tabela/string com colunas solicitadas.
	O parametro 'cols' é uma lista de tuplas (t) em que t[0] é o 'id' e t[1] um número.
	O número de t[1] representa a largura a ser definida para coluna id ou t[0].
	Exibe ao final o total de elementos no dicionário.
	'''

	r = []
	for linha in dicionario:
		select_this = True
		if marcadores != []:
			select_this = False
			try:
				for m in marcadores:
					if m in linha['marcador']:
						select_this = True
			except KeyError:
				pass

		if select_this == True:
			r.append(linha)


	if tipo_output == 'cli':
		visual_nfo = listagem_cli(r, cols)
	
	elif tipo_output == 'json':
		visual_nfo = listagem_json(r, cols)

	return visual_nfo


def obter_frq_abs_from_list_of_dicts(list_of_dicts, key=False):
	'''
	Retorna os diferentes valores existentes na chave 'key' para o 'list_of_dicts'.
	Retorna o valor absoluto das ocorrências de valores.

	'''
	
	#Assuming every dict on the list has the same structure...
	fields = list_of_dicts[0].keys()


	if key != False:
		selected_cols = [key]
	else:
		selected_cols = select_ops(fields, 2)
	
	o = OrderedDict()
	
	for f in selected_cols:
		query_list = []
		for line in list_of_dicts:
			query_list.append(line[f])
		query_list_entries = set(query_list)
		for itens in query_list_entries:
			o[itens]=query_list.count(itens)
	return o



def obter_frq_abs_e_rel_from_list_of_dicts(list_of_dicts, key=False):
	n = len(list_of_dicts)
	r = obter_frq_abs_from_list_of_dicts(list_of_dicts, key)
	o = OrderedDict()
	for k in r.keys():
		o[k] = (r[k], float((r[k]/n)*100.00))
	return o


def make_complete_stat_from_list_of_dicts(list_of_dicts, printout=True):
	fields = list_of_dicts[0].keys
	o = OrderedDict()
	for field in fields:
		colcount = obter_frq_abs_e_rel_from_list_of_dicts(list_of_dicts, field)
		o[field] = colcount
	
	for k in o.keys():
		print("Variável: "+k)
		for v in o[k].keys():
			print("  » "+v, o[k][v])
		print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="+os.linesep)



def map_values_in_list_of_dicts_col(list_of_dicts):
	'''
	Retorna os diferentes valores existentes na coluna 'col' para a 'tabela' do mysql selecionada.
	'''

	output = obter_frq_abs_from_list_of_dicts(list_of_dicts)
	output = output.keys()
	return output




def show_each_dict_in_block(list_of_dicts, print_fields, index_pos):
	'''
	Apresenta bloco de informações de um 'list_of_dicts'.
	Apenas os campos definidos em 'print_fields' serão retornados.
	A cada impressão o programa aquarda pelo comando para prosseguir.
	Elementos iniciais da lista podem ser ignorados definindo-se o local de inicio 'index_pos'.
	'''

	for i in list_of_dicts[index_pos:]:
		print_nfo = ""
		for f in print_fields:
			print_nfo += i[f].replace('/','') + os.linesep
		print(print_nfo)
		input("Pressione enter para continuar...")



def join_list_of_dicts_intersection(list_of_dicts1, list_of_dicts2, joint_key):
	'''
	Realiza a junção de dois dicionários distintos que compartilhem uma mesma chave/col.
	Retorna as linhas em que os valores da chave selecionada correspondem nos dois dicionários.
	'''

	output = []
	tmpdict = {}
	for row in list_of_dicts1:
		tmpdict[row[joint_key]] = row
	list_of_dicts2_cols = list_of_dicts2[0].keys()
	for other_row in list_of_dicts2:
		if other_row[joint_key] in tmpdict: #tmpdict.has_key(other_row[col]):
			joined_row = tmpdict[other_row[joint_key]]
			for colz in list_of_dicts2_cols:
				if colz != joint_key:
					joined_row[colz] = other_row[colz]
			output.append(joined_row)
	return output



def join_list_of_dicts_union(list_of_dicts1, list_of_dicts2, joint_key):
	'''
	Realiza a junção de dois dicionários distintos que compartilhem uma mesma chave/col.
	Retorna as linhas em que os valores da chave selecionada correspondem nos dois dicionários.
	'''

	output = []
	tmpdict = {}
	list_of_dicts1_cols = list_of_dicts1[0].keys()
	list_of_dicts2_cols = list_of_dicts2[0].keys()
	for row in list_of_dicts1:
		tmpdict[row[joint_key]] = row
	new_row_col = merge_lists(list_of_dicts1_cols,list_of_dicts2_cols)
	new_row_skell = OrderedDict()
	for col_name in new_row_col:
		new_row_skell[col_name]=""
	
	key_2_skip = []
	for other_row in list_of_dicts2:
		if other_row[joint_key] in tmpdict:
			key_2_skip.append(other_row[joint_key])
			joined_row = tmpdict[other_row[joint_key]]
			for colz in list_of_dicts2_cols:
				if colz != joint_key:
					joined_row[colz] = other_row[colz]
			output.append(joined_row)
		
	linhas_n_comuns = len(list_of_dicts1) + len(list_of_dicts1) - len(key_2_skip)
	tabela_linhas_n_comuns = []
	while linhas_n_comuns != 0:
		linha_inteira = copy(new_row_skell)
		tabela_linhas_n_comuns.append(linha_inteira)
		linhas_n_comuns -= 1
	
	tabela_linhas_n_comuns=[]
	
	for linha in list_of_dicts1:
		linha_inteira = copy(new_row_skell)
		if not linha[joint_key] in key_2_skip:
			for colz in list_of_dicts1_cols:
				try: linha_inteira[colz] = linha[colz]
				except: pass
			tabela_linhas_n_comuns.append(linha_inteira)

	for linha in list_of_dicts2:
		linha_inteira = copy(new_row_skell)
		if not linha[joint_key] in key_2_skip:
			for colz in list_of_dicts2_cols:
					linha_inteira[colz] = linha[colz]
			tabela_linhas_n_comuns.append(linha_inteira)
		
	final_output = merge_lists(tabela_linhas_n_comuns, output)
	return final_output




def cruzar_variaveis(list_of_dicts):
	arquivo_de_saida = input("Salvar resultado como...: ")
	limpar_tela()
	fields = list_of_dicts[0].keys()
	selected_cols = select_ops(fields, 2)
	selected_cols_len = len(selected_cols)
	print("Selecionadas: ", selected_cols, selected_cols_len)
	set_of_values = []
	while selected_cols_len != 0:
		col_values = []
		for line in list_of_dicts:
			col_values.append(line[selected_cols[selected_cols_len-1]])
		set_of_values.append(set(col_values))
		selected_cols_len -= 1
	print("Valores encontrados: ", set_of_values)
	o = OrderedDict()
	set_of_values_len = []
	for i in set_of_values:
		set_of_values_len.append(len(i))
	print("Número de valores diferentes: ", set_of_values_len)

	r = []
	if len(selected_cols) == 1:
		print("É necessário escolher mais de uma coluna para efetuar o cruzamento...")
	elif len(selected_cols) == 2:
		for lines in list_of_dicts:
			r.append(" e ".join([lines[selected_cols[0]],lines[selected_cols[1]]]))
	elif len(selected_cols) == 3:
		for lines in list_of_dicts:
			r.append(" e ".join([lines[selected_cols[0]],lines[selected_cols[1]],lines[selected_cols[2]]]))
	elif len(selected_cols) == 4:
		for lines in list_of_dicts:
			r.append(" e ".join([lines[selected_cols[0]],lines[selected_cols[1]],lines[selected_cols[2]],lines[selected_cols[3]]]))
	elif len(selected_cols) == 5:
		for lines in list_of_dicts:
			r.append(" e ".join([lines[selected_cols[0]],lines[selected_cols[1]],lines[selected_cols[2]],lines[selected_cols[3]],lines[selected_cols[4]]]))
	elif len(selected_cols) == 6:
		for lines in list_of_dicts:
			r.append(" e ".join([lines[selected_cols[0]],lines[selected_cols[1]],lines[selected_cols[2]],lines[selected_cols[3]],lines[selected_cols[4]],lines[selected_cols[5]]]))
	elif len(selected_cols) == 7:
		for lines in list_of_dicts:
			r.append(" e ".join([lines[selected_cols[0]],lines[selected_cols[1]],lines[selected_cols[2]],lines[selected_cols[3]],lines[selected_cols[4]],lines[selected_cols[5]],lines[selected_cols[6]]]))
	elif len(selected_cols) == 8:
		for lines in list_of_dicts:
			r.append(" e ".join([lines[selected_cols[0]],lines[selected_cols[1]],lines[selected_cols[2]],lines[selected_cols[3]],lines[selected_cols[4]],lines[selected_cols[5]],lines[selected_cols[6]],lines[selected_cols[7]]]))
	elif len(selected_cols) == 9:
		for lines in list_of_dicts:
			r.append(" e ".join([lines[selected_cols[0]],lines[selected_cols[1]],lines[selected_cols[2]],lines[selected_cols[3]],lines[selected_cols[4]],lines[selected_cols[5]],lines[selected_cols[6]],lines[selected_cols[7]],lines[selected_cols[8]]]))
	elif len(selected_cols) == 10:
		for lines in list_of_dicts:
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




def get_indexes(item, lista):
	'''
	Retorna os índices de um elemento em uma lista. Usado em listas que possuam elementos repitidos.
	'''

	loops = lista.count(item)
	r = []
	idx = 0
	while loops != 0:
		try:
			nidx = lista[idx:].index(item)
			r.append(nidx+idx)
			idx = nidx+1
			loops -= 1
		except ValueError:
			break
	return r



def diff_lists(a, b):
	'''Retorna os itens da lista "a" que não estão em "b".'''
	o = []
	for i in a:
		if i not in b:
			o.append(i)
	return o




def compare_lists(a, b, historical_analisis=False, listA_NAME='First', listB_NAME='Second'):
	'''
	Compara duas listas e retorna um dicionário que agrupa itens exclusivos e compartilhados.
	Se historical_analisis=True, apresenta uma única lista mostrando o que mudou na lista [b] em relação a [a].
	Os argumentos listA_NAME e listB_NAME permitem usar nomes específicos para as listas.
	'''
	o = {}
	if historical_analisis == True:
		#A segunda lista deve ser a mais nova para que os valores retornados sejam os mais atuais...
		o[u'mudou'] = diff_lists(b,a)
	else:
		o[u'onlyOn%s' % listA_NAME] = diff_lists(a,b)
		o[u'onlyOn%s' % listB_NAME] = diff_lists(b,a)
		o[u'shared'] = intersect_lists(a,b)
	return o




def diff_dicts(a, b, historical_analisis=True):
	'''
	Realiza a comparação entre dois dicionários retornando o que mudou no segundo [b] em relação ao primeiro [a].
	Se historical_analisis=False, retorna um dicionário agrupando itens exclusivos e compartilhados dessas listas.
	'''
	k = []
	for i in a.keys():
		k.append(i)
	k.sort()
	l1 = []
	l2 = []
	for i in k:
		l1.append((i, a[i]))
		l2.append((i, b[i]))
	o = compare_lists(l1, l2, historical_analisis)
	return o




def merge_lists(a, b):
	'''Retorna a lista de união, sem repetição de itens existentes em ambas as listas.'''
	o = []
	for i in b:
		o.append(i)
	for i in a:
		if i not in b:
			o.append(i)
	return o




def intersect_lists(a, b):
	'''Retorna a lista com itens comuns a partir de duas listas de entrada.'''
	o = []
	tl = merge_lists(a,b)
	for i in tl:
		if (i in a) and (i in b):
			o.append(i)
	return o



def show_dict_data(d, ofname):
	'''Apenas retorna as chaves e os valores de um dicionário no formato de lista, obedecendo o layout "KEY » VALUE". '''
	o = u''
	for i in sorted(d.keys()):
		o = o + u"Coluna/Variável: "+i.decode('utf-8')+u'\n'
		for ii in sorted(d[i].keys()):
			o = o + u"  --> %s:" % ii.decode('utf-8') + str(d[i][ii]) +'\n'
		o = o + '\n'
	f = open(ofname,'w')
	f.write(o.encode('utf-8'))
	f.close()



def strip_digits(s):
	r = s
	for i in digits:
		r = r.replace(i,'')
	return r


def strip_simbols(s):
	r = s
	for i in punctuation+"/":
		r = r.replace(i,"")
	return r

def strip_spaces(s):
	r = s
	for i in whitespace:
		r = r.replace(i,"")
	return r

def strip_chars(s):
	r = s
	for i in "abcdefghijklmnopqrstuvxz":
		r = r.replace(i,"")
	return r


def create_new_value_col_if_old_has_value(list_of_dicts, list_of_old_cols, interactive=True, script_descriptor=None):
	num_of_cols = len(list_of_old_cols)

	if (interactive == False) and (script_descriptor == None):
		if type(script_descriptor) != dict:
			print("Descritor não apresentado ou em formato inadequado...")
			exit()

	if num_of_cols == 1:

		old_col1 = list_of_old_cols[0]
		old_col1_values = []
		for line in list_of_dicts:
			if not line[old_col1] in old_col1_values:
				old_col1_values.append(line[old_col1])
		old_col1_values.sort()

		if interactive == True:
			print("Selecione os valores que deverão ser checados para disparar o gatilho de registro:")
			selected = select_ops(old_col1_values, 2)
			print("Defina o nome da nova coluna:")
			print("Cuidado! Se o nome definido for igual a un nome anteriormente existente, as informações anteriores dessa coluna serão sobrescritas:\n")
			new_col_name = input("$: ")
			print("Defina o valor que deverá ser registrado na nova coluna quando os valores selecionados forem encontrados: \n")
			new_value = input("$: ")
		else:
			selected = script_descriptor['valores_de_checagem'][list_of_old_cols[0]]
			new_col_name = script_descriptor['nome_da_nova_coluna']
			new_value = script_descriptor['valor_se_checagem_verdadeira']

		for line in list_of_dicts:
			if line.get(new_col_name) == None:
				line[new_col_name] = ""
			if line[old_col1] in selected:
				line[new_col_name] = new_value
	
	elif num_of_cols == 2:
	
		old_col1 = list_of_old_cols[0]
		old_col2 = list_of_old_cols[1]
		old_col1_values = []
		old_col2_values = []
	
		for line in list_of_dicts:
			if not line[old_col1] in old_col1_values:
				old_col1_values.append(line[old_col1])
			if not line[old_col2] in old_col2_values:
				old_col2_values.append(line[old_col2])
	
		old_col1_values.sort()
		old_col2_values.sort()

		if interactive == True:
			print("Selecione os valores que deverão ser checados para disparar o gatilho de registro na coluna {}:".format(list_of_old_cols[0]))
			selected_itens_col1 = select_ops(old_col1_values, 2)
			print("Selecione os valores que deverão ser checados para disparar o gatilho de registro na coluna {}:".format(list_of_old_cols[1]))
			selected_itens_col2 = select_ops(old_col2_values, 2)

			print("Defina o nome da nova coluna:")
			print("Cuidado! Se o nome definido for igual a un nome anteriormente existente, as informações anteriores dessa coluna serão sobrescritas:\n")
			new_col_name = input("$: ")

			print("Defina o valor que deverá ser registrado na nova coluna quando os valores selecionados forem encontrados: \n")
			new_value = input("$: ")
		else:
			selected_itens_col1 = script_descriptor['valores_de_checagem'][list_of_old_cols[0]]
			selected_itens_col2 = script_descriptor['valores_de_checagem'][list_of_old_cols[1]]
			new_col_name = script_descriptor['nome_da_nova_coluna']
			new_value = script_descriptor['valor_se_checagem_verdadeira']

		for line in list_of_dicts:
			if line.get(new_col_name) == None:
				line[new_col_name] = ""
			if (line[old_col1] in selected_itens_col1) and (line[old_col2] in selected_itens_col2):
				line[new_col_name] = new_value
	
	elif num_of_cols == 3:
		old_col1 = list_of_old_cols[0]
		old_col2 = list_of_old_cols[1]
		old_col3 = list_of_old_cols[2]
		old_col1_values = []
		old_col2_values = []
		old_col3_values = []

		if interactive == True:

			for line in list_of_dicts:
				if not line[old_col1] in old_col1_values:
					old_col1_values.append(line[old_col1])
				if not line[old_col2] in old_col2_values:
					old_col2_values.append(line[old_col2])
				if not line[old_col3] in old_col3_values:
					old_col3_values.append(line[old_col3])				

			old_col1_values.sort()
			old_col2_values.sort()
			old_col3_values.sort()

			print("Selecione os valores que deverão ser checados para disparar o gatilho de registro na coluna {}:".format(old_col1))
			selected_itens_col1 = select_ops(old_col1_values, 2)
			print("Selecione os valores que deverão ser checados para disparar o gatilho de registro na coluna {}:".format(old_col2))
			selected_itens_col2 = select_ops(old_col2_values, 2)
			print("Selecione os valores que deverão ser checados para disparar o gatilho de registro na coluna {}:".format(old_col3))
			selected_itens_col3 = select_ops(old_col3_values, 2)

			print("Defina o nome da nova coluna:")
			print("Cuidado! Se o nome definido for igual a un nome anteriormente existente, as informações anteriores dessa coluna serão sobrescritas:\n")
			new_col_name = input("$: ")

			print("Defina o valor que deverá ser registrado na nova coluna quando os valores selecionados forem encontrados: \n")
			new_value = input("$: ")
		else:
			selected_itens_col1 = script_descriptor['valores_de_checagem'][list_of_old_cols[0]]
			selected_itens_col2 = script_descriptor['valores_de_checagem'][list_of_old_cols[1]]
			selected_itens_col3 = script_descriptor['valores_de_checagem'][list_of_old_cols[2]]

			new_col_name = script_descriptor['nome_da_nova_coluna']
			new_value = script_descriptor['valor_se_checagem_verdadeira']

		count = 0
		for line in list_of_dicts:
			count += 1

			if line.get(new_col_name) == None:
				line[new_col_name] = ""

			if selected_itens_col1.find(line[old_col1]) != -1:
				if selected_itens_col2.find(line[old_col2]) != -1:
					if selected_itens_col3.find(line[old_col3]) != -1:

						print("Encontrada correspondência na linha: {} » {} ".format(count, line["NOME_ESTUDANTE"]))
						print("  ·", old_col1, "»» {} in {}".format(line[old_col1], selected_itens_col1))
						print("  ·", old_col2, "»» {} in {}".format(line[old_col2], selected_itens_col2))
						print("  ·", old_col3, "»» {} in {}".format(line[old_col3], selected_itens_col3))	
						print("")
						if line["NOME_ESTUDANTE"] == "Rodrigo Ramos de Lima":
							input()

						line[new_col_name] = new_value

		return list_of_dicts

	elif num_of_cols == 4:

		old_col1 = list_of_old_cols[0]
		old_col2 = list_of_old_cols[1]
		old_col3 = list_of_old_cols[2]
		old_col4 = list_of_old_cols[4]
		old_col1_values = []
		old_col2_values = []
		old_col3_values = []
		old_col4_values = []

		for line in list_of_dicts:
			if not line[old_col1] in old_col1_values:
				old_col1_values.append(line[old_col1])
			if not line[old_col2] in old_col2_values:
				old_col2_values.append(line[old_col2])
			if not line[old_col3] in old_col3_values:
				old_col3_values.append(line[old_col3])
			if not line[old_col4] in old_col4_values:
				old_col4_values.append(line[old_col4])								

		old_col1_values.sort()
		old_col2_values.sort()
		old_col3_values.sort()
		old_col4_values.sort()

		if interactive == True:
			print("Selecione os valores que deverão ser checados para disparar o gatilho de registro na coluna {}:".format(old_col1))
			selected_itens_col1 = select_ops(old_col1_values, 2)
			print("Selecione os valores que deverão ser checados para disparar o gatilho de registro na coluna {}:".format(old_col2))
			selected_itens_col2 = select_ops(old_col2_values, 2)
			print("Selecione os valores que deverão ser checados para disparar o gatilho de registro na coluna {}:".format(old_col3))
			selected_itens_col3 = select_ops(old_col3_values, 2)
			print("Selecione os valores que deverão ser checados para disparar o gatilho de registro na coluna {}:".format(old_col4))
			selected_itens_col4 = select_ops(old_col4_values, 2)		

			print("Defina o nome da nova coluna:")
			print("Cuidado! Se o nome definido for igual a un nome anteriormente existente, as informações anteriores dessa coluna serão sobrescritas:\n")
			new_col_name = input("$: ")

			print("Defina o valor que deverá ser registrado na nova coluna quando os valores selecionados forem encontrados: \n")
			new_value = input("$: ")
		else:
			selected_itens_col1 = script_descriptor['valores_de_checagem'][list_of_old_cols[0]]
			selected_itens_col2 = script_descriptor['valores_de_checagem'][list_of_old_cols[1]]
			selected_itens_col3 = script_descriptor['valores_de_checagem'][list_of_old_cols[2]]
			selected_itens_col4 = script_descriptor['valores_de_checagem'][list_of_old_cols[3]]			
			new_col_name = script_descriptor['nome_da_nova_coluna']
			new_value = script_descriptor['valor_se_checagem_verdadeira']

		for line in list_of_dicts:
			if line.get(new_col_name) == None:
				line[new_col_name] = ""
			if (line[old_col1] in selected_itens_col1) and (line[old_col2] in selected_itens_col2) and (line[old_col3] in selected_itens_col3) and (line[old_col4] in selected_itens_col4):
				line[new_col_name] = new_value
	return list_of_dicts


def create_new_value_col_from_script(script_instructions, input_file_info):

	'''
	output = input_file_info

	for line in output:
		line['CALOURO_SELECIONADO'] = ''
		if (line['P_EST'] == line['P_ING']) and (line['AES_GRUPO'] == 'Perfil'):
			line['CALOURO_SELECIONADO'] = 1
	
	return output

	'''
	tasks = script_instructions['analises']

	output = input_file_info

	for task in tasks:
		colunas_selecionadas = []
		for c in task['valores_de_checagem'].keys():
			colunas_selecionadas.append(c)
			output = create_new_value_col_if_old_has_value(output, colunas_selecionadas, interactive=False, script_descriptor=task)
	
	return output


def convert_list_to_cli_args(lista):
    o = '" "'.join(lista)
    o = '"' + o + '"'
    return o


def mk_randnum_seq(num):
	output = ''
	while num != 0:
		idx = randrange(len(digits))
		output += digits[idx]
		num -= 1
	return output


def vermelho(string):
	return "{}{}{}".format(fg(1), string, attr(0))


def azul_claro(string):
	return "{}{}{}".format(fg(12), string, attr(0))


def verde(string):
	return "{}{}{}".format(fg(2), string, attr(0))


def amarelo(string):
	return "{}{}{}".format(fg(3), string, attr(0))


def rosa(string):
	return "{}{}{}".format(fg(5), string, attr(0))



def saida_verde(rotulo, valor, referencia='', escalonamento=[]):
	if referencia != '':
		if escalonamento != []:
			partes = '('
			n = len(escalonamento)
			l_step = 0
			while l_step != n:
				if l_step == n-1:
					partes += str(escalonamento[l_step])
					partes += ')'
				else:
					partes += str(escalonamento[l_step])
					partes += '/'
				l_step += 1
			return str(verde(rotulo) + ' ({})'.format(referencia) +": {} ".format(valor) + partes)
		else:
			return str(verde(rotulo) + ' ({})'.format(referencia) +": {} ".format(valor))
	else:
		return str(verde('{}'.format(rotulo)) +": {} ".format(valor))




def saida_vermelha(rotulo, valor, referencia='', escalonamento=[]):
	if referencia != '':
		if escalonamento != []:
			partes = '('
			n = len(escalonamento)
			l_step = 0
			while l_step != n:
				if l_step == n-1:
					partes += str(escalonamento[l_step])
					partes += ')'
				else:
					partes += str(escalonamento[l_step])
					partes += '/'
				l_step += 1
			return str(vermelho(rotulo) + ' ({})'.format(referencia) +": {} ".format(valor) + partes)
		else:
			return str(vermelho(rotulo) + ' ({})'.format(referencia) +": {} ".format(valor))
	else:
		return str(vermelho('{}'.format(rotulo)) +": {} ".format(valor))




def saida_rosa(rotulo, valor, referencia='', escalonamento=[]):
	if referencia != '':
		if escalonamento != []:
			partes = '('
			n = len(escalonamento)
			l_step = 0
			while l_step != n:
				if l_step == n-1:
					partes += str(escalonamento[l_step])
					partes += ')'
				else:
					partes += str(escalonamento[l_step])
					partes += '/'
				l_step += 1
			return str(rosa(rotulo) + ' ({})'.format(referencia) +": {} ".format(valor) + partes)
		else:
			return str(rosa(rotulo) + ' ({})'.format(referencia) +": {} ".format(valor))
	else:
		return str(rosa('{}'.format(rotulo)) +": {} ".format(valor))
		


def limpar_tela(msg=None):
	os.system("clear")
	if msg != None:
		print(msg)



def render_cols(lista, n, idx=True):
	larguras = []
	for i in lista:
		larguras.append(len(i))
	largura_max = max(larguras) + 5

	line = ''
	num_of_cols = n
	for i in lista:
		if idx == True:
			if num_of_cols != 0:
				line += '{}: {}'.format(str(lista.index(i)), i).ljust(largura_max)
		elif idx == False:
			if num_of_cols != 0:
				line += '{}'.format(i).ljust(largura_max)
		else:
			print("Argumento idx deve ser Boleano...")
			raise TypeError
		num_of_cols -= 1
		if num_of_cols == 0:
			line += os.linesep
			num_of_cols = n
	print(line)

		

def gerar_console_menu(lista, cols=1):
	'''
	gerar_console_menu(lista) -> lista de opções para seleção via console.

	Esta função é invocada por 'select_op'...
	'''
	o = ''
	n = 0

	if type(lista) == list:
		o = ''
		for i in lista:
			o += str(n) + ': ' + i + os.linesep
			n += 1
		if cols == 1:
			print(o)
		else:
			render_cols(lista, cols)
		return lista
	else:
		print("O argumento precisa ser do tipo lista...")
		raise TypeError



def input_num(nome, default=0):
	'''
	input_num(nome, default=0) -> gera um campo input que so aceita números.
	
	O campo de descrição "nome" aceita apenas valores inteiros. Valores não inteiros implicam loop. Valor "" implica valor default...
	'''
	
	entry = False
	while entry != True:
		try:
			num = input('{} [{}]: '.format(verde(nome), verde(default)))
			if num == '':
				num = int(default)
				break
			num = int(num)
			break
		except:
			print(vermelho('Resultado precisa ser numérico...'))
			entry = False
	return num



def input_op(lista_de_opcoes_validas):
	while True:
		op = input(amarelo('$: '))
		if not op in lista_de_opcoes_validas:
			print(vermelho("Opção inválida! Selecione entre [{}].".format("|".join(lista_de_opcoes_validas))))
		else:
			return op



def select_op(lista_de_selecao, col_num, sort_list=False):
	'''
	select_op(lista_de_selecao, col_num, sort_list=False) -> toma os valores de uma lista como opções enumeradas. O valor numérico inserido implica o retorno do item da lista correspondente.
	
	O campo "col_num" indica a quantidade de colunas a ser apresentada. Em definindo "sort_list" como True a lista original será reorganizada.
	'''
	
	if sort_list == True:
		lista_de_selecao.sort()
	op_list = gerar_console_menu(lista_de_selecao, col_num)
	op = None
	#while check_item_list(op,range(0,len(op_list))) != True:
	while not op in range(0,len(op_list)):
		try:
			op = int(input(amarelo('$: ')))
		except:
			print(vermelho('Resultado precisa ser numérico...'))
	return op_list[op]



def select_ops(lista_de_selecao, col_num, sort_list=False):
	'''
	select_ops(lista_de_selecao, col_num, sort_list=False) -> similar à "select_op", mas aceita mais de uma resposta.
	
	O campo "col_num" indica a quantidade de colunas a ser apresentada. Em definindo "sort_list" como True a lista original será reorganizada.
	'''
	if sort_list == True:
		lista_de_selecao.sort()
	op_list = gerar_console_menu(lista_de_selecao, col_num)
	while True:
		op = interval_select(input(amarelo('$: ')))
		try:
			selecao = []
			for i in op:
				selecao.append(op_list[int(i)])
			break
		except IndexError:
			print('Opção inválida...')
	return selecao


def interval_select(selection_string):
	selection_list = selection_string.replace(" ","").split(",")
	output = []
	for item in selection_list:
		try:
			if item.find('-') != -1:
				first_interval_item = int(item.split('-')[0])
				last_interval_item = int(item.split('-')[1])
				for n in range(first_interval_item, last_interval_item+1):
					output.append(n)
			else:
				output.append(int(item))
		except AttributeError:
			pass
	output.sort()
	return output


def render_form_get_values(form_file, skip_q=[]):
	'''
	Renderiza as questões de um formulário JSON conforme a estrutura abaixo.
	Retorna um dicionário com as respostas.
	As chaves são definidas conforme o atributo 'id'.
	Os valores são resultado do input dos usuários.

	{
		"titulo": "Registro de atendimento",
		"descricao": "Intrumental para registro de atendimentos no âmbito do SPS/FUP",
		"questoes":
		[
			{
				"enunciado": "Matrícula",
				"id": "identificador",
				"tipo": "text",
			},
			{
				"enunciado": "Tipo de atendimento",
				"id": "atd_t",
				"tipo": "radio",
				"alternativas" :
				[
					"Informação presencial",
					"Informação via telefone",
					...
				]            
			}
		]
	}	
	'''

	def objective_question_handler(q):
		rewrite_form = False
		grupos_de_opcao = []
		grupos_de_alternativas = []

		print(verde(q['enunciado']))
		if q['tipo'] == 'radio':
			if type(q['alternativas']) == list:
				nfo[q['id']] = select_op(q['alternativas'], 1)
			else:
				print("Campos do tipo 'radio' devem ter suas alternativas organizadas em lista...")
				print("Favor corrigir o arquivo de formulário...")
				exit()

		elif q['tipo'] == 'checkbox':
			if type(q['alternativas']) == list:
				nfo[q['id']] = "; ".join(select_ops(q['alternativas'], 1))
			
			elif type(q['alternativas']) == dict:
				for a in q['alternativas'].keys():
					grupos_de_alternativas.append(a)
				grupos_de_alternativas.sort()
				gopt = select_ops(grupos_de_alternativas, 1)
				alternativas_efetivas = []
				for grp_op_key in gopt:
					grupos_de_opcao.append(grp_op_key)
					for op in q['alternativas'][grp_op_key]:
						if not op in alternativas_efetivas:
							alternativas_efetivas.append(op)
				alternativas_efetivas.sort()
				alternativas_efetivas.append("Outro")
				nfo[q['id']] = select_ops(alternativas_efetivas, 1)

		if type(q['alternativas']) == list:
			if nfo[q['id']].find('Outro') != -1:
				nfo[q['id']] = nfo[q['id']].split('; ')
				nfo[q['id']].remove('Outro')
				outros_recem_listados = []
				while True:
					outro_detalhes = input('Especifique: ')
					outros_recem_listados.append(outro_detalhes)
					q['alternativas'].remove('Outro')
					q['alternativas'].append(outro_detalhes)
					q['alternativas'].sort()
					q['alternativas'].append('Outro')
					print("")
					print(verde("Adicionar outra opção? [s|n]"))
					op = input_op(['s','n'])
					if op == 'n':
						break
				
				nfo[q['id']] = merge_lists(nfo[q['id']], outros_recem_listados)
				if len(nfo[q['id']]) > 1:
					nfo[q['id']] = '; '.join(nfo[q['id']])
				else:
					nfo[q['id']] = nfo[q['id']][0]

				rewrite_form = True
		
		elif type(q['alternativas']) == dict:
			nfo_q_id = "; ".join(nfo[q['id']])
			if nfo_q_id.find('Outro') != -1:
				outros_recem_listados = []
				while True:
					print(verde('À qual grupo a obção divergente pertence: '))
					grp_op_key_field = select_op(grupos_de_alternativas, 1)
					outro_detalhes = input(verde('\nEspecifique a opção divergente: '))
					outros_recem_listados.append(outro_detalhes)
					q['alternativas'][grp_op_key_field].append(outro_detalhes)
					q['alternativas'][grp_op_key_field].sort()
					print("")
					print(verde("Adicionar outra opção? [s|n]"))
					op = input_op(['s','n'])
					if op == 'n':
						break
				
				if len(outros_recem_listados) > 1:
					outros_recem_listados = "; ".join(outros_recem_listados)
				else:
					outros_recem_listados = outros_recem_listados[0]

				nfo[q['id']] = nfo_q_id.replace('Outro', outros_recem_listados)
				rewrite_form = True
		
		if rewrite_form == True:
			save_json(form, form_file)

		print("")
		return (nfo[q['id']], rewrite_form)

	def create_trigger_file(form_trigger_file):
		form_triggers_info = {}
		form_triggers_info['arquivo_de_registro'] = form['arquivo_de_registro']
		form_triggers_info['q_groups'] = {}
		form_triggers_info['index_list'] = []
		for q in form['questoes']:
			form_triggers_info['index_list'].append(q['id'])
			if q.get('trigger_skip'):
				form_triggers_info[q['id']] = {}
				form_triggers_info[q['id']]['trigger_skip'] = {}
				condicoes_in_form = q['trigger_skip'].split('; ')
				condicoes_in_trigger_file = {}
				for c in condicoes_in_form:
					csplit = c.split('::')
					if condicoes_in_trigger_file.get(csplit[0]):
						condicoes_in_trigger_file[csplit[0]].append(csplit[1])
					else:
						condicoes_in_trigger_file[csplit[0]] = [csplit[1]]
				form_triggers_info[q['id']]['trigger_skip'] = condicoes_in_trigger_file
			
			if q.get('q_group'):
				if form_triggers_info['q_groups'].get(q['q_group']):
					form_triggers_info['q_groups'][q['q_group']].append(q['id'])
				else:
					form_triggers_info['q_groups'][q['q_group']] = [q['id']]
			else:
				if form_triggers_info['q_groups'].get('undefined_q_group'):
					form_triggers_info['q_groups']['undefined_q_group'].append(q['id'])
				else:
					form_triggers_info['q_groups']['undefined_q_group'] = [q['id']]


		save_json(form_triggers_info, form_triggers_file)
		return form_triggers_info

	
	def prompt_questions(nfo, q):
		skip_this = False
		#print(q['id'])
		if form_triggers_info.get(q['id']):
			if form_triggers_info[q['id']].get('trigger_skip'):
				for t in form_triggers_info[q['id']]['trigger_skip'].keys():
					print("» "+t)
					try:
						if nfo[t] in form_triggers_info[q['id']]['trigger_skip'].get(t):
							skip_this = True
							if q.get('autofill'):
								nfo[q['id']] = q['autofill']
							break
					except KeyError:
						skip_this = True
						if q.get('autofill'):
							nfo[q['id']] = q['autofill']
						break



		if not skip_this:
			if q['id'] in skip_q:
				pass

			elif q['tipo'] == 'text':
				nfo[q['id']] = input("{}: ".format(verde(q['enunciado'])))
				print("")

			elif q['tipo'] == 'radio' or q['tipo'] == 'checkbox':
				try:
					q_response = objective_question_handler(q)
					nfo[q['id']] = q_response[0]
				except TypeError:
					pass
		else:
			if q.get('skip_to'):
				return q['skip_to']

		return nfo



	form = load_json(form_file)
	form_triggers_file = getoutput('echo $HOME')+'/.form_triggers'
	form_triggers_info = create_trigger_file(form_triggers_file)

	
	nfo = {}
	grp_nfo = {}
	grp_nfo_tag = ""
	grp_tag = ""
	max_idx = len(form['questoes'])-1
	idx = 0
	grp_prompt_pass = False
	clean_up_keys = []

	while idx <= max_idx:
		q = form['questoes'][idx]
		first_idx = False
		last_idx = False
		if q.get('q_group'):
			inside_q_group = True
			grp_tag=q['q_group']
			clean_up_keys.append(q['id'])
			first = form_triggers_info['q_groups'][q['q_group']][0]
			last = form_triggers_info['q_groups'][q['q_group']][-1]
			first_idx = form_triggers_info['index_list'].index(first)
			last_idx = form_triggers_info['index_list'].index(last)
		else:
			inside_q_group = False
		
		if (idx == first_idx) and inside_q_group == True:
			if grp_prompt_pass == False:
				print(verde("Inserir registro para ")+amarelo(q['q_group'])+verde("?"))
				resposta = select_op(["Sim", "Não"], 1)
				print("")
				if resposta == 'Não':
					idx = last_idx+1
					try:
						q = form['questoes'][idx]
					except IndexError:
						break

		grp_prompt_pass = False

		response = prompt_questions(nfo, q)

		if (type(response) == str) and response[0] == ':':
			idx = int(response[1:])
	
		elif inside_q_group == True:
			if idx == first_idx:
				grp_nfo_tag = response[q['id']]
				grp_nfo[grp_nfo_tag] = OrderedDict()
			else:
				try:
					grp_nfo[grp_nfo_tag][q['id']] = response[q['id']]
				except KeyError:
					pass
		else:
			nfo = response
			
		if (idx == last_idx) and (inside_q_group == True):
			print(verde("Inserir registro adicional para ")+amarelo(q['q_group'])+verde("?"))
			resposta = select_op(["Sim", "Não"], 1)
			if resposta == 'Sim':
				idx = first_idx-1
				grp_prompt_pass = True
			else:
				nfo[grp_tag] = grp_nfo
				grp_nfo = OrderedDict()
				grp_tag = ""

		idx += 1

		if idx > max_idx:
			output = OrderedDict()
			for k in sorted(nfo.keys()):
				output[k] = nfo[k]
			for k in set(clean_up_keys):
				del(output[k])
			break
		

	
	os.remove(form_triggers_file)
	return output

	
def lexical_list_join(lista):
    output = ""
    for item in lista:
        output += item
        if item == lista[-1]:
            pass
        elif item == lista[-2]:
            output += ' e '
        else:
            output += ', '
    return output


def return_obj_from_dict(dictionary):
    class Obj:
        pass
    obj = Obj()

    for k, v in dictionary.items():
        setattr(obj, k, v)
    
    return obj