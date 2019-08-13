#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
#  Copyright 2017 Daniel Cruz <bwb0de@bwb0dePC>
#  CLI Base configfile
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

import os
import asyncio
import time

from tempfile import gettempdir
from string import punctuation
from collections import OrderedDict
from subprocess import getoutput

from .cli_tools import verde, vermelho, select_op
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
        if line.get(field_name):
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


def get_nfo(identificador, set_de_dados, index_de_dados):
    for s in index_de_dados:
        if s['set_de_dados'] == set_de_dados:
            return s['dados'].get(identificador)


def get_info_doc(arquivo_de_dados, coluna, valor_de_checagem):
    for doc in arquivo_de_dados:
        if doc[coluna] == valor_de_checagem:
            return doc


def show_nfo_frag(identificador, set_de_dados, arquivo_de_dados, index_de_dados, print_info=True):
    ret_nfo = get_nfo(identificador, set_de_dados, index_de_dados)
    if ret_nfo:
        for i in ret_nfo:
            if print_info:
                print(arquivo_de_dados[i])
            return arquivo_de_dados[i]

def show_nfo_frag_by_nome(identificador, arquivo_de_dados, index_de_dados):
    identificador_init = identificador[0]
    set_de_nomes = {}
    for sets in index_de_dados:
        if sets['set_de_dados'] == 'nome':
            set_de_nomes = sets['dados']
    try:
        entries = set_de_nomes.get(identificador_init).get(identificador)
        num_entries = len(entries)
    except:
        entries = []
        num_entries = 0
    
    if num_entries > 1:
        nomes_op = []
        for idx in entries:
            nomes_op.append(arquivo_de_dados[idx]['nome'])
        print(verde("Mais de um estudante possui registro do nome solicitado em seu nome completo, selecione o estudante correto:"))
        op = select_op(nomes_op, 1)
        op_idx = entries[nomes_op.index(op)]
        return arquivo_de_dados[op_idx]['identificador']
    
    elif num_entries == 0:
        print(vermelho("Registro não encontrado..."))
    
    else:
        return arquivo_de_dados[entries[0]]['identificador']

def save_target_info(identificador, list_of_dicts):
    for array_item in list_of_dicts:
        if array_item['identificador'] == identificador:
            save_json(array_item, arquivo_usuario_alvo)

def numero_sei_mascara(num):
    m_num = num
    for char in punctuation:
        m_num = m_num.replace(char,'')
    return str(m_num[0:5]+'.'+m_num[5:11]+'/'+m_num[11:15]+'-'+m_num[15:])

def numero_identificador_mascara(num):
    #Define user ID format here
    m_num = num
    for char in punctuation:
        m_num = m_num.replace(char,'')
    return str(m_num[0:2]+'/'+m_num[2:])


async def load_json_file(arquivo):
    return load_json(arquivo)

async def get_col_width_nfo(field_name, data_set):
    return get_col_width(field_name, data_set)

async def get_col_label(formulario):
    id_and_label = {}
    for i in formulario['questoes']:
        id_and_label[i['id']] = i['enunciado']
    return id_and_label


#Machine and system user info
hostname = getoutput("hostname")
username = getoutput("whoami")


#Read info from /etc/cli/cli_tools.conf
pasta_do_usuario = getoutput("echo $HOME")
pasta_temporaria = gettempdir()
pasta_raiz_do_aplicativo = getoutput("cli-config read RAIZ")
pasta_de_seguranca = getoutput("cli-config read PASTA_DE_SEGURANCA")
pasta_de_dados = getoutput("cli-config read PASTA_DE_DADOS")
device = getoutput("cli-config read DEVICE_TYPE")
envio_automatico_email = bool(getoutput("cli-config read ENVIO_AUTOMATICO_EMAIL"))
trabalhar_com_fragmentos = bool(getoutput("cli-config read ENVIO_DE_FRAGMENTOS"))
rclone_drive=getoutput("cli-config read RCLONE")

if device == "Termux":
    pasta_temporaria = getoutput("echo $TMPDIR")


#Setting global paths to cli base folders and files
pasta_de_fragmentos = os.sep.join([pasta_de_dados, "fragmentos"])
pasta_de_indice = os.sep.join([pasta_de_dados, "indexados"])
pasta_de_formularios = os.sep.join([pasta_raiz_do_aplicativo, "cli/formularios"])

arquivo_fragmentos_emitidos = os.sep.join([pasta_de_fragmentos, "emitidos.json"])
arquivo_fragmentos_recebidos = os.sep.join([pasta_de_fragmentos, "recebidos.json"])
arquivo_atendimentos = os.sep.join([pasta_de_dados, "atendimentos.json"])
arquivo_usuarios = os.sep.join([pasta_de_dados, "usuarios.json"])
arquivo_profissionais = os.sep.join([pasta_de_dados, "profissionais.json"])
arquivo_processos = os.sep.join([pasta_de_dados, "processos.json"])
arquivo_corrigidos = os.sep.join([pasta_de_dados, "corrigidos.json"])
arquivo_index = os.sep.join([pasta_de_indice, "index_db.json"])
arquivo_col_wid = os.sep.join([pasta_de_indice, "col_wid.json"])
arquivo_sex_info = os.sep.join([pasta_de_indice, "sex_info.json"])
arquivo_estudos = os.sep.join([pasta_de_dados, "estudos.json"])
arquivo_usuario_alvo = os.sep.join([pasta_do_usuario, '.current_target'])
arquivo_modelo_ppaes = os.sep.join([pasta_raiz_do_aplicativo, "cli/modelos/ppaes.odt"])
arquivo_modelo_ppaes_detalhado = os.sep.join([pasta_raiz_do_aplicativo, "cli/modelos/ppaes_det.odt"])
arquivo_modelo_ccc = os.sep.join([pasta_raiz_do_aplicativo, "cli/modelos/criacao-cc.odt"])

lista_pase = os.sep.join([pasta_de_dados, "lista_pase.json"])
lista_moradia = os.sep.join([pasta_de_dados, "lista_moradia.json"])
lista_creche = os.sep.join([pasta_de_dados, "lista_creche.json"])
lista_transporte = os.sep.join([pasta_de_dados, "lista_transporte.json"])

formulario_atendimentos = os.sep.join([pasta_de_formularios, "form_atendimento.json"])
formulario_novo_usuario = os.sep.join([pasta_de_formularios, "form_novo_usuario.json"])
formulario_novo_processo = os.sep.join([pasta_de_formularios, "form_processos.json"])
formulario_registro_de_correcao = os.sep.join([pasta_de_formularios, "form_corrigidos.json"])
formulario_estudo_estudante = os.sep.join([pasta_de_formularios, "form_estudo_socioeconomico.json"])


#Carregando arquivos de dados
loop = asyncio.get_event_loop()
dados = loop.run_until_complete(asyncio.gather(
    load_json_file(arquivo_atendimentos),
    load_json_file(arquivo_usuarios),
    load_json_file(arquivo_profissionais),
    load_json_file(arquivo_processos),
    load_json_file(arquivo_corrigidos),
    load_json_file(arquivo_index),
    load_json_file(arquivo_estudos),
    load_json_file(lista_pase),
    load_json_file(lista_moradia),
    load_json_file(lista_transporte),
    load_json_file(lista_creche)                
))

dados_atendimentos = dados[0]
dados_usuarios = dados[1]
dados_profissionais = dados[2]
dados_processos = dados[3]
dados_processos_pend = get_itens('resultado', '', dados_processos)
dados_corrigidos = dados[4]
dados_index = dados[5]
dados_estudos = dados[6]
dados_lista_pase = dados[7]
dados_lista_moradia = dados[8]
dados_lista_transporte = dados[9]
dados_lista_creche = dados[10]

col_wid_test = int(getoutput("if [ -f {} ]; then echo 1; else echo 0; fi".format(arquivo_col_wid)))

if col_wid_test == 1:
    col_wid = load_json(arquivo_col_wid)
else:
    calculate_col_width()



#Custom configurations - SPS
matriculas = get_col_values('identificador', dados_usuarios)

periodo_corrente = "2º/2019"
formato_lista_fragmentos = "emitidos-{}@{}.json".format(username, hostname)

etiquetas = {}
etiquetas['identificador'] = "Identificador"
etiquetas['nome_usuario'] = "Nome"
etiquetas['eml_usuario'] = "e-Mail"
etiquetas['uid'] = "ID de Login"
etiquetas['nome_profissional'] = "Nome do Profissional"
etiquetas['eml_profissional'] = "e-Mail"
etiquetas['numero_sei'] = "Número do processo"
etiquetas['assunto'] = "Assunto"
etiquetas['motivo'] = "Motivo"
etiquetas['timestamp'] = "Data e hora"



