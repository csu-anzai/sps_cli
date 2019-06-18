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

from colored import fg, bg, attr
from subprocess import getoutput
from random import randrange
from string import digits

def convert_to_cli_args(lista):
    o = '" "'.join(lista)
    o = '"' + o + '"'
    return o


def create_lockfile(lockf):
	tmpdir = getoutput('echo $TMPDIR')
	f = open(tmpdir+os.sep+lockf,'w')
	f.close()

def remove_lockfile(lockf):
	tmpdir = getoutput('echo $TMPDIR')
	os.remove(tmpdir+os.sep+lockf)


def lockfile_name(path_to_file):
	lkf_name = path_to_file.split(os.sep)[-1]
	if lkf_name.find(".") != -1 or lkf_name.find(".") != 0:
		lkf_name = lkf_name.split(".")[0]
	file_name = '~lock_'+str(lkf_name)
	return file_name

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
		op = input(amarelo('$: ')).replace(' ','').split(',')
		try:
			selecao = []
			for i in op:
				selecao.append(op_list[int(i)])
			break
		except IndexError:
			print('Opção inválida...')
	return selecao

