#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#
#
#  Copyright 2017 Daniel Cruz <bwb0de@bwb0dePC>
#  Version 0.1
#
#  This program is free software; you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation; either version 2 of the License, or
#  (at your option) any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program; if not, write to the Free Software
#  Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston,
#  MA 02110-1301, USA.
#
#


import zipfile
import os
import shutil

from string import whitespace, punctuation, digits
from .py_euristic_tools import strip_simbols, get_indexes, strip_digits, strip_chars
from .py_functions_calculation import mediaa
from .py_functions_csv import *
from .py_functions_json import save_json
from math import fsum as soma

curric_folder = '/home/danielc/Documentos/SPS/Currículos/FUP'
curric_metadados_folder = '/home/danielc/Documentos/SPS/Dados_AES/Consultas'
old_etd_folder = '/home/bwb0de/Devel/sps_fup2/working_folder/SPS-UnB-Data_pesquisa/SPS/DadosAES/OldSAE_ESTUDOS/'
old_sae_processos_list = "/home/bwb0de/Devel/sps_fup2/working_folder/SPS-UnB-Data_pesquisa/SPS/DadosAES/Informações_antigas_SAE-candidatos_processos_seletivos.csv"

def old_sae_etd_rename_files(target_folder=old_etd_folder):
	files = os.listdir(target_folder)
	init_folder = os.getcwd()
	os.chdir(target_folder)
	for f in files:
		if f.find('.txt') != -1:
			file_sae_etd = open(f, encoding="cp1252")
			file_sae_etd_data = file_sae_etd.readlines()
			file_sae_etd.close()
			for line in file_sae_etd_data:
				if line.find("Período") != -1:
					periodo = line.split(";")[1]
					periodo = periodo.replace('/','-')
					os.rename(f, f.replace('.txt', '_{}.txt'.format(periodo)))
					break
	os.chdir(init_folder)

def old_sae_etd_strip_chars(target_folder=old_etd_folder):
	subfolders = os.listdir(target_folder)
	init_folder = os.getcwd()
	os.chdir(target_folder)
	for s in subfolders:
		os.chdir(s)
		files = os.listdir('.')
		for f in files:
			f_nnome = strip_chars(f.split('.')[0])+'.txt'
			os.rename(f, f_nnome)
		os.chdir('..')
	os.chdir(init_folder)




def old_sae_etd_movefiles_to_folder(target_folder=old_etd_folder):
	files = os.listdir(target_folder)
	init_folder = os.getcwd()
	os.chdir(target_folder)
	new_folders = []
	for f in files:
		if f.find('.txt') != -1:
			print(f)
			fname = f.split('_')[1].split('.')[0]
			if not fname in new_folders:
				try:
					os.mkdir(fname)
					new_folders.append(fname)
				except FileExistsError:
					new_folders.append(fname)
			shutil.move(f, "{}/{}/{}".format(target_folder, fname, f))

def old_sae_extract_hist_list(target_folder=old_etd_folder, target_csv_lista_processos=old_sae_processos_list, init_idx=0):
	processos = read_csv(target_csv_lista_processos, '\t')
	total_itens = len(processos)-1
	current_item = init_idx
	total_itens -= init_idx
	idts_verificados = []
	while total_itens != -1:
		periodo = processos[current_item]['Semestre/Ano'].replace('/','-')
		matricula = processos[current_item]['Matrícula'].replace('/','')
		op = None
		if not matricula in idts_verificados:
			idts_verificados.append(matricula)
			limpar_tela()
			print(processos[current_item]['Nome'])
			print(matricula)
			print(periodo)
			print("IDX:", current_item)
			op = input("Pressione 'v' para voltar, enter para seguir...")
		if op == 'v':
			current_item -= 1
			total_itens += 1
		else:
			current_item += 1
			total_itens -= 1


def old_sae_extract_list(target_folder=old_etd_folder, target_csv_lista_processos=old_sae_processos_list, init_idx=6663):
	processos = read_csv(target_csv_lista_processos, '\t')
	total_itens = len(processos)-1
	current_item = init_idx
	total_itens -= init_idx
	while total_itens != -1:
		periodo = processos[current_item]['Semestre/Ano'].replace('/','-')
		matricula = processos[current_item]['Matrícula'].replace('/','')
		fname = matricula+"_"+periodo+'.txt'
		if not os.path.isfile('{}/{}/{}'.format(target_folder, periodo, fname)):
			limpar_tela()
			print(processos[current_item]['Nome'])
			print(matricula)
			print(periodo)
			print("IDX:", current_item)
			op = input("Pressione 'v' para voltar, enter para seguir...")
		else:
			op = None
		if op == 'v':
			current_item -= 1
			total_itens += 1
		else:
			current_item += 1
			total_itens -= 1


def fix_tgm_list(csv_file):
	conteudo = read_csv(csv_file, delimiter='\t')
	for line in conteudo:
		if line["Semestre"] == '':
			line["Semestre"] = line["Motivo"]
			line["Motivo"] = ''
	write_csv(conteudo, csv_file, delimiter='\t')
	
def fix_tgm_list_concat(csv_file):
	'''
	Concatena múltiplas linhas em uma com base no semestre do relatório de trancamento...
	'''
	conteudo = read_csv(csv_file, delimiter='\t')
	last_mat = ''
	last_sem = ''
	for line in conteudo:
		if line['Matrícula'] == last_mat:
			line['Semestre'] = line['Semestre'] +'; '+ last_sem
		last_mat = line['Matrícula']
		last_sem = line['Semestre']
	write_csv(conteudo, csv_file, delimiter='\t')
	

def fix_tgm_semestres(csv_file):
	'''
	Concatena múltiplas linhas em uma com base no semestre do relatório de trancamento...
	'''
	conteudo = read_csv(csv_file, delimiter='\t')
	for line in conteudo:
		if line['Semestre'].find(';') != -1:
			l = line['Semestre'].replace(' ','').split(';')
			ll = []
			for i in set(l):
				ll.append(i)
			ll.sort()
			line['Semestre'] = '; '.join(ll)
	write_csv(conteudo, csv_file, delimiter='\t')	
	


def define_tgmj_sem_count(csv_file):
	conteudo = read_csv(csv_file)
	map_sem_col = set(read_csv_col("Semestre", csv_file))
	for line in conteudo:
		for v in map_sem_col:
			line['TGM_'+v] = 0
			line['TGJ_'+v] = 0
			
		if line['TG Tipo'] == 'TGM':
			line['TGM_'+line["Semestre"]] = 1
		elif line['TG Tipo'] == 'TGJ':
			line['TGJ_'+line["Semestre"]] = 1
			
	write_csv(conteudo, csv_file)	


def define_deslig_sem_count(csv_file):
	conteudo = read_csv(csv_file)
	map_sem_col = set(read_csv_col("SEM_DESLIG", csv_file))
	for line in conteudo:
		for v in map_sem_col:
			line['DESLIG_'+v] = 0
			
		line['DESLIG_'+line["SEM_DESLIG"]] = 1
			
	write_csv(conteudo, csv_file)	


def define_formados_sem_count(csv_file):
	conteudo = read_csv(csv_file)
	map_sem_col = set(read_csv_col("SEM_FORM", csv_file))
	for line in conteudo:
		for v in map_sem_col:
			line['FORMADO_'+v] = 0
			
		line['FORMADO_'+line["SEM_FORM"]] = 1
			
	write_csv(conteudo, csv_file)	


def fix_sem_part_nfo(csv_file):
	'''
	Esta função corrige a tabela completa de dados referente à estudantes da assistencia estudantil de forma a substituir os campos vazios "", por 0.
	'''
	
	conteudo = read_csv(csv_file)
	for line in conteudo:
		if line['09-1'] == '':
			line['09-1'] = 0
		if line['09-2'] == '':
			line['09-2'] = 0
		if line['10-1'] == '':
			line['10-1'] = 0
		if line['10-2'] == '':
			line['10-2'] = 0
		if line['11-1'] == '':
			line['11-1'] = 0
		if line['11-2'] == '':
			line['11-2'] = 0
		if line['12-1'] == '':
			line['12-1'] = 0
		if line['12-2'] == '':
			line['12-2'] = 0
		if line['13-1'] == '':
			line['13-1'] = 0
		if line['13-2'] == '':
			line['13-2'] = 0
		if line['14-1'] == '':
			line['14-1'] = 0
		if line['14-2'] == '':
			line['14-2'] = 0
		if line['15-1'] == '':
			line['15-1'] = 0
		if line['15-2'] == '':
			line['15-2'] = 0
		if line['16-1'] == '':
			line['16-1'] = 0
		if line['16-2'] == '':
			line['16-2'] = 0
		if line['17-1'] == '':
			line['17-1'] = 0
		if line['17-2'] == '':
			line['17-2'] = 0
		if line['18-1'] == '':
			line['18-1'] = 0
		if line['18-2'] == '':
			line['18-2'] = 0
	write_csv(conteudo, csv_file)




def define_new_students_on_AES(csv_file):
	'''
	Esta função tem como entrada a tabela completa de dados referente à estudantes da assistencia estudantil. Parte do arquivo deve coincidir com a estrutura definida no escopo da função para que a análise seja funcional.
	'''
	
	conteudo = read_csv(csv_file)
	for line in conteudo:
		line['NOVOS_EM_09-1'] = 0
		line['NOVOS_EM_09-2'] = 0
		line['NOVOS_EM_10-1'] = 0
		line['NOVOS_EM_10-2'] = 0
		line['NOVOS_EM_11-1'] = 0
		line['NOVOS_EM_11-2'] = 0
		line['NOVOS_EM_12-1'] = 0
		line['NOVOS_EM_12-2'] = 0
		line['NOVOS_EM_13-1'] = 0
		line['NOVOS_EM_13-2'] = 0
		line['NOVOS_EM_14-1'] = 0
		line['NOVOS_EM_14-2'] = 0
		line['NOVOS_EM_15-1'] = 0
		line['NOVOS_EM_15-2'] = 0
		line['NOVOS_EM_16-1'] = 0
		line['NOVOS_EM_16-2'] = 0
		line['NOVOS_EM_17-1'] = 0
		line['NOVOS_EM_17-2'] = 0
		line['NOVOS_EM_18-1'] = 0
		line['NOVOS_EM_18-2'] = 0
		if float(line['09-1']) > 0:
			line['NOVOS_EM_09-1'] = 1
		elif soma([float(line['09-1']), float(line['09-2'])]) > 0:
			line['NOVOS_EM_09-2'] = 1
		elif soma([float(line['09-1']), float(line['09-2']), float(line['10-1'])]) > 0:
			line['NOVOS_EM_10-1'] = 1
		elif soma([float(line['09-1']), float(line['09-2']), float(line['10-1']), float(line['10-2'])]) > 0:
			line['NOVOS_EM_10-2'] = 1
		elif soma([float(line['09-1']), float(line['09-2']), float(line['10-1']), float(line['10-2']), float(line['11-1'])]) > 0:
			line['NOVOS_EM_11-1'] = 1
		elif soma([float(line['09-2']), float(line['10-1']), float(line['10-2']), float(line['11-1']), float(line['11-2'])]) > 0:
			line['NOVOS_EM_11-2'] = 1
		elif soma([float(line['10-1']), float(line['10-2']), float(line['11-1']), float(line['11-2']), float(line['12-1'])]) > 0:
			line['NOVOS_EM_12-1'] = 1
		elif soma([float(line['10-2']), float(line['11-1']), float(line['11-2']), float(line['12-1']), float(line['12-2'])]) > 0:
			line['NOVOS_EM_12-2'] = 1
		elif soma([float(line['11-1']), float(line['11-2']), float(line['12-1']), float(line['12-2']), float(line['13-1'])]) > 0:
			line['NOVOS_EM_13-1'] = 1
		elif soma([float(line['11-2']), float(line['12-1']), float(line['12-2']), float(line['13-1']), float(line['13-2'])]) > 0:
			line['NOVOS_EM_13-2'] = 1
		elif soma([float(line['12-1']), float(line['12-2']), float(line['13-1']), float(line['13-2']), float(line['14-1'])]) > 0:
			line['NOVOS_EM_14-1'] = 1
		elif soma([float(line['12-2']), float(line['13-1']), float(line['13-2']), float(line['14-1']), float(line['14-2'])]) > 0:
			line['NOVOS_EM_14-2'] = 1
		elif soma([float(line['13-1']), float(line['13-2']), float(line['14-1']), float(line['14-2']), float(line['15-1'])]) > 0:
			line['NOVOS_EM_15-1'] = 1
		elif soma([float(line['13-2']), float(line['14-1']), float(line['14-2']), float(line['15-1']), float(line['15-2'])]) > 0:
			line['NOVOS_EM_15-2'] = 1
		elif soma([float(line['14-1']), float(line['14-2']), float(line['15-1']), float(line['15-2']), float(line['16-1'])]) > 0:
			line['NOVOS_EM_16-1'] = 1
		elif soma([float(line['14-2']), float(line['15-1']), float(line['15-2']), float(line['16-1']), float(line['16-2'])]) > 0:
			line['NOVOS_EM_16-2'] = 1
		elif soma([float(line['15-1']), float(line['15-2']), float(line['16-1']), float(line['16-2']), float(line['17-1'])]) > 0:
			line['NOVOS_EM_17-1'] = 1
		elif soma([float(line['15-2']), float(line['16-1']), float(line['16-2']), float(line['17-1']), float(line['17-2'])]) > 0:
			line['NOVOS_EM_17-2'] = 1
		elif soma([float(line['16-1']), float(line['16-2']), float(line['17-1']), float(line['17-2']), float(line['18-1'])]) > 0:
			line['NOVOS_EM_18-1'] = 1
		elif soma([float(line['16-2']), float(line['17-1']), float(line['17-2']), float(line['18-1']), float(line['18-2'])]) > 0:
			line['NOVOS_EM_18-2'] = 1
	write_csv(conteudo, csv_file)




def calculate_mediaa_of_new_on_sem(csv_file):
	'''
	Calcula a média de estudantes novos que solicitaram vinculo à AES, por semestre. Fas isso apenas para os anos em que ampos os semestres possuem estudantes novos evitando distorções no resultado por falta de dados.
	'''
	
	conteudo = read_csv(csv_file)
	sem20091 = 0
	sem20092 = 0
	sem20101 = 0
	sem20102 = 0
	sem20111 = 0
	sem20112 = 0
	sem20121 = 0
	sem20122 = 0
	sem20131 = 0
	sem20132 = 0
	sem20141 = 0
	sem20142 = 0
	sem20151 = 0
	sem20152 = 0
	sem20161 = 0
	sem20162 = 0
	sem20171 = 0
	sem20172 = 0
	sem20181 = 0
	sem20182 = 0
	for line in conteudo:
		if int(line['NOVOS_EM_09-1']) != 0:
			sem20091 += 1
		elif line['NOVOS_EM_09-2'] != 0:
			sem20092 += 1
		elif line['NOVOS_EM_10-1'] != 0:
			sem20101 += 1
		elif line['NOVOS_EM_10-2'] != 0:
			sem20102 += 1
		elif line['NOVOS_EM_11-1'] != 0:
			sem20111 += 1
		elif line['NOVOS_EM_11-2'] != 0:
			sem20112 += 1
		elif line['NOVOS_EM_12-1'] != 0:
			sem20121 += 1
		elif line['NOVOS_EM_12-2'] != 0:
			sem20122 += 1
		elif line['NOVOS_EM_13-1'] != 0:
			sem20131 += 1
		elif line['NOVOS_EM_13-2'] != 0:
			sem20132 += 1
		elif line['NOVOS_EM_14-1'] != 0:
			sem20141 += 1
		elif line['NOVOS_EM_14-2'] != 0:
			sem20142 += 1
		elif line['NOVOS_EM_15-1'] != 0:
			sem20151 += 1
		elif line['NOVOS_EM_15-2'] != 0:
			sem20152 += 1
		elif line['NOVOS_EM_16-1'] != 0:
			sem20161 += 1
		elif line['NOVOS_EM_16-2'] != 0:
			sem20162 += 1
		elif line['NOVOS_EM_17-1'] != 0:
			sem20171 += 1
		elif line['NOVOS_EM_17-2'] != 0:
			sem20172 += 1
		elif line['NOVOS_EM_18-1'] != 0:
			sem20181 += 1
		elif line['NOVOS_EM_18-2'] != 0:
			sem20182 += 1
	
	if not (sem20091 == 0 or sem20092 == 0):
		mediaa([])
	if not (sem20101 == 0 or sem20102 == 0):
		mediaa([])
	if not (sem20111 == 0 or sem20112 == 0):
		mediaa([])
	if not (sem20121 == 0 or sem20122 == 0):
		mediaa([])
	if not (sem20131 == 0 or sem20132 == 0):
		mediaa([])
	if not (sem20141 == 0 or sem20142 == 0):
		mediaa([])
	if not (sem20151 == 0 or sem20152 == 0):
		mediaa([])
	if not (sem20161 == 0 or sem20162 == 0):
		mediaa([])
	if not (sem20171 == 0 or sem20172 == 0):
		mediaa([])
	if not (sem20181 == 0 or sem20182 == 0):
		mediaa([])
	

def join_alurel(folder, output_fname):
	'''
	Junta todas as linhas do relatório de alunos em um único arquivo de saída.
	Os relatórios de alunos são extraidos do sistema SIGRA da UnB.
	'''
	
	initdir = os.getcwd()
	os.chdir(folder)
	files_to_join = os.listdir('.')
	
	output = []
	
	for fi in files_to_join:
		fi_underscore_idx = len(get_indexes('_', fi))
		semestre_val = fi.split('_')[fi_underscore_idx].split('.')[0]
		f = open(fi, 'r', encoding="iso-8859-1")
		conteudo = f.readlines()
		f.close()
		
		for line in conteudo:
			if linha.find("\s*\d\d/\d\d\d*", line) != None:
				if line.find(":") == -1:
					line = line.replace('   ','\t').replace('\n','')
					while line.find('\t\t') != -1:
						line = line.replace('\t\t','\t')
					line = line.replace('/','').split('\t')[1:]
					striped_line = []
					for item in line:
						striped_line.append(item.strip())
					line = '\t'.join(striped_line)
					line = line + '\t' + semestre_val + '\n'
					output.append(line)
	
	f = open(output_fname, 'w')
	f.writelines(output)
	f.close()


def fix_joined_alurel(csv_file, delimiter='\t'):
	'''
	'''
	
	with open(csv_file) as f:
		conteudo = f.readlines()
	
	conteudo_editado = []
	for line in conteudo:
		line_editada = line.split(delimiter)
		if linha.find(".*\d\d\d\d\d", line_editada[1]) != None:
			num = line_editada[1].split(' ').pop()
			line_editada[1] = strip_simbols(line_editada[1]).strip()+delimiter+num
		line_editada = delimiter.join(line_editada)
		conteudo_editado.append(line_editada)
	
	with open(csv_file, 'w') as f:
		f.writelines(conteudo_editado)
		

def get_curric_branches(csv_file, habilit_num_col, curric_branche_col):
	'''
	Percorre a tabela de alunos de forma a criar um par ordenado entre habilitação e versão do currículo, sem duplicatas.
	'''
	conteudo = read_csv(csv_file)
	
	o = []
	for line in conteudo:
		o.append(str(line["Nível do Curso"])+';'+str(line[habilit_num_col])+';'+str(line[curric_branche_col])+os.linesep)
	o.sort()
	
	output_data = []
	for r in o:
		if not r in output_data:
			output_data.append(r)
	f = open('output_curric_L', 'w')
	f.writelines(output_data)
	f.close()
	
	


def set_campus_from_hcode(csv_file, hcode_col, campus_col):
	'''
	Define o campus do curso com base na avaliação do código da habiliatação e registra na coluna 'campus_col'.
	Não sobrescreve valores existentes. 
	'''	
	conteudo = read_csv(csv_file)
	
	#Códigos extraídos do matrícula web em 28/11/2018...
	planaltina = ['2283', '2291', '9636', '9628', '761', '6157', '6190', '21776', '21768', '50008', '21890', '21725', '51926']
	gama = ['6009', '60836', '6297', '6289', '6360', '6131', '51811', '5886']
	ceilandia = ['7072', '7013', '7137', '60852', '7153', '7145', '21784', '281', '51152', '51136']
	
	for line in conteudo:
		#if line[campus_col] != '':
			if line[hcode_col] in planaltina:
				line[campus_col] = 'FUP'
			elif line[hcode_col] in gama:
				line[campus_col] = 'FGA'
			elif line[hcode_col] in ceilandia:
				line[campus_col] = 'FCE'
			else:
				line[campus_col] = 'Darcy Ribeiro'
	
	write_csv(conteudo,csv_file)
	
def mask_cpf_col(csv_file, cpf_col):
	conteudo = read_csv(csv_file)
	
	for line in conteudo:
		formated_cpf = line[cpf_col].zfill(11)
		formated_cpf = formated_cpf[0:3]+'.'+formated_cpf[3:6]+'.'+formated_cpf[6:9]+'-'+formated_cpf[9:]
		line[cpf_col] = formated_cpf
		if line[cpf_col] == '000.000.000-00':
			line[cpf_col] = ''
		
	write_csv(conteudo,csv_file)


def process_curric(curric_file_txt):
	'''
	'''
	f = open(curric_file_txt, 'r', encoding="iso-8859-1")
	conteudo = f.readlines()
	f.close()
	
	curric_novo_nome = curric_file_txt.replace('.txt','.csv')
	curric_metainfo = curric_file_txt.replace('.txt','-metainfo.txt')
	
	grau = ''
	semestre = ''
	minimo = ''
	maximo = ''
	minimo_semestres = ''
	maximo_semestres = ''
	tipo_disciplina = ''
	creditos_disciplina = ''
	area = ''
	disciplina_code = ''
	dep = ''
	h_code = ''
	h_nome = ''
	write_line = False
	next_line_get = False
	get_dep = True
	novo_conteudo = []
	line_count = 0
	
	for line in conteudo:
		line_count += 1
		if line_count == 13:
			h_code = line.replace('\n','').split(':')[1].strip()

		elif line_count == 14:
			h_nome = line.replace('\n','').split('-')[1].strip()

		elif line_count == 17:
			line = line.replace('  ','^')
			while line.find('^^') != -1:
				line = line.replace('^^','^')
			semestre = line.split('^')[2]					
					
		elif line_count == 19:
			grau = line.replace('\n','').strip()

		elif line_count == 22:
			line = line.replace('  ','^')
			while line.find('^^') != -1:
				line = line.replace('^^','^')
			line = line.replace(' :^', ':')
			minimo = line.split(':')[2].split('^')[0]
			maximo = line.split(':')[3].split('\n')[0].strip()

		elif line_count == 23:
			line = line.replace('  ','^')
			while line.find('^^') != -1:
				line = line.replace('^^','^')
			line = line.replace(' :^', ':')
			minimo_semestres = line.split(':')[2].split('^')[0]
			maximo_semestres = line.split(':')[3].split('\n')[0].strip()
		
		if line.find('Disciplinas Obrigatórias') != -1:
			tipo_disciplina = 'OBR'
		elif line.find('Disciplinas Optativas') != -1:
			tipo_disciplina = 'OPT'
			
		if get_dep == True:
			if linha.find("\s*[A-Z]*\s*GR$", line) != None:
				dep = line.replace('   ','^')
				while dep.find('^^') != -1:
					dep = dep.replace('^^','^')
				dep = dep.split('^')[1].strip()
				get_dep == False

		if re.search(".*\d\d\d\s*\d\d\d\s*\d\d\d\s*", line) != None:
			line = line.replace('   ','^')
			while line.find('^^') != -1:
				line = line.replace('^^','^')
			creditos_disciplina = int(line.split('^')[2]) + int(line.split('^')[3]) + int(line.split('^')[4])
			area = line.split('^')[6].replace('\n','').strip()
			next_line_get = True
			
		if next_line_get == True:
			if linha.find("\s*\d\d\d\d\d\d", line) != None:
				disciplina_code = line.strip()
				write_line = True
				next_line_get = False
				
		if write_line == True:
			nova_linha = OrderedDict()
			nova_linha['Código Disciplina'] = disciplina_code
			nova_linha['Tipo Disciplina'] = tipo_disciplina
			nova_linha['Departamento'] = dep
			nova_linha['Créditos'] = creditos_disciplina
			nova_linha['Área'] = area
			novo_conteudo.append(nova_linha)
			write_line = False
			get_dep = True
			
		
	
	metainfo_data = []
	metainfo_data.append("Grau:{grau}\n".format(grau=grau))
	metainfo_data.append("Mínimo semestres:{min_s}\n".format(min_s=minimo_semestres))
	metainfo_data.append("Máximo semestres:{max_s}\n".format(max_s=maximo_semestres))
	metainfo_data.append("Mínimo créditos por semestre:{min_c}\n".format(min_c=minimo))
	metainfo_data.append("Máximo créditos por semestre:{max_c}\n".format(max_c=maximo))
	metainfo_data.append("Código habilitação:{h_code}\n".format(h_code=h_code))
	metainfo_data.append("Nome habilitação:{h_nome}".format(h_nome=h_nome))
	
	with open(curric_metainfo, 'w') as meta_file:
		meta_file.writelines(metainfo_data)
	
	write_csv(novo_conteudo, curric_novo_nome, delimiter='\t', lineterminator='\n')
			

def process_sae_etd(sae_etd_file_txt):
	f = open(sae_etd_file_txt, 'r', encoding="iso-8859-1")
	conteudo = f.readlines()
	f.close()

	print(os.getcwd(), sae_etd_file_txt)
	
	output = OrderedDict()	

	obter_matricula = True
	obter_nome = True
	obter_periodo_estudo = True
	obter_motivos = True
	obter_curso_nivel = True
	obter_curso_nome = True
	obter_campus = True
	obter_periodo_ingresso_unb = True
	obter_forma_ingresso = True
	obter_sexo = True
	obter_cpf = True
	obter_isencao_vestibular = True
	obter_teve_abatimento = True
	obter_cor = True
	obter_escola_em_tipo = True
	obter_escola_em_nome = True
	obter_escola_em_cidade = True
	obter_escola_em_uf = True
	obter_fez_pre_vestibular = True
	obter_faz_outro_curso_superior = True
	obter_fez_outro_curso_superior = True
	obter_situacao_prof_corrente = True
	obter_situacao_prof_anterior = True
	obter_contribui_p_rendafam = True
	obter_cidade_moradia_sae = False
	obter_cidade_moradia_sigra = False
	obter_email = False
	obter_com_quem_reside = False
	obter_situacao_residencia_familia = False
	obter_estado_civil_estudante = True
	obter_pai_nome = False
	obter_pai_cpf = False
	obter_pai_cidade = False
	obter_pai_endereco = False
	obter_pai_endereco_uf = False
	obter_pai_escolaridade = False
	obter_pai_profissao = False
	obter_pai_remuneracao = False
	obter_mae_nome = False
	obter_mae_cpf = False
	obter_mae_cidade = False
	obter_mae_endereco = False
	obter_mae_endereco_uf = False
	obter_mae_escolaridade = False
	obter_mae_profissao = False
	obter_mae_remuneracao = False
	obter_transporte_usado = True
	obter_grupo_familiar = False
	obter_justificativa = False
	obter_pontuacao = False
	obter_pontuacao_vinculo_emprego_estudante = False
	obter_pontuacao_cidade_estudante = False
	obter_pontuacao_vinculo_emprego_pai = False
	obter_pontuacao_vinculo_emprego_mae = False
	obter_pontuacao_vinculo_emprego_mantenedor = False
	obter_pontuacao_fx_renda = False
	obter_pontuacao_parecer = False

	check_if_global_moradia_field = True
	check_if_dados_pai_field = True
	check_if_dados_mae_field = True
	check_if_grpfam_field = True
	check_if_justificativa_field = True
	check_if_pontuacao_field = True

	justificativa = ""
	pontuacao_vinculo_emprego_estudante = ""
	pontuacao_cidade_estudante = ""
	pontuacao_vinculo_emprego_pai = ""
	pontuacao_vinculo_emprego_mae = ""
	pontuacao_vinculo_emprego_mantenedor = ""
	pontuacao_fx_renda = ""
	pontuacao_parecer = ""

	for linha in conteudo:
		if obter_matricula:
			if linha.find("Matrícula: ;") != -1:
				matricula = linha.split(": ;")[1].split(";")[0].strip()
				obter_matricula = False
			
		if obter_nome:
			if linha.find("Nome: ;") != -1:
				nome = linha.split(": ;")[2].split(";")[0].strip()
				obter_nome = False
			
		if obter_periodo_estudo:
			if linha.find("Período: ;") != -1:
				periodo_estudo = linha.split(": ;")[1].split(";")[0].strip()
				obter_periodo_estudo = False
			
		if obter_motivos:
			if linha.find("Motivo(s): ;") != -1:
				motivos = linha.split(": ;")[1].split(";")[0].strip()
				obter_motivos = False

		if obter_curso_nivel:
			if linha.find("Nível: ;") != -1:
				curso_nivel = linha.split(": ;")[2].split(";")[0].strip()
				obter_curso_nivel = False

		if obter_curso_nome:
			if linha.find("Curso: ;") != -1:
				curso_nome = linha.split(": ;")[3].split(";")[0].strip()
				obter_curso_nome = False

		if obter_campus:
			if linha.find("Campus: ;") != -1:
				campus = linha.split(": ;")[1].split(";")[0].strip()
				obter_campus = False
			
		if obter_periodo_ingresso_unb:
			if linha.find("Período de ingresso: ;") != -1:
				periodo_ingresso_unb = linha.split(": ;")[1].split(";")[0].strip()
				obter_periodo_ingresso_unb = False
			
		if obter_forma_ingresso:
			if linha.find("Forma de ingresso: ;") != -1:
				forma_ingresso = linha.split(": ;")[1].split(";")[0].strip()
				obter_forma_ingresso = False

		if obter_sexo:
			if linha.find("Sexo:;") != -1:
				sexo = linha.split(":;")[1].split(";")[0].strip()
				obter_sexo = False
			
		if obter_cpf:
			if linha.find("CPF: ;") != -1:
				cpf = linha.split(": ;")[2].split(";")[0].strip()
				obter_cpf = False
			
		if obter_isencao_vestibular:
			if linha.find("Isenção taxa vestibular: ;") != -1:
				isencao_vestibular = linha.split(": ;")[1].split(";")[0].strip()
				if isencao_vestibular == "Não":
					teve_abatimento = "Não se aplica"
					obter_teve_abatimento = False
				obter_isencao_vestibular = False

		if obter_teve_abatimento:
			if linha.find("Teve abatimento: ;") != -1:
				teve_abatimento = linha.split(": ;")[2].split(";")[0].strip()
				obter_teve_abatimento = False

		if obter_cor:
			if linha.find("Raça: ;") != -1:
				cor = linha.split(": ;")[1].split(";")[0].strip()
				obter_cor = False
			
		if obter_escola_em_tipo:
			if linha.find("Ensino médio: ;") != -1:
				escola_em_tipo = linha.split(": ;")[1].split(";")[0].strip()
				obter_escola_em_tipo = False

		if obter_escola_em_nome:
			if re.search("\s*Escola: ;", linha) != None:
				escola_em_nome = linha.split(": ;")[1].split(";")[0].strip()
				obter_escola_em_nome = False
			
		if obter_escola_em_cidade:
			if re.search("\s*Escola: ;", linha) != None:
				escola_em_cidade = linha.split(": ;")[2].split(";")[0].strip()
				obter_escola_em_cidade = False
			
		if obter_escola_em_uf:
			if re.search("\s*Escola: ;", linha) != None:
				escola_em_uf = linha.split(": ;")[3].split(";")[0].strip()
				obter_escola_em_uf = False
			
		if obter_fez_pre_vestibular:
			if linha.find("Pré-vestibular: ;") != -1:
				fez_pre_vestibular = linha.split(": ;")[1].split(";")[0].strip()
				obter_fez_pre_vestibular = False

		if obter_faz_outro_curso_superior:
			if linha.find("Faz outro curso superior fora da UnB?: ;") != -1:
				faz_outro_curso_superior = linha.split(": ;")[1].split(";")[0].strip()
				outro_curso_superior_ies = ""
				obter_faz_outro_curso_superior = False
			elif linha.find("Curso superior sendo feito fora da UnB: ;") != -1:
				faz_outro_curso_superior = linha.split(": ;")[1].split(";")[0].strip()
				outro_curso_superior_ies = linha.split(": ;")[2].split(";")[0].strip()
				obter_faz_outro_curso_superior = False				

		if obter_fez_outro_curso_superior:
			if linha.find("Fez outro curso de nível superior? ;") != -1:
				fez_outro_curso_superior = linha.split("? ;")[1].split(";")[0].strip()
				obter_fez_outro_curso_superior = False			

		if obter_situacao_prof_corrente:
			if linha.find("Situação Profissional/Renda") != -1:
				situacao_prof_corrente = linha.split(" - ")[1].split(";")[0].strip()
				obter_situacao_prof_corrente = False			

		if obter_situacao_prof_anterior:
			if linha.find("Já trabalhou? ;") != -1:
				situacao_prof_anterior = linha.split("? ;")[1].split(";")[0].strip()
				obter_situacao_prof_anterior = False
			elif linha.find("Já trabalhou na atividade: ;") != -1:
				situacao_prof_anterior = linha.split(": ;")[1].split(";")[0].strip()
				obter_situacao_prof_anterior = False

		if obter_contribui_p_rendafam == True:
			if linha.find("Contribui p/ renda familiar? ;") != -1:
				contribui_p_rendafam = linha.split("? ;")[1].split(";")[0].strip()
				obter_contribui_p_rendafam = False
			
		if check_if_global_moradia_field:
			if linha.find("Situação Atual de Moradia;") != -1:
				obter_cidade_moradia_sae = True
				obter_cidade_moradia_sigra = True
				obter_email = True
				obter_com_quem_reside = True
				obter_situacao_residencia_familia = True
				check_if_global_moradia_field = False

		if obter_cidade_moradia_sae:
			if linha.find("Cidade: ;") != -1:
				cidade_moradia_sae = linha.split(": ;")[2].split(";")[0].strip()
				endereco_moradia_sae = linha.split(": ;")[1].split(";")[0].strip()
				obter_cidade_moradia_sae = False
			
		if obter_cidade_moradia_sigra:
			if linha.find("Endereço DAA: ;") != -1:
				endereco_moradia_sigra = linha.split(": ;")[1].split(";")[0].strip()
				obter_cidade_moradia_sigra = False
			
		if obter_email:
			if linha.find("Email: ;") != -1:
				try:
					email = linha.split(": ;")[3].split(";")[0].strip()
				except IndexError:
					email = ""
				obter_email = False
			
		if obter_com_quem_reside:
			if linha.find("Como reside atualmente? ;") != -1:
				com_quem_reside = linha.split("? ;")[1].split(";")[0].strip().replace(".",'')
				obter_com_quem_reside = False
			else:
				com_quem_reside = "Outra situação: "+linha.split(";")[0].strip()
				obter_com_quem_reside = False				
			
		if obter_situacao_residencia_familia:
			if linha.find("Como reside sua família? ;") != -1:
				situacao_residencia_familia = linha.split("? ;")[1].split(";")[0].strip().replace(".",'')
				obter_situacao_residencia_familia = False

		if obter_estado_civil_estudante:
			if linha.find("Estado civil: ;") != -1:
				estado_civil_estudante = linha.split(": ;")[1].split(";")[0].strip().replace(".",'')
				obter_estado_civil_estudante = False

		if check_if_dados_pai_field:
			if linha.find("Dados do Pai;") != -1:
				obter_pai_nome = True
				obter_pai_cpf = True
				obter_pai_cidade = True
				obter_pai_endereco = True
				obter_pai_endereco_uf = True
				obter_pai_escolaridade = True
				obter_pai_profissao = True
				obter_pai_remuneracao = True
				check_if_dados_pai_field = False

		if obter_pai_nome:
			if linha.find("Nome: ;") != -1:
				pai_nome = linha.split(": ;")[1].split(";")[0].strip()
				if linha.find("Falecido") != -1:
					pai_situacao = "Falecido"
					pai_remuneracao = "Não se aplica"
					pai_profissao = "Não se aplica"
					pai_cpf = "Não se aplica"
					pai_cidade = "Não se aplica"
					pai_endereco = "Não se aplica"
					pai_endereco_uf = "Não se aplica"
					pai_escolaridade = "Não se aplica"
				elif linha.find("Desconhecido") != -1:
					pai_situacao = "Desconhecido"
					pai_remuneracao = "Não se aplica"
					pai_profissao = "Não se aplica"
					pai_cpf = "Não se aplica"
					pai_cidade = "Não se aplica"
					pai_endereco = "Não se aplica"
					pai_endereco_uf = "Não se aplica"
					pai_escolaridade = "Não se aplica"
				else:
					pai_situacao = "Vivo"
				obter_pai_nome = False
			
		if obter_pai_cpf:
			if linha.find("CPF: ;") != -1:
				pai_cpf = linha.split(": ;")[3].split(";")[0].strip()
				pai_idade = linha.split(": ;")[2].split(";")[0].strip()
				obter_pai_cpf = False

		if obter_pai_cidade:
			if linha.find("Cidade: ;") != -1:
				pai_cidade = linha.split(": ;")[2].split(";")[0].strip()
				obter_pai_cidade = False
			
		if obter_pai_endereco:
			if linha.find("Endereço: ;") != -1:
				pai_endereco = linha.split(": ;")[1].split(";")[0].strip()
				obter_pai_endereco = False

		if obter_pai_endereco_uf:
			if linha.find("UF: ;") != -1:
				pai_endereco_uf = linha.split(": ;")[1].split(";")[0].strip()
				obter_pai_endereco_uf = False

		if obter_pai_escolaridade:
			if linha.find("Grau de instrução: ;") != -1:
				pai_escolaridade = linha.split(": ;")[1].split(";")[0].strip()
				obter_pai_escolaridade = False
			
		if obter_pai_profissao:
			if linha.find("Profissão: ;") != -1:
				pai_profissao = linha.split(": ;")[1].split(";")[0].strip()
				obter_pai_profissao = False
			
		if obter_pai_remuneracao:
			if linha.find("Remuneração (R$): ;") != -1:
				pai_remuneracao = linha.split(": ;")[2].split(";")[0].strip()
				obter_pai_remunaracao = False

		if check_if_dados_mae_field:
			if linha.find("Dados da Mãe;") != -1:
				obter_mae_nome = True
				obter_mae_cpf = True
				obter_mae_cidade = True
				obter_mae_endereco = True
				obter_mae_endereco_uf = True
				obter_mae_escolaridade = True
				obter_mae_profissao = True
				obter_mae_remuneracao = True
				check_if_dados_mae_field = False

		if obter_mae_nome:
			if linha.find("Nome: ;") != -1:
				mae_nome = linha.split(": ;")[1].split(";")[0].strip()
				if linha.find("Falecida") != -1:
					mae_situacao = "Falecida"
					mae_remuneracao = "Não se aplica"
					mae_profissao = "Não se aplica"
					mae_cpf = "Não se aplica"
					mae_cidade = "Não se aplica"
					mae_endereco = "Não se aplica"
					mae_endereco_uf = "Não se aplica"
					mae_escolaridade = "Não se aplica"
				elif linha.find("Desconhecida") != -1:
					mae_situacao = "Desconhecida"
					mae_remuneracao = "Não se aplica"
					mae_profissao = "Não se aplica"
					mae_cpf = "Não se aplica"
					mae_cidade = "Não se aplica"
					mae_endereco = "Não se aplica"
					mae_endereco_uf = "Não se aplica"
					mae_escolaridade = "Não se aplica"
				else:
					mae_situacao = "Viva"
				obter_mae_nome = False
			
		if obter_mae_cpf:
			if linha.find("CPF: ;") != -1:
				mae_cpf = linha.split(": ;")[3].split(";")[0].strip()
				mae_idade = linha.split(": ;")[2].split(";")[0].strip()
				obter_mae_cpf = False

		if obter_mae_cidade:
			if linha.find("Cidade: ;") != -1:
				mae_cidade = linha.split(": ;")[2].split(";")[0].strip()
				obter_mae_cidade = False
			
		if obter_mae_endereco:
			if linha.find("Endereço: ;") != -1:
				mae_endereco = linha.split(": ;")[1].split(";")[0].strip()
				obter_mae_endereco = False

		if obter_mae_endereco_uf:
			if linha.find("UF: ;") != -1:
				mae_endereco_uf = linha.split(": ;")[1].split(";")[0].strip()
				obter_mae_endereco_uf = False

		if obter_mae_escolaridade:
			if linha.find("Grau de instrução: ;") != -1:
				mae_escolaridade = linha.split(": ;")[1].split(";")[0].strip()
				obter_mae_escolaridade = False
			
		if obter_mae_profissao:
			if linha.find("Profissão: ;") != -1:
				mae_profissao = linha.split(": ;")[1].split(";")[0].strip()
				obter_mae_profissao = False
			
		if obter_mae_remuneracao:
			if linha.find("Remuneração (R$): ;") != -1:
				mae_remuneracao = linha.split(": ;")[2].split(";")[0].strip()
				obter_mae_remunaracao = False
			
		if obter_transporte_usado:
			if linha.find("Meio de transporte utilizado semanalmente: ;") != -1:
				transporte_usado = linha.split(": ;")[1].split(";")[0].strip()
				obter_transporte_usado = False				

		if obter_justificativa == True:
				if linha.find("Pontuação;") == -1:
					justificativa += linha
				else:
					obter_justificativa = False


		if check_if_justificativa_field:
			if linha.find("Justiticativa;") != -1:			
				obter_justificativa = True
				check_if_justificativa_field = False

		if obter_pontuacao:
			if obter_pontuacao_vinculo_emprego_estudante:
				if linha.find("Cidade do aluno: ;") != -1:
					obter_pontuacao_vinculo_emprego_estudante = False
				else:
					pontuacao_vinculo_emprego_estudante += linha

			if obter_pontuacao_cidade_estudante:
				if linha.find("Profissão do pai: ;") != -1:
					obter_pontuacao_cidade_estudante = False
				else:
					pontuacao_cidade_estudante += linha

			if obter_pontuacao_vinculo_emprego_pai:
				if linha.find("Profissão da mãe: ;") != -1:
					obter_pontuacao_vinculo_emprego_pai = False
				else:
					pontuacao_vinculo_emprego_pai += linha

			if obter_pontuacao_vinculo_emprego_mae:
				if linha.find("Profissão do mantenedor/cônjuge: ;") != -1:
					obter_pontuacao_vinculo_emprego_mae = False
				else:
					pontuacao_vinculo_emprego_mae += linha

			if obter_pontuacao_vinculo_emprego_mantenedor:
				if linha.find("Faixa de renda: ;") != -1:
					obter_pontuacao_vinculo_emprego_mantenedor = False
				else:
					pontuacao_vinculo_emprego_mantenedor += linha
			
			if obter_pontuacao_fx_renda:
				if linha.find("Parecer técnico: ;") != -1: 
					obter_pontuacao_fx_renda = False
				else:
					pontuacao_fx_renda += linha
			
			if obter_pontuacao_parecer:
				if linha.find("Independente: ;") != -1:
					obter_pontuacao_parecer = False
				else:
					pontuacao_parecer += linha

			if linha.find("Profissão do aluno: ;") != -1:
				obter_pontuacao_vinculo_emprego_estudante = True
			
			elif linha.find("Cidade do aluno: ;") != -1:
				obter_pontuacao_cidade_estudante = True
			
			elif linha.find("Profissão do pai: ;") != -1:
				obter_pontuacao_vinculo_emprego_pai = True
			
			elif linha.find("Profissão da mãe: ;") != -1:
				obter_pontuacao_vinculo_emprego_mae = True
			
			elif linha.find("Profissão do mantenedor/cônjuge: ;") != -1:
				obter_pontuacao_vinculo_emprego_mantenedor = True
			
			elif linha.find("Faixa de renda: ;") != -1:
				obter_pontuacao_fx_renda = True
			
			elif linha.find("Parecer técnico: ;") != -1: 
				obter_pontuacao_parecer = True
			
			elif linha.find("Grupo: ;") != -1:
				pontuacao_grupo = linha.split(": ;")[3].split(";")[0].strip()

			elif linha.find("Assistente social: ;") != -1:
				pontuacao_assistente_social = linha.split(": ;")[1].split(";")[0].strip()


		if check_if_pontuacao_field:
			if linha.find("Pontuação;") != -1:
				obter_pontuacao = True


	output["matricula"] = matricula
	output["nome"] = nome
	output["periodo_estudo"] = periodo_estudo
	output["motivos"] = motivos
	output["curso_nivel"] = curso_nivel
	output["curso_nome"] = curso_nome
	output["campus"] = campus
	output["periodo_ingresso_unb"] = periodo_ingresso_unb
	output["forma_ingresso"] = forma_ingresso
	output["sexo"] = sexo
	output["cpf"] = cpf
	try:
		output["isencao_vestibular"] = isencao_vestibular
		output["teve_abatimento"] = teve_abatimento
	except:
		output["isencao_vestibular"] = "Não se aplica"
		output["teve_abatimento"] = "Não se aplica"
	output["cor"] = cor
	output["escola_em_tipo"] = escola_em_tipo
	output["escola_em_nome"] = escola_em_nome
	output["escola_em_cidade"] = escola_em_cidade
	output["escola_em_uf"] = escola_em_uf
	try:
		output["fez_pre_vestibular"] = fez_pre_vestibular
	except UnboundLocalError:
		output["fez_pre_vestibular"] = ""
	output["faz_outro_curso_superior"] = faz_outro_curso_superior
	output["outro_curso_superior_ies"] = outro_curso_superior_ies
	output["fez_outro_curso_superior"] = fez_outro_curso_superior
	output["situacao_prof_corrente"] = situacao_prof_corrente
	output["situacao_prof_anterior"] = situacao_prof_anterior
	output["contribui_p_rendafam"] = contribui_p_rendafam
	output["cidade_moradia_sae"] = cidade_moradia_sae
	output["endereco_moradia_sae"] = endereco_moradia_sae
	output["endereco_moradia_sigra"] = endereco_moradia_sigra
	try:
		output["email"] = email
	except UnboundLocalError:
		output["email"] = ""
	output["com_quem_reside"] = com_quem_reside
	try:
		output["situacao_residencia_familia"] = situacao_residencia_familia
	except UnboundLocalError:
		output["situacao_residencia_familia"] = ""
	output["estado_civil_estudante"] = estado_civil_estudante
	output["pai_nome"] = pai_nome
	output["pai_situacao"] = pai_situacao
	try:
		output["pai_cpf"] = pai_cpf
	except UnboundLocalError:
		output["pai_cpf"] = ""
	output["pai_cidade"] = pai_cidade
	output["pai_endereco"] = pai_endereco
	try:
		output["pai_endereco_uf"] = pai_endereco_uf
	except UnboundLocalError:
		output["pai_endereco_uf"] = ""
	output["pai_escolaridade"] = pai_escolaridade
	output["pai_profissao"] = pai_profissao
	output["pai_remuneracao"] = pai_remuneracao
	output["mae_nome"] = mae_nome
	output["mae_situacao"] = mae_situacao
	output["mae_cpf"] = mae_cpf
	output["mae_cidade"] = mae_cidade
	output["mae_endereco"] = mae_endereco
	try:
		output["mae_endereco_uf"] = mae_endereco_uf
	except UnboundLocalError:
		output["mae_endereco_uf"] = ""		
	output["mae_escolaridade"] = mae_escolaridade
	output["mae_profissao"] = mae_profissao
	try:
		output["mae_remuneracao"] = mae_remuneracao
	except UnboundLocalError:
		output["mae_remuneracao"] = ""
	output["transporte_usado"] = transporte_usado
	output["justificativa"] = justificativa.replace(";"," ").replace('\n',' ').replace('  ',' ').strip()
	output["pontuacao_vinculo_emprego_estudante"] = pontuacao_vinculo_emprego_estudante.replace(";"," ").replace('\n',' ').replace('  ',' ').strip()
	output["pontuacao_cidade_estudante"] = pontuacao_cidade_estudante.replace(";"," ").replace('\n',' ').replace('  ',' ').strip()
	output["pontuacao_vinculo_emprego_pai"] = pontuacao_vinculo_emprego_pai.replace(";"," ").replace('\n',' ').replace('  ',' ').strip()
	output["pontuacao_vinculo_emprego_mae"] = pontuacao_vinculo_emprego_mae.replace(";"," ").replace('\n',' ').replace('  ',' ').strip()
	output["pontuacao_vinculo_emprego_mantenedor"] = pontuacao_vinculo_emprego_mantenedor.replace(";"," ").replace('\n',' ').replace('  ',' ').strip()
	output["pontuacao_fx_renda"] = pontuacao_fx_renda.replace(";"," ").replace('\n',' ').replace('  ',' ').strip()
	output["pontuacao_parecer"] = pontuacao_parecer.replace(";"," ").replace('\n',' ').replace('  ',' ').strip()
	try:
		output["pontuacao_grupo"] = pontuacao_grupo
	except UnboundLocalError:
		output["pontuacao_grupo"] = ""
	try:
		output["pontuacao_assistente_social"] = pontuacao_assistente_social
	except UnboundLocalError:
		output["pontuacao_assistente_social"] = ""
	
	return output	

def multiprocess_sae_etd():
	initdir = os.getcwd()
	output = []
	os.chdir(old_etd_folder)
	for folder in os.listdir(old_etd_folder):
		os.chdir(old_etd_folder)
		os.chdir(folder)
		for old_sae_file in os.listdir("."):
			old_sae_file_nfo = process_sae_etd(old_sae_file)
			output.append(old_sae_file_nfo)
	os.chdir(initdir)
	write_csv(output, "./old_sae_nfo.csv", delimiter='\t')



def process_sigra_hist(hist_file_txt):
	f = open(hist_file_txt, 'r', encoding="iso-8859-1")
	conteudo = f.readlines()
	f.close()
	
	output = OrderedDict()
	
	periodo = 0
	verao = 0
	cc = 0
	obter_nome = True
	obter_matricula = True
	obter_curso = True
	obter_nome_pai = True
	obter_nome_mae = True
	obter_dn = True
	calculo_ira = OrderedDict()
	total_creditos_obr_aprovados = 0
	total_creditos_opt_aprovados = 0
	total_creditos_mod_aprovados = 0
	total_cretitos_exigidos = 0
	total_creditos_obtidos = 0
	total_creditos_pendentes = 0
	total_creditos_aprovados_por_semestre = []
	nreg_mat = 0
	tgj_geral = 0
	tgj_saude = 0
	tgm_geral = 0
	
	for line in conteudo:
		if obter_matricula == True:
			if linha.find("\s*\d\d/\d*", line) != None:
				matricula = line.replace(' ',';')
				while matricula.find(';;') != -1:
					matricula = matricula.replace(';;',';')
				matricula = matricula.split(';')[1]#.replace('/','')
				obter_matricula = False
				
		
		if obter_nome == True:
			if conteudo.index(line) == 4:
				nome = line.replace('  ','').strip()
				obter_nome = False
				
				
		if obter_curso == True:
			if conteudo.index(line) == 5:
				curso = line.replace('  ','').strip()
				obter_curso = False
				

		if obter_nome_pai == True:
			if linha.find("\s*Pai\:", line) != None:
				nome_pai = line.split(':')[1].strip()
				obter_nome_pai = False
				
				
		if obter_nome_mae == True:
			if linha.find("\s*Mãe\:", line) != None:
				nome_mae = line.split(':')[1].strip()
				obter_nome_mae = False
				

		if obter_dn == True:
			if linha.find("\s*Nascimento\:", line) != None:
				dn = line.replace('  ',':')
				while dn.find('::') != -1:
					dn = dn.replace('::',':')
				dn = dn.split(':')[2].strip()
				obter_dn = False
				
			
		if linha.find("\s*Período\:", line) != None:
			if line.find('(Continuação)') != -1:
				pass
			elif linha.find("\s*\d\d\d\d/0", line) != None:
				verao += 1
			else:
				periodo += 1
				calculo_ira[periodo] = []
				
		if linha.find("\s*Aluno não registrou matrícula no Período", line) != None:
			calculo_ira[periodo] = "Aluno não registrou matrícula no Período"
			nreg_mat += 1
			
		if linha.find("\s*Trancamento Geral Justificado", line) != None:
			calculo_ira[periodo] = "Trancamento Geral Justificado"
			tgj_geral += 1

		if linha.find("\s*Trancamento Geral Justificado (Problema de Saúde)", line) != None:
			calculo_ira[periodo] = "Trancamento Geral Justificado (Problema de Saúde)"
			tgj_saude += 1
		
		if linha.find("\s*Trancamento Geral de Matrícula", line) != None:
			calculo_ira[periodo] = "Trancamento Geral de Matrícula"
			tgm_geral += 1

		if linha.find("\s*Período em Realização", line) != None:
			calculo_ira[periodo] = "Período em Realização"
		
		if linha.find("\s*\d\d\d\d\d\d", line) != None:
			idx_target = 98
			if line[idx_target:idx_target+5].strip() != "":
				mensao = line[idx_target:idx_target+5].strip()

			idx_target = 106
			if line[idx_target:idx_target+5].strip() != "":
				calculo_ira[periodo].append('OBR-Area-'+line[idx_target:idx_target+5].strip()+"-"+mensao)

			idx_target = 114
			if line[idx_target:idx_target+5].strip() != "":
				calculo_ira[periodo].append('OPT-Area-'+line[idx_target:idx_target+5].strip()+"-"+mensao)

			idx_target = 125
			if line[idx_target:idx_target+5].strip() != "":
				calculo_ira[periodo].append('OBR-Domínio-'+line[idx_target:idx_target+5].strip()+"-"+mensao)

			idx_target = 131
			if line[idx_target:idx_target+5].strip() != "":
				calculo_ira[periodo].append('OPT-Domínio-'+line[idx_target:idx_target+5].strip()+"-"+mensao)

			idx_target = 143
			if line[idx_target:idx_target+5].strip() != "":
				calculo_ira[periodo].append('MLV--'+line[idx_target:idx_target+5].strip()+"-"+mensao)
			
		if linha.find("\s*Curso.....", line) != None:
			idx_target = 55
			if line[idx_target:idx_target+5].strip() != "":
				total_cretitos_exigidos = int(line[idx_target:idx_target+5].strip())

			idx_target = 64
			if line[idx_target:idx_target+5].strip() != "":
				total_creditos_obtidos = int(line[idx_target:idx_target+5].strip())

			idx_target = 72
			if line[idx_target:idx_target+5].strip() != "":
				total_creditos_pendentes = int(line[idx_target:idx_target+5].strip())


	
	ira_por_semestre = []
	
	for periodo in calculo_ira.keys():
		if type(calculo_ira[periodo]) != list:
			pass
		else:

			ira_numerador = 0
			ira_denominador = 0
			#ira_TR = 0
			ira_tr_obr = 0
			ira_tr_opt = 0
			tj_obr = 0
			tj_opt = 0
			ira_total_creditos = 0
			total_creditos_aprovados = 0

			for disciplina in calculo_ira[periodo]:
				disciplina_split = disciplina.split("-")
				creditos = float(disciplina_split[2])
				disciplina_tipo = disciplina_split[0]
				mensao = disciplina_split[3]
				ira_total_creditos += creditos
				
				if mensao == "SS":
					peso = 5.0
					if disciplina_tipo == 'OBR':
						total_creditos_obr_aprovados += creditos
						total_creditos_aprovados += creditos
					elif disciplina_tipo == 'OPT':
						total_creditos_opt_aprovados += creditos
						total_creditos_aprovados += creditos
					else:
						total_creditos_mod_aprovados += creditos
						total_creditos_aprovados += creditos
				
				elif mensao == 'MS':
					peso = 4.0
					if disciplina_tipo == 'OBR':
						total_creditos_obr_aprovados += creditos
						total_creditos_aprovados += creditos
					elif disciplina_tipo == 'OPT':
						total_creditos_opt_aprovados += creditos
						total_creditos_aprovados += creditos
					else:
						total_creditos_mod_aprovados += creditos
						total_creditos_aprovados += creditos

				elif mensao == 'MM':
					peso = 3.0
					if disciplina_tipo == 'OBR':
						total_creditos_obr_aprovados += creditos
						total_creditos_aprovados += creditos
					elif disciplina_tipo == 'OPT':
						total_creditos_opt_aprovados += creditos
						total_creditos_aprovados += creditos
					else:
						total_creditos_mod_aprovados += creditos
						total_creditos_aprovados += creditos
			
				elif mensao == 'MI':
					peso = 2.0
				
				elif mensao == 'II':
					peso = 1.0
				
				elif mensao == 'SR':
					peso = 0.0
				
				elif mensao == 'TR':
					peso = 0.0
					if disciplina_tipo == 'OBR':
						ira_tr_obr += 1
					elif disciplina_tipo == 'OPT':
						ira_tr_opt += 1
				
				elif mensao == 'TJ':
					peso = 0.0
					if disciplina_tipo == 'OBR':
						tj_obr += 1
					elif disciplina_tipo == 'OPT':
						tj_opt += 1
						
				elif mensao == 'DP':
					peso = 0.0

				elif mensao == 'TM':
					peso = 0.0

				elif mensao == 'AP':
					peso = 0.0

				elif mensao == 'CC':
					peso = 0.0
					cc += creditos
				
				else:
					peso = 0.0
				
				numerador = float(peso) * float(creditos) * float(periodo)
				denominador = float(creditos) * float(periodo)
				
				ira_numerador += numerador
				ira_denominador += denominador
			
			if not calculo_ira[periodo] == []:
				total_creditos_aprovados_por_semestre.append(total_creditos_aprovados)
				try:
					ira = (1.0 - (((0.6 * ira_tr_obr) + (0.4 * ira_tr_opt))/ira_total_creditos)) * (ira_numerador/ira_denominador)
					ira_por_semestre.append(ira)
				except ZeroDivisionError:
					pass
		
	try:
		percentual_d_conclusao = float((total_creditos_obtidos/float(total_cretitos_exigidos)) * 100)
	except ZeroDivisionError:
		percentual_d_conclusao = "Impossível calcular"
	
	try:
		expectativa_de_semestres_adicionais = (float(total_cretitos_exigidos) - (total_creditos_obtidos)) / mediaa(total_creditos_aprovados_por_semestre)
	except ZeroDivisionError:
		expectativa_de_semestres_adicionais = "Impossível calcular"
	
	output['Matrícula'] = matricula
	output['Data de Nascimento'] = dn
	output['Pai'] = nome_pai
	output['Mae'] = nome_mae
	#output['Código Habilitação'] = "Criar Tabela - COD/CURSO/TURNO"
	output['Curso'] = curso
	if curso.find("Diurno") != -1:
		output['Turno do curso'] = "Diruno"
	else:
		output['Turno do curso'] = "Noturno"
	try:
		output['Média de créditos obtidos por semestre'] = mediaa(total_creditos_aprovados_por_semestre)
	except ZeroDivisionError:
		output['Média de créditos obtidos por semestre'] = "Impossível calcular"
	output['Quantidade de semestres cursados'] = periodo
	output['Quantidade de semestres de verão cursados'] = verao
	output['Quantidade de semestres sem registro de matrícula'] = nreg_mat
	output['TGJs'] = tgj_geral
	output['TGJs Saúde'] = tgj_saude
	output['TGMs'] = tgm_geral
	output['Expectativa de semestres à cursar até a conclusão'] = expectativa_de_semestres_adicionais
	output['Variação no IRA'] = ira_por_semestre
	try:
		output['IRA médio'] = mediaa(ira_por_semestre)
	except ZeroDivisionError:
		output['IRA médio'] = "Impossível calcular"
	output['Total créditos OBR obtidos'] = total_creditos_obr_aprovados
	output['Total créditos OPT obtidos'] = total_creditos_opt_aprovados
	output['Total créditos MLV obtidos'] = total_creditos_mod_aprovados
	output['Total créditos obtidos'] = total_creditos_obtidos
	output['Total créditos exigidos'] = total_cretitos_exigidos
	output['Créditos a obter'] = total_creditos_pendentes
	output['Percentual de conclusão do curso'] = str(percentual_d_conclusao)+"%"

	return output

				

def multi_process_curric(target_folder):
	os.chdir(target_folder)
	files = os.listdir('.')
	files.sort()
	for f in files:
		print("Processando currículo: {f}...".format(f=f))
		process_curric(f)
		
def create_csv_curric_metainfo(target_folder):
	pass


def multi_process_sigra_academic_history(filezip):
	#Get filezip name
	path_name = strip_simbols(filezip.split('.')[0])
	initdir = os.getcwd()
	zf = zipfile.ZipFile(filezip, 'r')
	os.mkdir(path_name)
	zf.extractall(path_name)
	os.chdir(path_name)
	hist_files = os.listdir('.')
	error_count = 0
	hist_files_data = []
	matricula_dos_erros = []
	for hfile in hist_files:
		hist_files_data.append(process_sigra_hist(hfile))
		os.remove(hfile)
		'''
		try:
			hist_files_data.append(process_sigra_hist(hfile))
			os.remove(hfile)
		except:
			error_count += 1
			#os.remove(hfile)
			matricula_dos_erros.append(hfile.split('.')[0])
		'''
			
	os.chdir(initdir)
	try: 
		os.removedirs(path_name)
	except: 
		print("Houve erros no processamento de alguns históricos. Estes arquivos não foram excluídos...")
	write_csv(hist_files_data, 'academic_analisis.csv')
	return matricula_dos_erros

