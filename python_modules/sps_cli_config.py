#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import getoutput

automail=True
periodo_corrente="1º/2019"
user_home_folder = getoutput("echo $HOME")

hostname = getoutput("hostname")
if hostname == "oracleVM":
    app_root_folder = "/home/bwb0de/Devel/sps_fup2"
elif hostname == "debian":
    app_root_folder = "/home/danielc/Documentos/Devel/GitHub/sps_fup2"
elif hostname == "localhost":
    app_root_folder = "/data/data/com.termux/files/home/sps_fup2"

