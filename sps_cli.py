from py_console_tools_v0 import *
from py_json_handlers import *
from py_csv_app import read_csv
from sps_manual import *
from smtplib import SMTP
from string import whitespace, punctuation, digits

from email.message import EmailMessage

import time
import json
import getpass
import hashlib

def csv2json(csv_file):
    csv_file_name = csv_file.split('.')[0]
    csv_file_data = read_csv(csv_file)
    save_json(csv_file_data, "./{}.json".format(csv_file_name))

def insert_info(json_estudantes, print_fields, formulario_q_add, novo_nome_de_campo):
    #insert_info('Consultas_OldSAE.json', ['mat','Nome','Periodo','Data de Nascimento'], 'form_estudo_socioeconomico.json', 'Estudo Social e Economico')
    estudantes = load_json('./{}'.format(json_estudantes))
    novas_questoes = load_json('./forms/{}'.format(formulario_q_add))
    for e in estudantes:
        print(e)
        if e.get(novo_nome_de_campo) == None:
            limpar_tela()
            print_nfo = ""
            for f in print_fields:
                print_nfo += e[f] + os.linesep
            print(print_nfo)
            nfo = render_form_get_values(novas_questoes)
            e[novo_nome_de_campo] = nfo
            save_json(estudantes, './{}'.format(json_estudantes))

def load_json(path_to_file):
    initfolder = os.getcwd()
    nfo = path_to_file.split('/')
    fname = nfo[-1]
    path = path_to_file.replace(fname, '')
    os.chdir(path.replace('/', os.sep))
    f = open(fname)
    data = f.read()
    f.close()
    os.chdir(initfolder)
    return json.loads(data)

def show_info_by_info(json_file, print_fields, index_pos):
    info_file = load_json('./{}'.format(json_file))
    for i in info_file[index_pos:]:
        limpar_tela()
        print_nfo = ""
        for f in print_fields:
            print_nfo += i[f].replace('/','') + os.linesep
        print(print_nfo)
        input("Pressione enter para continuar...")
