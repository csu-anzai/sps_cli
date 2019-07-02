#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import getoutput
from .cli_machine_info import hostname, username
from .cli_global_paths import arquivo_de_configuracao

from .py_functions_json import load_json

global_config = load_json(arquivo_de_configuracao)

periodo_corrente = "1º/2019"
envio_automatico_email = global_config[hostname]["envio_automatico_email"]
trabalhar_com_fragmentos = global_config[hostname]["trabalhar_com_fragmentos"]
formato_lista_fragmentos = "emitidos-{}@{}.json".format(username, hostname)
