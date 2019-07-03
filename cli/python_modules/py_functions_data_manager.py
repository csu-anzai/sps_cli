#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
#  py_functions_data_manager
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
import json

from string import whitespace, punctuation, digits
from .py_functions_csv import read_csv
from .cli_tools import limpar_tela, select_op, select_ops, verde, input_op
from .py_euristic_tools import merge_lists
from .py_functions_json import load_json, save_json
from collections import OrderedDict
from copy import copy
from time import ctime, sleep

def convert_csv2json(csv_file):
    csv_file_name = csv_file.split('.')[0]
    csv_file_data = read_csv(csv_file)
    save_json(csv_file_data, "./{}.json".format(csv_file_name))



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
			nfo[q['id']] = input("{}: ".format(verde(q['enunciado'])))
			print("")

		elif q['tipo'] == 'radio':
			print(verde(q['enunciado']))
			nfo[q['id']] = select_op(q['alternativas'], 1)
			if nfo[q['id']].find('Outro') != -1:
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
				
				if len(outros_recem_listados) > 1:
					outros_recem_listados = "; ".join(outros_recem_listados)
				else:
					outros_recem_listados = outros_recem_listados[0]

				nfo[q['id']] = nfo[q['id']].replace('Outro', outros_recem_listados)
				rewrite_form = True

			print("")

				
		elif q['tipo'] == 'checkbox':
			print(verde(q['enunciado']))
			nfo[q['id']] = "; ".join(select_ops(q['alternativas'], 1))
			if nfo[q['id']].find('Outro') != -1:
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
				
				if len(outros_recem_listados) > 1:
					outros_recem_listados = "; ".join(outros_recem_listados)
				else:
					outros_recem_listados = outros_recem_listados[0]

				nfo[q['id']] = nfo[q['id']].replace('Outro', outros_recem_listados)
				rewrite_form = True

			print("")
				
	if rewrite_form == True:
		save_json(form, form_file)

	return nfo

def listagem_cli(linhas_selecionadas, cols):
	visual_nfo = ""
	visual_count = len(linhas_selecionadas)
	for linha in linhas_selecionadas:
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


