#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import getoutput
from .cli_machine_info import hostname, username
from .cli_global_paths import arquivo_de_configuracao

from .py_functions_json import load_json

periodo_corrente = "1º/2019"
envio_automatico_email = bool(getoutput("cli-config read ENVIO_AUTOMATICO_EMAIL"))
trabalhar_com_fragmentos = bool(getoutput("cli-config read ENVIO_DE_FRAGMENTOS"))
formato_lista_fragmentos = "emitidos-{}@{}.json".format(username, hostname)

