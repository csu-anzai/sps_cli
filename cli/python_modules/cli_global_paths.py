#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import os

from .cli_machine_info import pasta_do_usuario, hostname, username, pasta_raiz_do_aplicativo

pasta_de_dados = os.sep.join([pasta_raiz_do_aplicativo, "dados"])
pasta_de_configuracao = os.sep.join([pasta_raiz_do_aplicativo, "cli/config"])
pasta_de_seguranca = os.sep.join([pasta_raiz_do_aplicativo, "cli/seguranca"])
pasta_de_fragmentos = os.sep.join([pasta_de_dados, "fragmentos"])
pasta_de_indice = os.sep.join([pasta_de_dados, "indexados"])
pasta_de_formularios = os.sep.join([pasta_raiz_do_aplicativo, "cli/formularios"])

arquivo_atendimentos = os.sep.join([pasta_de_dados, "atendimentos.json"])
arquivo_usuarios = os.sep.join([pasta_de_dados, "usuarios.json"])
arquivo_profissionais = os.sep.join([pasta_de_dados, "profissionais.json"])
arquivo_processos = os.sep.join([pasta_de_dados, "processos.json"])
arquivo_corrigidos = os.sep.join([pasta_de_dados, "corrigidos.json"])
arquivo_index = os.sep.join([pasta_de_indice, "index_db.json"])
arquivo_estudos = os.sep.join([pasta_de_dados, "estudos.json"])
arquivo_de_configuracao = os.sep.join([pasta_de_configuracao, "opcoes.json"])
arquivo_usuario_alvo = os.sep.join([pasta_do_usuario, '.current_target'])

formulario_atendimentos = os.sep.join([pasta_de_formularios, "form_atendimento.json"])
formulario_novo_usuario = os.sep.join([pasta_de_formularios, "form_novo_usuario.json"])
formulario_novo_processo = os.sep.join([pasta_de_formularios, "form_processos.json"])
formulario_registro_de_correcao = os.sep.join([pasta_de_formularios, "form_corrigidos.json"])
formulario_estudo_estudante = os.sep.join([pasta_de_formularios, "form_estudo_socioeconomico_estudante.json"])
formulario_estudo_grupo_familiar = os.sep.join([pasta_de_formularios, "form_estudo_socioeconomico_grupo-familiar-info.json"])
formulario_estudo_membros_grupo_familiar = os.sep.join([pasta_de_formularios, "form_estudo_socioeconomico_membros-grupo-familiar.json"])