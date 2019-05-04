#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time
import os

from py_console_tools_v0 import load_json, listar_dicionario

def get_col_width(field_name, dict_array):
    width = 0
    for line in dict_array:
        if len(line[field_name]) > width:
            width = len(line[field_name])
    return (field_name, width+2)

def get_mat(dados_estudantes):
    matriculas = []
    for estudantes in dados_estudantes:
        matriculas.append(estudantes['mat'])
    return matriculas

def save_target_info(mat):
    for e in dados_estudantes:
        if e['mat'] == mat:
            save_json(e, './.current_target')

def timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S %a", time.localtime())


import asyncio

async def test():
    print("Acabou!")
    return 1

async def test2():
    os.system("ls; sleep 5; ls")


loop = asyncio.get_event_loop()
loop.run_until_complete(asyncio.gather(
    test2(),
    test(),
))



#Quando os comandos estiverem disponíveis globalmente, utilizar caminhos absolutos.
data_folder = "./data"
form_folder = "./forms"

arquivo_atendimentos = os.sep.join([data_folder, "atendimentos.json"])
arquivo_estudantes = os.sep.join([data_folder, "estudantes.json"])
arquivo_profissionais = os.sep.join([data_folder, "profissionais.json"])
arquivo_processos = os.sep.join([data_folder, "processos.json"])
arquivo_corrigidos = os.sep.join([data_folder, "corrigidos.json"])

form_atendiento = os.sep.join([form_folder, "form_atendimento.json"])
form_novo_estudante = os.sep.join([form_folder, "form_novo_estudante.json"])
form_estudo_socioeconomico = os.sep.join([form_folder, "form_estudo_socioeconomico.json"])
form_processos = os.sep.join([form_folder, "form_processos.json"])
form_corrigidos = os.sep.join([form_folder, "form_corrigidos.json"])

dados_atendimentos = load_json(arquivo_atendimentos)
dados_estudantes = load_json(arquivo_estudantes)
dados_profissionais = load_json(arquivo_profissionais)
dados_processos = load_json(arquivo_processos)
dados_corrigidos = load_json(arquivo_corrigidos)


#Larguras das colunas nas listas.
col_width_etd_mat = get_col_width('mat', dados_estudantes)
col_width_atend_ident = col_width_etd_mat
col_width_etd_nome = get_col_width('nome', dados_estudantes)
col_width_etd_eml = get_col_width('eml', dados_estudantes)
col_width_atend_time = ('timestamp', len(timestamp()) + 2)
col_width_prof_uid = get_col_width('uid', dados_profissionais)
col_width_prof_nome = get_col_width('nome', dados_profissionais)
col_width_prof_eml = get_col_width('eml', dados_profissionais)

