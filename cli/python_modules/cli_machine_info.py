#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import getoutput

pasta_do_usuario = getoutput("echo $HOME")
hostname = getoutput("hostname")
username = getoutput("whoami")

tmpdir='/tmp'

if hostname == "oracleVM":
    pasta_raiz_do_aplicativo = "/home/bwb0de/Devel/sps_cli"

elif hostname == "debian":
    pasta_raiz_do_aplicativo = "/home/danielc/Documentos/Devel/GitHub/sps_fup2"

elif hostname == "localhost":
    tmpdir = getoutput("echo $TMPDIR")
    pasta_raiz_do_aplicativo = "/data/data/com.termux/files/home/sps_fup2"

elif hostname == "spsfup":
    pasta_raiz_do_aplicativo = "/srv/sps_fup2"

#Incluir checagen de dependências
'''
python3
rclone
zip
ccrypt
nano
nodejs
git
pandoc
wkhtmltopdf
'''