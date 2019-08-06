#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
#  Copyright 2019 Daniel Cruz <bwb0de@bwb0dePC>
#  CLI-DB-Loader Version 0.1
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
import asyncio
import time

from collections import OrderedDict
from subprocess import getoutput

from .cli_tools import load_json, save_json


def timestamp(mode=None):
    if mode == "mkid":
        from subprocess import getoutput
        return time.strftime("{}%Y%m%d%H%M%S".format(username[0:3].upper()), time.localtime())
    elif mode == "long":
        mes_corrente = time.strftime("%m", time.localtime())

        mes = {}
        mes['01'] = 'janeiro'
        mes['02'] = 'fevereiro'
        mes['03'] = 'março'
        mes['04'] = 'abril'
        mes['05'] = 'maio'
        mes['06'] = 'junho'
        mes['07'] = 'julho'
        mes['08'] = 'agosto'
        mes['09'] = 'setembro'
        mes['10'] = 'outubro'
        mes['11'] = 'novembro'
        mes['12'] = 'dezembro'

        nome_mes = mes[mes_corrente]
        
        return time.strftime("%d de "+nome_mes+" de %Y", time.localtime())
    else:
        return time.strftime("%Y-%m-%d %H:%M:%S %a", time.localtime())

def get_col_width(field_name, list_of_dicts):
    width = 0
    for line in list_of_dicts:
        if len(line[field_name]) > width:
            width = len(line[field_name])
    return (field_name, width+2)

def get_itens(field_name, field_value,  list_of_dicts):
    r = []
    for array_item in list_of_dicts:
        if array_item[field_name] == field_value:
            r.append(array_item)
    return r

def get_col_values(field_name, list_of_dicts):
    r = []
    for array_item in list_of_dicts:
        r.append(array_item[field_name])
    return r

def get_tags(dados_usuarios):
    marcadores = []
    for estudante in dados_usuarios:
        if estudante.get("marcador"):
            for m in estudante['marcador']:
                if m not in marcadores:
                    marcadores.append(m)
    marcadores.sort()
    return marcadores

def get_tags_idx(dados_usuarios):
    marcadores_idx = {}
    for estudante in dados_usuarios:
        if estudante.get("marcador"):
            for m in estudante['marcador']:
                if marcadores_idx.get(m) == None:
                    marcadores_idx[m] = [dados_usuarios.index(estudante)]
                else:
                    marcadores_idx[m].append(dados_usuarios.index(estudante))
    return marcadores_idx

async def load_json_file(arquivo):
    return load_json(arquivo)

async def get_col_width_nfo(field_name, data_set):
    return get_col_width(field_name, data_set)

async def get_col_label(formulario):
    id_and_label = {}
    for i in formulario['questoes']:
        id_and_label[i['id']] = i['enunciado']
    return id_and_label

def calculate_col_width():
    loop2 = asyncio.get_event_loop()
    col_width = loop2.run_until_complete(asyncio.gather(
        get_col_width_nfo('identificador', dados_usuarios),
        get_col_width_nfo('nome', dados_usuarios),
        get_col_width_nfo('eml', dados_usuarios),
        get_col_width_nfo('uid', dados_profissionais),
        get_col_width_nfo('prof_nome', dados_profissionais),
        get_col_width_nfo('prof_eml', dados_profissionais),
        get_col_width_nfo('numero_sei', dados_processos),
        get_col_width_nfo('assunto', dados_processos),
        get_col_width_nfo('motivo', dados_processos),
    ))

    #Larguras das colunas nas listas. Rodar método async aqui...
    col_wid = OrderedDict()
    col_wid['identificador'] = col_width[0]
    col_wid['nome_usuario'] = col_width[1]
    col_wid['eml_usuario'] = col_width[2]
    col_wid['uid'] = col_width[3]
    col_wid['nome_profissional'] = col_width[4]
    col_wid['eml_profissional'] = col_width[5]
    col_wid['numero_sei'] = col_width[6]
    col_wid['assunto'] = col_width[7]
    col_wid['motivo'] = col_width[8]
    col_wid['timestamp'] = ('timestamp', len(timestamp()) + 2)

    save_json(col_wid, arquivo_col_wid)    


loop = asyncio.get_event_loop()
dados = loop.run_until_complete(asyncio.gather(
    load_json_file(arquivo_atendimentos),
    load_json_file(arquivo_usuarios),
    load_json_file(arquivo_profissionais),
    load_json_file(arquivo_processos),
    load_json_file(arquivo_corrigidos),
    load_json_file(arquivo_index),
    load_json_file(arquivo_estudos)
))

dados_atendimentos = dados[0]
dados_usuarios = dados[1]
dados_profissionais = dados[2]
dados_processos = dados[3]
dados_processos_pend = get_itens('resultado', '', dados_processos)
dados_corrigidos = dados[4]
dados_index = dados[5]
dados_estudos = dados[6]

col_wid_test = int(getoutput("if [ -f {} ]; then echo 1; else echo 0; fi".format(arquivo_col_wid)))

if col_wid_test == 1:
    col_wid = load_json(arquivo_col_wid)
else:
    calculate_col_width()

