import time
from py_console_tools_v0 import load_json, listar_dicionario

def get_col_width(field_name, dict_array):
    width = 0
    for line in dict_array:
        if len(line[field_name]) > width:
            width = len(line[field_name])
    return (field_name, width+2)

def get_mat(db_estudantes):
    matriculas = []
    for estudantes in db_estudantes:
        matriculas.append(estudantes['mat'])
    return matriculas

def timestamp():
    return time.strftime("%Y-%m-%d %H:%M:%S %a", time.localtime())

form_atendiento = './forms/form_atendimento.json'
form_novo_estudante = './forms/form_novo_estudante.json'
form_estudo_socioeconomico = './forms/form_estudo_socioeconomico.json'
form_processos = './forms/form_processos.json'

db_atendimentos = load_json('./data/atendimentos.json')
db_estudantes = load_json('./data/estudantes.json')
db_profissionais = load_json('./data/profissionais.json')
db_processos = load_json('./data/processos.json')

col_width_etd_mat = get_col_width('mat', db_estudantes)
col_width_etd_nome = get_col_width('nome', db_estudantes)
col_width_etd_eml = get_col_width('eml', db_estudantes)
col_width_atend_time = ('timestamp', len(timestamp()) + 2)
col_width_atend_ident = col_width_etd_mat
col_width_prof_uid = get_col_width('uid', db_profissionais)
col_width_prof_nome = get_col_width('nome', db_profissionais)
col_width_prof_eml = get_col_width('eml', db_profissionais)

