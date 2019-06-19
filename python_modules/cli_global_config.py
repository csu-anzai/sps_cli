#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import getoutput

envio_automatico_email=True
periodo_corrente="1º/2019"
pasta_do_usuario = getoutput("echo $HOME")
hostname = getoutput("hostname")
username = getoutput("whoami")

trabalhar_com_fragmentos = True
formato_lista_fragmentos = "emitidos-{}@{}.json".format(username, hostname)
tmpdir='/tmp'

if hostname == "oracleVM":
    pasta_raiz_do_aplicativo = "/home/bwb0de/Devel/sps_fup2"
elif hostname == "debian":
    pasta_raiz_do_aplicativo = "/home/danielc/Documentos/Devel/GitHub/sps_fup2"
elif hostname == "localhost":
    tmpdir = getoutput("echo $TMPDIR")
    pasta_raiz_do_aplicativo = "/data/data/com.termux/files/home/sps_fup2"

