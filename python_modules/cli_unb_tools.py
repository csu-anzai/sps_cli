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

def old_sae_extract_list(target_folder=old_etd_folder, target_csv_lista_processos=old_sae_processos_list, init_idx=6190):
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
			if re.search("^\s*\d\d/\d\d\d*", line) != None:
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
		if re.search("^.*\d\d\d\d\d", line_editada[1]) != None:
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
			if re.search("^\s*[A-Z]*\s*GR$", line) != None:
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
			if re.search("^\s*\d\d\d\d\d\d", line) != None:
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
			
	


def process_sigra_hist(hist_file_txt):
	'''
	'''
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
	total_creditos_aprovados_por_semestre = []
	nreg_mat = 0
	tgj_geral = 0
	tgj_saude = 0
	tgm_geral = 0
	ss_num = 0
	ms_num = 0
	mm_num = 0
	mi_num = 0
	ii_num = 0
	sr_num = 0
	tr_num = 0
	cc_num = 0
	
	for line in conteudo:
		if obter_matricula == True:
			if re.search("^\s*\d\d/\d*", line) != None:
				matricula = line.replace(' ',';')
				while matricula.find(';;') != -1:
					matricula = matricula.replace(';;',';')
				matricula = matricula.split(';')[1]#.replace('/','')
				obter_matricula = False
				print(matricula)
		
		if obter_nome == True:
			if conteudo.index(line) == 4:
				nome = line.replace('  ','').strip()
				obter_nome = False
				print(nome)
				
		if obter_curso == True:
			if conteudo.index(line) == 5:
				curso = line.replace('  ','').strip()
				obter_curso = False
				print(curso)
				'''
				if curso == "Educação do Campo (Diurno)":
					pass
				else:
					obter_curso = False
					print(curso)
					curric_list = os.listdir(curric_folder)
					for c in curric_list:
						if c.find(curso) != -1:
							curso_cod = c.split('-')[0].strip()
							print(curso_cod)
							curric_nfo = read_csv(os.path.join(curric_folder, c))
							curric_metadados_nfo = read_csv(os.path.join(curric_metadados_folder, "Cursos_Metainfo.csv"))
							for c_nfo in curric_metadados_nfo:
								if c_nfo['Código Habilitação'] == curso_cod:
									creditos_p_formar = c_nfo['Quantidade de créditos para formatura']
									turno = c_nfo['Turno']
									break
							break'''
			
			'''if conteudo.index(line) == 6:
				curso = line.split(':')[1].strip()
				if curso == "Educação do Campo - Ciências da Natureza e Matemática":
					curso = "Educação do Campo - Ciências da Natureza"
				obter_curso = False
				print(curso)
				curric_list = os.listdir(curric_folder)
				for c in curric_list:
					if c.find(curso) != -1:
						curso_cod = c.split('-')[0].strip()
						print(curso_cod)
						curric_nfo = read_csv(os.path.join(curric_folder, c))
						curric_metadados_nfo = read_csv(os.path.join(curric_metadados_folder, "Cursos_Metainfo.csv"))
						for c_nfo in curric_metadados_nfo:
							if c_nfo['Código Habilitação'] == curso_cod:
								creditos_p_formar = c_nfo['Quantidade de créditos para formatura']
								turno = c_nfo['Turno']
								break
						break				'''
						

		if obter_nome_pai == True:
			if re.search("^\s*Pai\:", line) != None:
				nome_pai = line.split(':')[1].strip()
				obter_nome_pai = False
				print(nome_pai)
				
		if obter_nome_mae == True:
			if re.search("^\s*Mãe\:", line) != None:
				nome_mae = line.split(':')[1].strip()
				obter_nome_mae = False
				print(nome_mae)

		if obter_dn == True:
			if re.search("^\s*Nascimento\:", line) != None:
				dn = line.replace('  ',':')
				while dn.find('::') != -1:
					dn = dn.replace('::',':')
				dn = dn.split(':')[2].strip()
				obter_dn = False
				print(dn)
			
		if re.search("^\s*Período\:", line) != None:
			if line.find('(Continuação)') != -1:
				pass
			elif re.search("^\s*\d\d\d\d/0", line) != None:
				verao += 1
			else:
				periodo += 1
				calculo_ira[periodo] = []
				
		if re.search("^\s*Aluno não registrou matrícula no Período", line) != None:
			calculo_ira[periodo] = "Aluno não registrou matrícula no Período"
			nreg_mat += 1
			
		if re.search("^\s*Trancamento Geral Justificado", line) != None:
			calculo_ira[periodo] = "Trancamento Geral Justificado"
			tgj_geral += 1

		if re.search("^\s*Trancamento Geral Justificado (Problema de Saúde)", line) != None:
			calculo_ira[periodo] = "Trancamento Geral Justificado (Problema de Saúde)"
			tgj_saude += 1
		
		if re.search("^\s*Trancamento Geral de Matrícula", line) != None:
			calculo_ira[periodo] = "Trancamento Geral de Matrícula"
			tgm_geral += 1

		if re.search("^\s*Período em Realização", line) != None:
			calculo_ira[periodo] = "Período em Realização"
		
		if re.search("^\s*\d\d\d\d\d\d", line) != None:
			idx_target = 98
			#if line[idx_target] == " ":
			#	idx_target += 1
			calculo_ira[periodo].append(line[idx_target:idx_target+5].strip())

			idx_target = 106
			calculo_ira[periodo].append(line[idx_target:idx_target+5].strip())
			
			
			'''
			if line.find("Métodos de Organização e Educação Comunitária  1") != 1:
				line = line.replace("Métodos de Organização e Educação Comunitária  1", "Métodos de Organização e Educação Comunitária 1")
			if line.find("HISTORIA  DA PSICOLOGIA") != -1:
				line = line.replace("HISTORIA  DA PSICOLOGIA", "HISTORIA DA PSICOLOGIA")
			disciplina = line.replace('  ',';').replace('\n','')
			while disciplina.find(';;') != -1:
				disciplina = disciplina.replace(';;',';')
			disciplina = disciplina.split(';')[1:]
			disciplina.append(periodo)
			calculo_ira[periodo].append(disciplina)'''
	
	print(calculo_ira)
	exit()

	ira_por_semestre = []
	
	for periodo in calculo_ira.keys():

		ira_numerador = 0
		ira_denominador = 0
		ira_TR = 0
		ira_tr_obr = 0
		ira_tr_opt = 0
		tj_obr = 0
		tj_opt = 0
		ira_total_creditos = 0
		total_creditos_aprovados = 0

		for disciplina in calculo_ira[periodo]:
			#print(disciplina)
			creditos = float(disciplina[3])
			ira_total_creditos += creditos
			disciplina_tipo = "ML"
			for disciplina_curricular in curric_nfo:
				if disciplina_curricular['Código'] == disciplina[0]:
					disciplina_tipo = disciplina_curricular['Tipo']
					break			
			if  disciplina[2].find('SS')  != -1:
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
			
			elif disciplina[2].find('MS') != -1:
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

			elif disciplina[2].find('MM') != -1:
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
		
			elif disciplina[2].find('MI') != -1:
				peso = 2.0
			
			elif disciplina[2].find('II') != -1:
				peso = 1.0
			
			elif disciplina[2].find('SR') != -1:
				peso = 0.0
			
			elif disciplina[2].find('TR') != -1:
				peso = 0.0
				if disciplina_tipo == 'OBR':
					ira_tr_obr += 1
				elif disciplina_tipo == 'OPT':
					ira_tr_opt += 1
			
			elif disciplina[2].find('TJ') != -1:
				peso = 0.0
				if disciplina_tipo == 'OBR':
					tj_obr += 1
				elif disciplina_tipo == 'OPT':
					tj_opt += 1
					
			elif disciplina[2].find('DP') != -1:
				peso = 0.0

			elif disciplina[2].find('TM') != -1:
				peso = 0.0

			elif disciplina[2].find('AP') != -1:
				peso = 0.0

			elif disciplina[2].find('CC') != -1:
				peso = 0.0
				cc += creditos
			
			numerador = float(peso) * float(disciplina[3]) * float(disciplina[4])
			denominador = float(disciplina[3]) * float(disciplina[4])
			
			ira_numerador += numerador
			ira_denominador += denominador
		
		if not calculo_ira[periodo] == []:
			ira = (1.0 - (((0.6 * ira_tr_obr) + (0.4 * ira_tr_opt))/ira_total_creditos)) * (ira_numerador/ira_denominador)
			ira_por_semestre.append(ira)
			total_creditos_aprovados_por_semestre.append(total_creditos_aprovados)
		
	percentual_d_conclusao = float((total_creditos_obr_aprovados + total_creditos_opt_aprovados + total_creditos_mod_aprovados)/(float(creditos_p_formar)) * 100)
	expectativa_de_semestres_adicionais = (float(creditos_p_formar) - (total_creditos_obr_aprovados + total_creditos_opt_aprovados + total_creditos_mod_aprovados)) / mediaa(total_creditos_aprovados_por_semestre)
	
	'''
	print("Periodo: " + str(periodo))
	print("Curso de verão: " + str(verao))
	print("Variação no IRA: " + str(ira_por_semestre))
	print("Média IRA: " + str(mediaa(ira_por_semestre)))
	print("Créditos OBR obtidos: " + str(total_creditos_obr_aprovados))
	print("Créditos OPT obtidos: " + str(total_creditos_opt_aprovados))
	print("Créditos Módulo Livre obtidos: " + str(total_creditos_mod_aprovados))
	print("Média céditos obtidos por semestre: " + str(mediaa(total_creditos_aprovados_por_semestre)))
	print("Quantidade de creditos para formar: " + str(creditos_p_formar))
	print("Percentual de conclusão do curso: " + str(percentual_d_conclusao) +"%")
	print("Expectativa de semestres para conclusão do curso: " + str(expectativa_de_semestres_adicionais))
	print("Turno: " + str(turno))
	input('...')
	'''
	
	output['Matrícula'] = matricula
	output['Data de Nascimento'] = dn
	output['Pai'] = nome_pai
	output['Mae'] = nome_mae
	output['Código Habilitação'] = curso_cod
	output['Turno do curso'] = turno
	output['Créditos a obter'] = creditos_p_formar
	output['Percentual de conclusão do curso'] = creditos_p_formar
	output['Média de créditos obtidos por semestre'] = mediaa(total_creditos_aprovados_por_semestre)
	output['Quantidade de semestres cursados'] = periodo
	output['Quantidade de semestres de verão cursados'] = verao
	output['Quantidade de semestres sem registro de matrícula'] = nreg_mat
	output['TGJs'] = tgj_geral
	output['TGJs Saúde'] = tgj_saude
	output['TGMs'] = tgm_geral
	output['Expectativa de semestres à cursar até a conclusão'] = expectativa_de_semestres_adicionais
	output['IRA médio'] = mediaa(ira_por_semestre)
	output['Total créditos OBR obtidos'] = total_creditos_obr_aprovados
	output['Total créditos OPT obtidos'] = total_creditos_opt_aprovados
	output['Total créditos ML obtidos'] = total_creditos_mod_aprovados
		
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
		try:
			hist_files_data.append(process_sigra_hist(hfile))
			os.remove(hfile)
		except:
			error_count += 1
			#os.remove(hfile)
			matricula_dos_erros.append(hfile.split('.')[0])
			
	os.chdir(initdir)
	try: 
		os.removedirs(path_name)
	except: 
		print("Houve erros no processamento de alguns históricos. Estes arquivos não foram excluídos...")
	write_csv(hist_files_data, 'academic_analisis.csv')
	return matricula_dos_erros

