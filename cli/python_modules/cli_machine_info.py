#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import getoutput

hostname = getoutput("hostname")
username = getoutput("whoami")

pasta_do_usuario = getoutput("echo $HOME")
pasta_temporaria=getoutput("cli-config read PASTA_TEMPORARIA")
pasta_raiz_do_aplicativo = getoutput("cli-config read RAIZ")
pasta_de_seguranca = getoutput("cli-config read PASTA_DE_SEGURANCA")
pasta_de_dados = getoutput("cli-config read PASTA_DE_DADOS")

if hostname == "oracleVM":
    pasta_raiz_do_aplicativo = "/home/bwb0de/Devel/sps_cli"

elif hostname == "debian":
    pasta_raiz_do_aplicativo = "/home/danielc/Documentos/Devel/GitHub/sps_fup2"

elif hostname == "localhost":
    pasta_temporaria = getoutput("echo $TMPDIR")
    pasta_raiz_do_aplicativo = "/data/data/com.termux/files/home/sps_cli"

elif hostname == "spsfup":
    pasta_raiz_do_aplicativo = "/srv/sps_fup2"

