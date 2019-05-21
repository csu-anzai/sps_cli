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
import json #Remover depois
from colored import fg, bg, attr
#from py_euristic_tools import check_item_list

from subprocess import getoutput
from random import randrange
from string import digits

def mk_randstr(num):
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
	try: cmd = os.system("clear")
	except: cmd = os.system("cls")
	if msg != None:
		print(msg)




def render_cols(lista, n, idx=True):
	larguras = []
	for i in lista:
		larguras.append(len(i))
	largura_max = max(larguras) + 5

	o = []
	l = []
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
			op = int(input('$: '))
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
		op = input('$: ').replace(' ','').split(',')
		try:
			selecao = []
			for i in op:
				selecao.append(op_list[int(i)])
			break
		except IndexError:
			print('Opção inválida...')
	return selecao

##As funções abaixo devarão ser realocadas...

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


def save_json(novos_dados, path_to_file):
	lockf = lockfile_name(path_to_file)
	initfolder = os.getcwd()
	nfo = path_to_file.split('/')
	fname = nfo[-1]
	path = path_to_file.replace(fname, '')

	while True:
		if os.path.isfile(lockf):
			time.sleep(0.1)
		else:
			create_lockfile(lockf)
			break

	os.chdir(path.replace('/', os.sep))
	with open(path_to_file, 'w') as f:
		f.write(json.dumps(novos_dados, ensure_ascii=False, indent=4))		

	os.chdir(initfolder)
	remove_lockfile(lockf)
