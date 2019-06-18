#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os
from subprocess import getoutput

envio_automatico_email=True
periodo_corrente="1º/2019"
pasta_do_usuario = getoutput("echo $HOME")
hostname = getoutput("hostname")
username = getoutput("whoami")

trabalhar_com_fragmentos = True
formato_lista_fragmentos = "emitidos-{}@{}.json".format(username, hostname)

if hostname == "oracleVM":
    pasta_raiz_do_aplicativo = "/home/bwb0de/Devel/sps_fup2"
elif hostname == "debian":
    pasta_raiz_do_aplicativo = "/home/danielc/Documentos/Devel/GitHub/sps_fup2"
elif hostname == "localhost":
    pasta_raiz_do_aplicativo = "/data/data/com.termux/files/home/sps_fup2"

pasta_de_dados = os.sep.join([pasta_raiz_do_aplicativo, "dados"])
pasta_de_seguranca = os.sep.join([pasta_raiz_do_aplicativo, "seguranca"])
pasta_de_fragmentos = os.sep.join([pasta_de_dados, "fragmentos"])
pasta_de_indice = os.sep.join([pasta_de_dados, "indexados"])
pasta_de_formularios = os.sep.join([pasta_raiz_do_aplicativo, "formularios"])

arquivo_atendimentos = os.sep.join([pasta_de_dados, "atendimentos.json"])
arquivo_usuarios = os.sep.join([pasta_de_dados, "usuarios.json"])
arquivo_profissionais = os.sep.join([pasta_de_dados, "profissionais.json"])
arquivo_processos = os.sep.join([pasta_de_dados, "processos.json"])
arquivo_corrigidos = os.sep.join([pasta_de_dados, "corrigidos.json"])
arquivo_index = os.sep.join([pasta_de_indice, "index_db.json"])
arquivo_estudos = os.sep.join([pasta_de_dados, "estudos.json"])
arquivo_usuario_alvo = os.sep.join([pasta_do_usuario, '.current_target'])

formulario_atendimentos = os.sep.join([pasta_de_formularios, "form_atendimento.json"])
formulario_novo_usuario = os.sep.join([pasta_de_formularios, "form_novo_usuario.json"])
formulario_novo_processo = os.sep.join([pasta_de_formularios, "form_processos.json"])
formulario_registro_de_correcao = os.sep.join([pasta_de_formularios, "form_corrigidos.json"])