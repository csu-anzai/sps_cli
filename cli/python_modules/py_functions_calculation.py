#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
#  Copyright 2017 Daniel Cruz <bwb0de@bwb0dePC>
#  Estatística Version 0.1
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


from math import fsum as soma
import re



def media_aritmetica(l):
	'''Calcula a média aritmética a partir de uma lista numérica de entrada.'''
	return float(soma(l)/len(l))



def desvios(l):
	x = media_aritmetica(l)
	d = []
	for i in l:
		d.append(i-x)
	return d



def variancia(l):
	y = len(l)-1
	d = desvios(l)
	v = []
	for i in d:
		v.append(i**2)
	smqd = soma(v)
	return smqd/y



def desvio_padrao(l):
	return variancia(l)**0.5



def dispersao(l):
	y = len(l) #n
	d = desvios(l)
	dvp = desvio_padrao(l)
	r = {1: 0, 2: 0, 3: 0}
	for i in d:
		if i < 0: i = i * (-1)
		if i/dvp >= 1:
			if i/dvp < 3: r[2] = r[2] + 1
			else: r[3] = r[3] + 1
		else: r[1] = r[1] + 1
	rr1 = r[1]/y
	rr1 = rr1*100
	rr2 = r[2]/y
	rr2 = rr2*100
	rr3 = r[3]/y
	rr3 = rr3*100
	return {1: rr1, 2: rr2, 3: rr3}


def verifica_tipo_da_chave(chave):
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


def procura_segmentada(elemento, lista, idx=0): #Bisection procura_segmentada
	print(lista)
	if len(lista) == 1:
		if elemento == lista[0]:
			return idx
		else:
			return False
	slice_init = 0
	slice_end = len(lista)
	mid = slice_end // 2
	if lista[mid] == elemento:
		return idx+mid
	elif elemento > lista[mid]:
		slice_init = mid+1
		idx += slice_init
		return procura_segmentada(elemento, lista[slice_init:slice_end], idx)
	elif elemento < lista[mid]:
		slice_end = mid-1
		return procura_segmentada(elemento, lista[slice_init:slice_end], slice_end)


def frequencia_absoluta(l): #rever método confore py_csv
	o = {}
	for i in l:
		o[i] = 0
	for i in l:
		o[i] = o[i] + 1
	return o




def frequencia_relativa(l): #rever método confore py_csv
	ab = frequencia_absoluta(l)
	n = len(l)
	o = {}
	for i in ab.keys():
		o[i] = ((ab[i])/n)*100
	return o



def dispersao_i(v, l):
	dis = dispersao(l)
	dvp = desvio_padrao(l)
	c = v-media_aritmetica(l)
	if c < 0: c = c * (-1)
	if c/dvp >= 1:
		if c/dvp < 3: return dis[2]
		else: return dis[3]
	else: return dis[1]
