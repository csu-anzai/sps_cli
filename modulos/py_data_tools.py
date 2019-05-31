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
import re
import pickle

from string import whitespace, punctuation, digits
from .py_json_handlers import load_json, save_json
from .py_csv_app import read_csv
from .py_console_tools import limpar_tela, select_op, select_ops
from .py_euristic_tools import merge_lists
from collections import OrderedDict
from copy import copy
from time import ctime, sleep

def convert_csv2json(csv_file):
    csv_file_name = csv_file.split('.')[0]
    csv_file_data = read_csv(csv_file)
    save_json(csv_file_data, "./{}.json".format(csv_file_name))

def create_lockfile(lockf):
	f = open("/tmp/"+lockf,'w')
	f.close()

def remove_lockfile(lockf):
	os.remove("/tmp/"+lockf)


def lockfile_name(path_to_file):
	lkf_name = path_to_file.split(os.sep)[-1]
	if lkf_name.find(".") != -1 or lkf_name.find(".") != 0:
		lkf_name = lkf_name.split(".")[0]
	file_name = '~lock_'+str(lkf_name)
	return file_name


def show_each_dictArray_block(dict_array, print_fields, index_pos):
	'''
	Apresenta bloco de informações de um 'dict_array'.
	Apenas os campos definidos em 'print_fields' serão retornados.
	A cada impressão o programa aquarda pelo comando para prosseguir.
	Elementos iniciais da lista podem ser ignorados definindo-se o local de inicio 'index_pos'.
	'''
	for i in dict_array[index_pos:]:
		limpar_tela()
		print_nfo = ""
		for f in print_fields:
			print_nfo += i[f].replace('/','') + os.linesep
		print(print_nfo)
		input("Pressione enter para continuar...")



def join_dictArray_intersection(dict_array1, dict_array2, joint_key):
	'''
	Realiza a junção de dois dicionários distintos que compartilhem uma mesma chave/col.
	Retorna as linhas em que os valores da chave selecionada correspondem nos dois dicionários.
	'''
	output = []
	tmpdict = {}
	for row in dict_array1:
		tmpdict[row[joint_key]] = row
	dict_array2_cols = dict_array2[0].keys()
	for other_row in dict_array2:
		if other_row[joint_key] in tmpdict: #tmpdict.has_key(other_row[col]):
			joined_row = tmpdict[other_row[joint_key]]
			for colz in dict_array2_cols:
				if colz != joint_key:
					joined_row[colz] = other_row[colz]
			output.append(joined_row)
	return output



def join_dictArray_union(dict_array1, dict_array2, joint_key):
	'''
	Realiza a junção de dois dicionários distintos que compartilhem uma mesma chave/col.
	Retorna as linhas em que os valores da chave selecionada correspondem nos dois dicionários.'''
	output = []
	tmpdict = {}
	dict_array1_cols = dict_array1[0].keys()
	dict_array2_cols = dict_array2[0].keys()
	for row in dict_array1:
		tmpdict[row[joint_key]] = row
	new_row_col = merge_lists(dict_array1_cols,dict_array2_cols)
	new_row_skell = OrderedDict()
	for col_name in new_row_col:
		new_row_skell[col_name]=""
	
	key_2_skip = []
	for other_row in dict_array2:
		if other_row[joint_key] in tmpdict:
			key_2_skip.append(other_row[joint_key])
			joined_row = tmpdict[other_row[joint_key]]
			for colz in dict_array2_cols:
				if colz != joint_key:
					joined_row[colz] = other_row[colz]
			output.append(joined_row)
		
	linhas_n_comuns = len(dict_array1) + len(dict_array1) - len(key_2_skip)
	tabela_linhas_n_comuns = []
	while linhas_n_comuns != 0:
		linha_inteira = copy(new_row_skell)
		tabela_linhas_n_comuns.append(linha_inteira)
		linhas_n_comuns -= 1
	
	tabela_linhas_n_comuns=[]
	
	for linha in dict_array1:
		linha_inteira = copy(new_row_skell)
		if not linha[joint_key] in key_2_skip:
			for colz in dict_array1_cols:
				try: linha_inteira[colz] = linha[colz]
				except: pass
			tabela_linhas_n_comuns.append(linha_inteira)

	for linha in dict_array2:
		linha_inteira = copy(new_row_skell)
		if not linha[joint_key] in key_2_skip:
			for colz in dict_array2_cols:
					linha_inteira[colz] = linha[colz]
			tabela_linhas_n_comuns.append(linha_inteira)
		
	final_output = merge_lists(tabela_linhas_n_comuns, output)
	return final_output



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
	form = load_json(form_file)
	exec_cmd = ""
	rewrite_form = False
	nfo = {}
	for q in form['questoes']:
		print_response = False

		if q['id'] in skip_q:
			pass

		elif q['tipo'] == 'text':
			nfo[q['id']] = input("{}: ".format(q['enunciado']))

		elif q['tipo'] == 'radio':
			print(q['enunciado'])
			nfo[q['id']] = select_op(q['alternativas'], 1)
			if nfo[q['id']].find('Outro') != -1:
				outro_detalhes = input('Especifique: ')
				nfo[q['id']] = nfo[q['id']].replace('Outro', outro_detalhes)
				q['alternativas'].remove('Outro')
				q['alternativas'].append(outro_detalhes)
				q['alternativas'].sort()
				q['alternativas'].append('Outro')
				rewrite_form = True

				
		elif q['tipo'] == 'checkbox':
			print(q['enunciado'])
			nfo[q['id']] = "; ".join(select_ops(q['alternativas'], 1))
			if nfo[q['id']].find('Outro') != -1:
				outro_detalhes = input('Especifique: ')
				nfo[q['id']] = nfo[q['id']].replace('Outro', outro_detalhes)
				q['alternativas'].remove('Outro')
				q['alternativas'].append(outro_detalhes)
				q['alternativas'].sort()
				q['alternativas'].append('Outro')
				rewrite_form = True
				
	if rewrite_form == True:
		save_json(form, form_file)

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
		else:
			visual_count += 1
		if select_this == True:
			w = 0
			li = ""
			linha_sem_quebra = True
			for col in cols:
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
			
			if linha_sem_quebra == True:
				visual_nfo += li + os.linesep

	visual_nfo += "Total: {}".format(visual_count)
	return visual_nfo


def obter_frq_abs_from_dictArray(dict_array, key=False):
	'''
	Retorna os diferentes valores existentes na chave 'key' para o 'dict_array'.
	Retorna o valor absoluto das ocorrencias de valores.
	'''
	fields = dict_array[0].keys()
	if key != False:
		selected_cols = [key]
	else:
		selected_cols = select_ops(fields, 2)
	o = OrderedDict()
	for f in selected_cols:
		query_list = []
		for line in dict_array:
			query_list.append(line[f])
		query_list_entries = set(query_list)
		for itens in query_list_entries:
			o[itens]=query_list.count(itens)
	return o




def obter_frq_abs_e_rel_from_dictArray(dict_array, key=False):
	n = len(dict_array)
	r = obter_frq_abs_from_dictArray(dict_array, key)
	o = OrderedDict()
	for k in r.keys():
		o[k] = (r[k], float((r[k]/n)*100.00))
	return o


def make_complete_stat_from_dictArray(dict_array, printout=True):
	fields = dict_array[0].keys
	o = OrderedDict()
	for field in fields:
		colcount = obter_frq_abs_e_rel_from_dictArray(dict_array, field)
		o[field] = colcount
	
	for k in o.keys():
		print("Variável: "+k)
		for v in o[k].keys():
			print("  » "+v, o[k][v])
		print("=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-=-="+os.linesep)



def map_values_in_dictArray_col(dict_array):
	'''
	Retorna os diferentes valores existentes na coluna 'col' para a 'tabela' do mysql selecionada.
	'''
	output = obter_frq_abs_from_dictArray(dict_array)
	output = output.keys()
	return output


