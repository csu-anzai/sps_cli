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


import os
from string import whitespace, punctuation, digits
from .cli_tools import select_ops
from collections import OrderedDict
from copy import copy
from time import ctime, sleep


def show_each_dictArray_block(dict_array, print_fields, index_pos):
	'''
	Apresenta bloco de informações de um 'dict_array'.
	Apenas os campos definidos em 'print_fields' serão retornados.
	A cada impressão o programa aquarda pelo comando para prosseguir.
	Elementos iniciais da lista podem ser ignorados definindo-se o local de inicio 'index_pos'.
	'''
	for i in dict_array[index_pos:]:
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
	Realiza a comparação entre dois dicionários retornando o que mudou no segundo [b] em relação ao primeiro[a].
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

def create_new_value_col_from_old(dict_array, old_col):
	pass

def create_new_value_col_from_cross_old(dict_array, list_of_old_cols, interactive=True, script_descriptor=None):
	num_of_cols = len(list_of_old_cols)

	if (interactive == False) and (script_descriptor == None):
		if type(script_descriptor) != dict:
			print("Descritor não apresentado ou em formato inadequado...")
			exit()

	if num_of_cols == 1:

		old_col1 = list_of_old_cols[0]
		old_col1_values = []
		for line in dict_array:
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

		for line in dict_array:
			if line.get(new_col_name) == None:
				line[new_col_name] = ""
			if line[old_col1] in selected:
				line[new_col_name] = new_value
	
	elif num_of_cols == 2:
	
		old_col1 = list_of_old_cols[0]
		old_col2 = list_of_old_cols[1]
		old_col1_values = []
		old_col2_values = []
	
		for line in dict_array:
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

		for line in dict_array:
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

			for line in dict_array:
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
		work = ""
		for line in dict_array:
			count += 1

			if line.get(new_col_name) == None:
				line[new_col_name] = ""
			#if (line[old_col1] == selected_itens_col1) and (line[old_col2] == selected_itens_col2) and (line[old_col3] == selected_itens_col3):
#			if line[old_col1] in selected_itens_col1:
#				if line[old_col2] in selected_itens_col2:
#					if line[old_col3] in selected_itens_col3:

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
			else:
				work += "Sem correspondência na linha: {} » {}\n".format(count, line["NOME_ESTUDANTE"])
				work += str("  · "+ old_col1+ " »» {} in {} ".format(line[old_col1], selected_itens_col1) + '\n')
				work += str("  · "+ old_col2+ " »» {} in {} ".format(line[old_col2], selected_itens_col2) + '\n')
				work += str("  · "+ old_col3+ " »» {} in {} ".format(line[old_col3], selected_itens_col3) + '\n\n')


		f=open('work','w')
		f.write(work)
		f.close()

		return dict_array

	elif num_of_cols == 4:

		old_col1 = list_of_old_cols[0]
		old_col2 = list_of_old_cols[1]
		old_col3 = list_of_old_cols[2]
		old_col4 = list_of_old_cols[4]
		old_col1_values = []
		old_col2_values = []
		old_col3_values = []
		old_col4_values = []

		for line in dict_array:
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

		for line in dict_array:
			if line.get(new_col_name) == None:
				line[new_col_name] = ""
			if (line[old_col1] in selected_itens_col1) and (line[old_col2] in selected_itens_col2) and (line[old_col3] in selected_itens_col3) and (line[old_col4] in selected_itens_col4):
				line[new_col_name] = new_value
	return dict_array

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
			output = create_new_value_col_from_cross_old(output, colunas_selecionadas, interactive=False, script_descriptor=task)
	
	return output