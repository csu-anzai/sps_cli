#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import time

from .cli_global_config import username
from .cli_global_paths import arquivo_usuario_alvo
from .py_functions_json import save_json
from string import punctuation


def save_target_info(identificador, dict_array):
    for array_item in dict_array:
        if array_item['identificador'] == identificador:
            save_json(array_item, arquivo_usuario_alvo)

def timestamp(mode=None):
    if mode == "mkid":
        from subprocess import getoutput
        return time.strftime("{}%Y%m%d%H%M%S".format(username[0:3].upper()), time.localtime())
    else:
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


