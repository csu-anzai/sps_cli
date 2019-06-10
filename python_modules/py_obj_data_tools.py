
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

import re


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


	

