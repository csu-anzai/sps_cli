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

from collections import OrderedDict
from .cli_sps_base import timestamp

from .cli_global_paths import \
    pasta_raiz_do_aplicativo,\
    pasta_de_dados,\
    pasta_de_seguranca,\
    pasta_de_fragmentos,\
    pasta_de_indice,\
    pasta_de_formularios,\
    pasta_do_usuario,\
    arquivo_atendimentos,\
    arquivo_usuarios,\
    arquivo_profissionais,\
    arquivo_processos,\
    arquivo_corrigidos,\
    arquivo_index,\
    arquivo_estudos
    
from .py_functions_json import load_json, save_json


def get_col_width(field_name, dict_array):
    width = 0
    for line in dict_array:
        if len(line[field_name]) > width:
            width = len(line[field_name])
    return (field_name, width+2)

def get_itens(field_name, field_value,  dict_array):
    r = []
    for array_item in dict_array:
        if array_item[field_name] == field_value:
            r.append(array_item)
    return r

def get_col_values(field_name, dict_array):
    r = []
    for array_item in dict_array:
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

loop2 = asyncio.get_event_loop()
col_width = loop2.run_until_complete(asyncio.gather(
    get_col_width_nfo('identificador', dados_usuarios),
    get_col_width_nfo('nome', dados_usuarios),
    get_col_width_nfo('eml', dados_usuarios),
    get_col_width_nfo('uid', dados_profissionais),
    get_col_width_nfo('nome', dados_profissionais),
    get_col_width_nfo('eml', dados_profissionais),
    get_col_width_nfo('numero_sei', dados_processos),
    get_col_width_nfo('assunto', dados_processos),
    get_col_width_nfo('motivo', dados_processos),
))

#Larguras das colunas nas listas. Rodar método async aqui...
col_width_info = OrderedDict()
col_width_info['identificador'] = col_width[0]
col_width_info['nome_usuario'] = col_width[1]
col_width_info['eml_usuario'] = col_width[2]
col_width_info['uid'] = col_width[3]
col_width_info['nome_profissional'] = col_width[4]
col_width_info['eml_profissional'] = col_width[5]
col_width_info['numero_sei'] = col_width[6]
col_width_info['assunto'] = col_width[7]
col_width_info['motivo'] = col_width[8]
col_width_info['timestamp'] = ('timestamp', len(timestamp()) + 2)

col_width_etd_mat = col_width[0]
col_width_atend_ident = col_width_etd_mat
col_width_etd_nome = col_width[1]
col_width_etd_eml = col_width[2]
col_width_atend_time = ('timestamp', len(timestamp()) + 2)
col_width_prof_uid = col_width[3]
col_width_prof_nome = col_width[4]
col_width_prof_eml = col_width[5]
col_width_proc_sei_n = col_width[6]
col_width_proc_assunto = col_width[7]
col_width_proc_motivo = col_width[8]

