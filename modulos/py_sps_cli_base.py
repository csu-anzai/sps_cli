#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os
import asyncio

from .py_console_tools_v0 import load_json, listar_dicionario, save_json
from subprocess import getoutput
from string import punctuation

def get_col_width(field_name, dict_array):
    width = 0
    for line in dict_array:
        if len(line[field_name]) > width:
            width = len(line[field_name])
    return (field_name, width+2)

def get_mat(dados_usuarios):
    matriculas = []
    for estudantes in dados_usuarios:
        matriculas.append(estudantes['mat'])
    return matriculas

def get_procp(dados_processos):
    #Lista processos pendentes
    dados_processos_pend = []
    for proc in dados_processos:
        if proc['resultado'] == "":
            dados_processos_pend.append(proc)
    return dados_processos_pend


def get_tags(dados_usuarios):
    marcadores = []
    for estudante in dados_usuarios:
        if estudante.get("marcador"):
            for m in estudante['marcador']:
                if m not in marcadores:
                    marcadores.append(m)
    marcadores.sort()
    return marcadores

def save_target_info(mat):
    for e in dados_usuarios:
        if e['mat'] == mat:
            save_json(e, os.sep.join([user_home_folder, '.current_target']))

def timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S %a", time.localtime())

def numero_sei_mascara(num):
    m_num = num
    for char in punctuation:
        m_num = m_num.replace(char,'')
    return str(m_num[0:5]+'.'+m_num[5:11]+'/'+m_num[11:15]+'-'+m_num[15:])

def numero_identificador_mascara(num):
    #Defina aqui a máscara para o identificador conforme o público alvo da instituição
    m_num = num
    for char in punctuation:
        m_num = m_num.replace(char,'')
    return str(m_num[0:2]+'/'+m_num[2:])


async def load_json_file(arquivo):
    return load_json(arquivo)

async def get_col_width_nfo(field_name, data_set):
    return get_col_width(field_name, data_set)


automail=True

#Quando os comandos estiverem disponíveis globalmente, utilizar caminhos absolutos.
user_home_folder = getoutput("echo $HOME")
app_root_folder = "/home/danielc/Documentos/Devel/GitHub/sps_fup2"

data_folder = os.sep.join([app_root_folder, "dados"])
index_db_folder = os.sep.join([data_folder, "indexados"])
form_folder = os.sep.join([app_root_folder, "formularios"])

arquivo_atendimentos = os.sep.join([data_folder, "atendimentos.json"])
arquivo_usuarios = os.sep.join([data_folder, "usuarios.json"])
arquivo_profissionais = os.sep.join([data_folder, "profissionais.json"])
arquivo_processos = os.sep.join([data_folder, "processos.json"])
arquivo_corrigidos = os.sep.join([data_folder, "corrigidos.json"])
arquivo_index = os.sep.join([index_db_folder, "index_db.json"])

form_atendiento = os.sep.join([form_folder, "form_atendimento.json"])
form_novo_usuario = os.sep.join([form_folder, "form_novo_usuario.json"])
form_estudo_socioeconomico = os.sep.join([form_folder, "form_estudo_socioeconomico.json"])
form_processos = os.sep.join([form_folder, "form_processos.json"])
form_corrigidos = os.sep.join([form_folder, "form_corrigidos.json"])

loop = asyncio.get_event_loop()
dados = loop.run_until_complete(asyncio.gather(
    load_json_file(arquivo_atendimentos),
    load_json_file(arquivo_usuarios),
    load_json_file(arquivo_profissionais),
    load_json_file(arquivo_processos),
    load_json_file(arquivo_corrigidos),
))

dados_atendimentos = dados[0]
dados_usuarios = dados[1]
dados_profissionais = dados[2]
dados_processos = dados[3]
dados_processos_pend = get_procp(dados_processos)
dados_corrigidos = dados[4]

loop2 = asyncio.get_event_loop()
col_width = loop2.run_until_complete(asyncio.gather(
    get_col_width_nfo('mat', dados_usuarios),
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

