#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  py_data_tools
#  Copyright 2018 Daniel Cruz <danielc@debian>
#  Version 0.1
#
#  Descrição:
#  * Este pacote possui uma série de funções para trabalhar com dados nos formatos 'csv', 'json' e 'pickle'.
#  * Permite a leitura, escrita e conversão de dados nesses formatos.
#  * Define, também, uma estrutura de dados MultiKeyDict que permite registro ordenados de dados e procura otimizada.
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
import csv
import re
import pickle
import json

from string import whitespace, punctuation, digits
from py_console_tools import limpar_tela, select_op, select_ops
from collections import OrderedDict
from copy import copy
from time import ctime, sleep


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
    initfolder = os.getcwd()
    nfo = path_to_file.split('/')
    fname = nfo[-1]
    path = path_to_file.replace(fname, '')
    os.chdir(path.replace('/', os.sep))
    f = open(fname, 'w')
    f.write(json.dumps(novos_dados, ensure_ascii=False, indent=4))
    f.close()
    os.chdir(initfolder)



def render_form_get_values(form, skip_q=[]):
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
				"id": "mat",
				"tipo": "text"
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
	nfo = {}
	for q in form['questoes']:
		#if check_item_list(q['id'], skip_q) == True:
		if q['id'] in skip_q:
			pass
		elif q['tipo'] == 'text':
			nfo[q['id']] = input("{}: ".format(q['enunciado']))
		elif q['tipo'] == 'radio':
			print(q['enunciado'])
			nfo[q['id']] = select_op(q['alternativas'], 1)
		elif q['tipo'] == 'checkbox':
			print(q['enunciado'])
			nfo[q['id']] = "; ".join(select_ops(q['alternativas'], 1))
	return nfo


def listar_dicionario(dicionario, cols, marcadores=[]):
	'''
	Lista o conteúdo de um dicionário retornando uma tabela/string com colunas solicitadas.
	O parametro 'cols' é uma lista de tuplas (t) em que t[0] é o 'id' e t[1] um número.
	O número de t[1] representa a largura a ser definida para coluna id ou t[0].
	Exibe ao final o total de elementos no dicionário.
	'''
	visual_nfo = ""
	visual_count = 0
	for linha in dicionario:
		select_this = True
		if marcadores != []:
			select_this = False
			try:
				for m in marcadores:
					if m in linha['marcador']:
						select_this = True
						visual_count += 1
			except KeyError:
				pass
		if select_this == True:
			for col in cols:
				visual_nfo += linha[col[0]].ljust(col[1])
			visual_nfo += os.linesep
	visual_nfo += "Total: {}".format(visual_count)
	return visual_nfo


def read_csv(csv_file, delimiter=',', lineterminator='\n'):
	'''Acessa o conteúdo do arquivo CSV e o armazena na memória.'''
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




def join_csv_intersection(csvfile1, csvfile2, col, output_file):
	'''Realiza a junção de dois dicionários distintos que compartilhem uma mesma chave/col. Retorna as linhas em que os valores da chave selecionada correspondem nos dois dicionários.'''
	output = []
	tmpdict = {}
	csvdata1 = read_csv(csvfile1)
	csvdata2 = read_csv(csvfile2)
	for row in csvdata1:
		tmpdict[row[col]] = row
	csvdata2_cols = csvdata2[0].keys()
	for other_row in csvdata2:
		if other_row[col] in tmpdict: #tmpdict.has_key(other_row[col]):
			joined_row = tmpdict[other_row[col]]
			for colz in csvdata2_cols:
				if colz != col:
					joined_row[colz] = other_row[colz]
			output.append(joined_row)
	write_csv(output, output_file)
	return output




def join_csv_union(csvfile1, csvfile2, col, output_file):
	'''Realiza a junção de dois dicionários distintos que compartilhem uma mesma chave/col. Retorna as linhas em que os valores da chave selecionada correspondem nos dois dicionários.'''
	output = []
	tmpdict = {}
	csvdata1 = read_csv(csvfile1)
	csvdata2 = read_csv(csvfile2)
	csvdata1_cols = csvdata1[0].keys()
	csvdata2_cols = csvdata2[0].keys()
	for row in csvdata1:
		tmpdict[row[col]] = row
	new_row_col = merge_lists(csvdata1_cols,csvdata2_cols)
	new_row_skell = OrderedDict()
	for col_name in new_row_col:
		new_row_skell[col_name]=""
	
	key_2_skip = []
	for other_row in csvdata2:
		if other_row[col] in tmpdict:
			key_2_skip.append(other_row[col])
			joined_row = tmpdict[other_row[col]]
			for colz in csvdata2_cols:
				if colz != col:
					joined_row[colz] = other_row[colz]
			output.append(joined_row)
		
	linhas_n_comuns = len(csvdata1) + len(csvdata1) - len(key_2_skip)
	tabela_linhas_n_comuns = []
	while linhas_n_comuns != 0:
		linha_inteira = copy(new_row_skell)
		tabela_linhas_n_comuns.append(linha_inteira)
		linhas_n_comuns -= 1
	
	tabela_linhas_n_comuns=[]
	
	for linha in csvdata1:
		linha_inteira = copy(new_row_skell)
		#if check_item_list(linha[col], key_2_skip) != True:
		if not linha[col] in key_2_skip:
			for colz in csvdata1_cols:
				try: linha_inteira[colz] = linha[colz]
				except: pass
			tabela_linhas_n_comuns.append(linha_inteira)

	for linha in csvdata2:
		linha_inteira = copy(new_row_skell)
		#if check_item_list(linha[col], key_2_skip) != True:
		if not linha[col] in key_2_skip:
			for colz in csvdata2_cols:
					linha_inteira[colz] = linha[colz]
			tabela_linhas_n_comuns.append(linha_inteira)
		
	final_output = merge_lists(tabela_linhas_n_comuns, output)
		
	write_csv(final_output, output_file)
	return output




def join_csv_overwrite(csvfile1, csvfile2, col, output_file):
	'''Gera um arquivo de saída com base no arquivo 2 em que as informações do arquivo 1 serão sobrescritas nas colunas de mesmo nome, no arquivo 2, onde os valores da célula referente à "col" coincidam'''
	
	return None




def compare_csv_col(csv_file1, csv_file2):
	""" """
	pass




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
	#limpar_tela()
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
						#limpar_tela()
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
							#limpar_tela()
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
			new_csv_file = ctime().replace(' ','_') + "_rmLines_from_" + csv_file
			write_csv(remove_that, new_csv_file)




def copy_col(csv_file, source_col, destination_col):
	"Copia o conteúdo de uma coluna alvo para uma coluna de destino se a célula do destino ainda não estiver preechida"
	conteudo = read_csv(csv_file)
	novo_conteudo = []
	cols = read_csv_head(csv_file)
	change_info = False
	#if check_item_list(destination_col, cols) == True:
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
	#limpar_tela()
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



def create_lockfile(lockf):
	f = open(lockf,'w')
	f.close()



def lockfile_name(csv_file):
	file_name = '~lock_'+str(csv_file).replace('.csv','')
	return file_name	


def convert_csv_type(csv_file, old_delimiter, new_delimiter, old_lineterminator=os.linesep, new_lineterminator=os.linesep):
	conteudo = read_csv(csv_file, delimiter=old_delimiter, lineterminator=old_lineterminator)
	write_csv(conteudo, csv_file, delimiter=new_delimiter, lineterminator=new_lineterminator)


def write_csv(csv_data_list, csv_file, header=None, delimiter=',', lineterminator='\n'):
	'''
	Escreve o conteudo de uma lista de dicionários, 'csv_data_list', em um arquivo CSV, 'csv_file'.
	Esta função gera um arquivo de trava até que o processo seja concluído.
	A ordem do cabeçalho pode ser definido arbitrariamente mediante a inclusão do argumento 'header'.
	'''
	
	lockf = lockfile_name(csv_file)
	
	if header == None:
		fields = csv_data_list[0].keys()
	else:
		fields = header
	
	while True:
		if os.path.isfile(lockf):
			sleep(0.7)
		else:
			create_lockfile(lockf)
			break
	
	with open(csv_file, 'w') as f:
		w = csv.DictWriter(f, fields, delimiter=delimiter, lineterminator=lineterminator)
		w.writeheader()
		w.writerows(csv_data_list)
		os.remove(lockf)
		




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




# def check_item_list(item, lista):
# 	try:
# 		lista.index(item)
# 		return True
# 	except:
# 		return False
		


def get_indexes(item, lista):
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
		if not i in b:
			o.append(i)
	return o




def compare_lists(a, b, historical_analisis=False, listA_NAME='First', listB_NAME='Second'):
	'''Compara duas listas e retorna um dicionário que agrupa itens exclusivos e compartilhados. Se o terceiro argumento for "True", apresenta uma única lista mostrando o que mudou de [b] em relação a [a]. Os argumentos 4 e 5 definem os nomes das listas de entrada.'''
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
	'''Realiza a comparação entre dois dicionários retornando, por padrão, o que mudou do segundo [b] em relação ao primeiro[a]. Se o terceiro argumento for "False", retorna um dicionário agrupando itens exclusivos e compartilhados dessas listas.'''
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
		if i in b:
			pass
		else:
			o.append(i)
	return o




def intersect_lists(a, b):
	'''Retorna a lista com itens comuns a partir de duas listas de entrada.'''
	o = []
	tl = merge_lists(a,b)
	for i in tl:
		if i in a and i in b:
			o.append(i)
	return o



def clean_digits(s):
	r = s
	for i in digits:
		r = r.replace(i,'')
	return r


def clean_string(s):
	''' Retira todos os sinais de pontuação e espaços em branco de uma string.'''
	r = s
	for i in whitespace+punctuation+"/":
		r = r.replace(i,"")
	return r



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


class MultiKeyDict():
	def __init__(self):
		self.delimitadores = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9', 'A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n', 'o', 'p', 'q', 'r', 's', 't', 'u', 'v', 'w', 'x', 'y', 'z']
		self.delimitadores_idx = {}
		for i in self.delimitadores:
			self.delimitadores_idx[i] = None
		self.delimitadores = ''.join(self.delimitadores)

		#Mantem as chaves em listas separadas
		self.lista_chaves_1 = []
		self.lista_chaves_2 = []
		self.lista_chaves_3 = []
		self.lista_chaves_4 = []
		self.lista_chaves_5 = []
		
		#Estabelece as etiquetas para as chaves
		self.etiqueta_chave_1 = 'Nome'
		self.etiqueta_chave_2 = 'e-Mail'
		self.etiqueta_chave_3 = 'Matrícula'
		self.etiqueta_chave_4 = 'CPF'
		self.etiqueta_chave_5 = 'Data de nascimento'

		self.etiqueta_chave_1_dica = ''
		self.etiqueta_chave_2_dica = '[formato: ????@????.????]'
		self.etiqueta_chave_3_dica = '[formato: ##/#######]'
		self.etiqueta_chave_4_dica = '[formato: ###.###.###-##]'
		self.etiqueta_chave_5_dica = '[formato: ##/##/####]'


		#Lista armazena os indices de referência para os respectivos valores em '__d'.
		self.referencias_chaves_1 = []
		self.referencias_chaves_2 = []
		self.referencias_chaves_3 = []
		self.referencias_chaves_4 = []
		self.referencias_chaves_5 = []
		
		#Valores
		self.dados = []

	def __repr__(self):
		output = 'MultiKeyDict('
		first_loop = True
		for i in range(0,len(self.lista_chaves_1)):
			if first_loop == False:
				output += ';; '
			output += '['
			if self.lista_chaves_1[i] != '':
				output += self.etiqueta_chave_1 + ": '" + self.lista_chaves_1[i] + "'"
			if self.lista_chaves_1[i] != '':
				output += '; ' + self.etiqueta_chave_2 + ": '" + self.lista_chaves_2[i] + "'"
			if self.lista_chaves_1[i] != '':
				output += '; ' + self.etiqueta_chave_3 + ": '" + self.lista_chaves_3[i] + "'"
			if self.lista_chaves_1[i] != '':
				output += '; ' + self.etiqueta_chave_4 + ": '" + self.lista_chaves_4[i] + "'"
			if self.lista_chaves_1[i] != '':
				output += '; ' + self.etiqueta_chave_5 + ": '" + self.lista_chaves_5[i] + "'"
			output += ']: ' + str(self.dados[i])
			first_loop = False
		output += ')'
		return output


	def verifica_tipo_da_chave(self, chave):
		line = chave.strip()
		if re.search(r"^\d\d\/\d\d\/\d\d\d\d", line) != None:
			return 'Data'
		elif re.search(r"^\w*\@\w*\.\w*", line) != None:
			return 'e-Mail'
		elif re.search(r"^\d{3}\.\d{3}\.\d{3}\-\d{2}", line) != None:
			return 'CPF'
		elif re.search(r"^\d\d\/\d\d\d*", line) != None:
			return 'Matrícula'
		else:
			return 'Nome'		
		

	def procura(self, chave):
		def procura_segmentada(elemento, lista, idx=None): #Bisection procura_segmentada
			if len(lista) == 0:
				return False
			elif len(lista) == 1:
				if elemento == lista[0]:
					return 0
				else:
					return False
			slice_init = 0
			slice_end = len(lista)
			mid = slice_end // 2
			if lista[mid] == elemento:
				return mid
			elif elemento > lista[mid]:
				slice_init = mid+1
				return procura_segmentada(elemento, lista[slice_init:slice_end], slice_init)
			elif elemento < lista[mid]:
				slice_end = mid
				return procura_segmentada(elemento, lista[slice_init:slice_end], slice_end)

		tipo_chave = self.verifica_tipo_da_chave(chave)
		
		if tipo_chave == 'Nome':
			return procura_segmentada(chave, self.lista_chaves_1)
		elif tipo_chave == 'e-Mail':
			return procura_segmentada(chave, self.lista_chaves_2)
		elif tipo_chave == 'Matrícula':
			return procura_segmentada(chave, self.lista_chaves_3)
		elif tipo_chave == 'CPF':			
			return procura_segmentada(chave, self.lista_chaves_4)
		elif tipo_chave == 'Data':
			return procura_segmentada(chave, self.lista_chaves_5)
		else:
			return False



	def inserir(self, v, chave1, chave2=None, chave3=None, chave4=None, chave5=None):
		#Adiciona registro de forma ordenada e não permite a inclusão de registros duplicados...
		trava_chave_1 = True
		trava_chave_2 = True
		trava_chave_3 = True
		trava_chave_4 = True
		trava_chave_5 = True
		
		if self.procura(chave1) == False:
			trava_chave_1 = False
		if self.procura(chave2) == False:
			trava_chave_2 = False
		if self.procura(chave3) == False:
			trava_chave_3 = False
		if self.procura(chave4) == False:
			trava_chave_4 = False
		if self.procura(chave5) == False:
			trava_chave_5 = False
		
		if trava_chave_1 and trava_chave_2 and trava_chave_3 and trava_chave_4 and trava_chave_5:
			print('Não foi possível inserir o conjunto de chaves -> valor. Estas chaves já estão no dicionário.')
		else:
			vidx = len(self.dados)
			self.adicionar_a_lista_ordenada(chave1, self.lista_chaves_1, self.referencias_chaves_1, vidx)
			self.adicionar_a_lista_ordenada(chave2, self.lista_chaves_2, self.referencias_chaves_2, vidx)
			self.adicionar_a_lista_ordenada(chave3, self.lista_chaves_3, self.referencias_chaves_3, vidx)
			self.adicionar_a_lista_ordenada(chave4, self.lista_chaves_4, self.referencias_chaves_4, vidx)
			self.adicionar_a_lista_ordenada(chave5, self.lista_chaves_5, self.referencias_chaves_5, vidx)
			self.dados.append(v)

	def remove(self, k):
		idx = self.verifica_tipo_da_chave(k)
		self.lista_chaves_1.remove(self.lista_chaves_1[idx])
		self.lista_chaves_2.remove(self.lista_chaves_2[idx])
		self.lista_chaves_3.remove(self.lista_chaves_3[idx])
		self.lista_chaves_4.remove(self.lista_chaves_4[idx])
		self.lista_chaves_5.remove(self.lista_chaves_5[idx])
		self.dados.remove(self.dados[idx])
		

	def get(self, k):
		print(self.dados[self.procura(k)])
		
		
	def adicionar_a_lista_ordenada(self, elemento, lista, lista_referencia, id_do_valor):
		assert type(elemento) == str, "Primeiro argumento (elemento) deve ser do tipo string..."
		assert type(lista) == list, "Segundo argumento deve ser do tipo lista..."

		#Obtém o caractere referente ao próximo grupos de palavras para estabelecer o intervalo
		next_grpchar = self.delimitadores.index(elemento[0])+1
		
		if self.delimitadores_idx[elemento[0]] != None:
			slice_init = self.delimitadores_idx[elemento[0]]
			init_slice_set = True
			skip_last_pump = True
		else:
			slice_init = 0
			self.delimitadores_idx[elemento[0]] = 0
			init_slice_set = False
			skip_last_pump = False
		
		if self.delimitadores_idx[self.delimitadores[next_grpchar]] != None:
			slice_end = self.delimitadores_idx[self.delimitadores[next_grpchar]]
			end_slice_set = True
		else:
			end_slice_set = False
		
		idxz_to_increment = self.delimitadores.split(elemento[0])[1]

		for c in idxz_to_increment:
			if self.delimitadores_idx[c] != None:
				self.delimitadores_idx[c] += 1

		#Executa este laço se exitir, de fato um intervalo ao qual o elemento pertença.
		if (init_slice_set == True) and (end_slice_set == True):
			for item_do_slice in lista[slice_init:slice_end]:
				if elemento > item_do_slice:
					if item_do_slice == lista[slice_init:slice_end][-1]:
						lista.insert(lista.index(item_do_slice)+1, elemento)
				else:
					lista.insert(lista.index(item_do_slice),elemento)
					lista_referencia.insert(lista.index(elemento), id_do_valor)
					return lista
		else:
			for item in lista:
				if elemento > item:
					pass
				else:
					lista.insert(lista.index(item),elemento)
					lista_referencia.insert(lista.index(elemento), id_do_valor)
					return lista
			#Se nenhuma das condições anteriores corresponderem, adiciona o item ao final da lista. 
			lista.append(elemento)
			lista_referencia.insert(lista.index(elemento), id_do_valor)
			if not skip_last_pump:
				self.delimitadores_idx[elemento[0]] = len(lista)-1
		return lista


	

