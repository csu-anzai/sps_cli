#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from .cli_machine_info import username
from .cli_global_paths import arquivo_usuario_alvo
from .cli_tools import verde, vermelho, select_op
from .cli_db_loader import get_col_values, dados_usuarios
from .py_functions_json import save_json
from string import punctuation

matriculas = get_col_values('identificador', dados_usuarios)

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

def save_target_info(identificador, dict_array):
    for array_item in dict_array:
        if array_item['identificador'] == identificador:
            save_json(array_item, arquivo_usuario_alvo)

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


