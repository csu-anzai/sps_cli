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

import time
import os

from tempfile import gettempdir
from string import punctuation
from subprocess import getoutput

from .cli_tools import verde, vermelho, select_op
from .cli_db_loader import get_col_values, dados_usuarios
from .py_functions_json import save_json

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

formulario_atendimentos = os.sep.join([pasta_de_formularios, "form_atendimento.json"])
formulario_novo_usuario = os.sep.join([pasta_de_formularios, "form_novo_usuario.json"])
formulario_novo_processo = os.sep.join([pasta_de_formularios, "form_processos.json"])
formulario_registro_de_correcao = os.sep.join([pasta_de_formularios, "form_corrigidos.json"])
formulario_estudo_estudante = os.sep.join([pasta_de_formularios, "form_estudo_socioeconomico_estudante.json"])
formulario_estudo_grupo_familiar = os.sep.join([pasta_de_formularios, "form_estudo_socioeconomico_grupo-familiar-info.json"])
formulario_estudo_membros_grupo_familiar = os.sep.join([pasta_de_formularios, "form_estudo_socioeconomico_membros-grupo-familiar.json"])


#Custom configurations - SPS
matriculas = get_col_values('identificador', dados_usuarios)

periodo_corrente = "1º/2019"
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




def get_nfo(identificador, set_de_dados, index_de_dados):
    for s in index_de_dados:
        if s['set_de_dados'] == set_de_dados:
            return s['dados'].get(identificador)


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
