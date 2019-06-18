#!/usr/bin/env python3
# -*- coding: utf-8 -*-

from subprocess import getoutput
from .cli_decorators import only_root
from .cli_sps_base import dados_profissionais
import os


def create_user_configuration():
    config = {}
    user_config_file = os.sep.join([getoutput('echo $HOME'), '.sps-cli.conf'])
    
    import getpass
    from python_modules.cli_tools import select_op
    from python_modules.py_functions_json import save_json
    
    nome = input("Insira o seu nome completo: ")
    eml = input("Insira o seu endereço de email: ")
    if eml.find('@unb.br') != -1:
        envio_automatico_email = input("Enviar emails automaticamente? [s|n]")

        if envio_automatico_email.lower() == 's':
            envio_automatico_email = True
            eml_server = "mail.unb.br"
            eml_port = "587"

            while True:
                eml_pwd = getpass.getpass('Insira a senha de acesso ao email apresentado: ')
                verificar_senha = getpass.getpass('Repita a senha informada: ')
                if eml_pwd == verificar_senha:
                    eml_pwd = getoutput('echo "{}" | base64'.format(eml_pwd))
                    break

        else:
            envio_automatico_email = False
            eml_pwd = ""
            eml_server = ""
            eml_port = ""

    print('Selecione a sua especialidade profissional: ')
    especialidade = select_op(['Assistente Social', 'Administrador', 'Administradora', 'Assistente Administrativo', 'Estatístico', 'Estatística', 'Pedagogo', 'Pedagoga', 'Psicólogo', 'Psicóloga', 'Técnico em assuntos educacionais', 'Técnica em assuntos educacionais'], 1, sort_list=True) 
    sigla_conselho = input('Informe a sigla do conselho profissional: ')
    numero_no_concelho = input('Qual a matrícula frente ao conselho profissional: ')
    matricula_instituicao = input('Qual a matrícula institucional: ')
    eml_assinatura = "Atenciosamente,\n---\n{nome}\n{cargo}\n{conselho} {matricula_conselho}\nFUB {matricula_fub}".format(nome=nome, cargo=especialidade, conselho=sigla_conselho, matricula_conselho=numero_no_concelho, matricula_fub=matricula_instituicao)

    config['nome']=eml
    config['eml']=eml
    config['envio_automatico_email']=envio_automatico_email
    config['eml_pwd']=eml_pwd
    config['eml_server']=eml_server
    config['eml_port']=eml_port
    config['especialidade']=especialidade
    config['sigla_conselho']=sigla_conselho
    config['numero_no_concelho']=numero_no_concelho
    config['matricula_instituicao']=matricula_instituicao
    config['eml_assinatura']=eml_assinatura

    save_json(config, user_config_file)


@only_root
def create_db_files(target_folder):
    init_dir = os.getcwd()
    os.chdir(target_folder)
    os.mkdir('seguranca')
    os.mkdir('eml-template')
    os.mkdir('dados')
    os.mkdir('dados/fragmentos')
    os.mkdir('dados/indexados')
    os.system('touch dados/atendimentos.json')
    os.system('touch dados/corrigidos.json')
    os.system('touch dados/processos.json')
    os.system('touch dados/profissionais.json')
    os.system('touch dados/usuarios.json')
    os.system('touch dados/estudos.json')
    os.system('touch dados/indexados/index_db.json')
    os.system('touch seguranca/ccrypt-key')
    os.system('if [ $(cat dados/atendimentos.json | wc -l) -lt 2 ]; then echo "[]" > dados/atendimentos.json; fi')
    os.system('if [ $(cat dados/corrigidos.json | wc -l) -lt 2 ]; then echo "[]" > dados/corrigidos.json; fi')
    os.system('if [ $(cat dados/processos.json | wc -l) -lt 2 ]; then echo "[]" > dados/processos.json; fi')
    os.system('if [ $(cat dados/profissionais.json | wc -l) -lt 2 ]; then echo "[]" > dados/profissionais.json; fi')
    os.system('if [ $(cat dados/usuarios.json | wc -l) -lt 2 ]; then echo "[]" > dados/usuarios.json; fi')
    os.system('if [ $(cat dados/estudos.json | wc -l) -lt 2 ]; then echo "[]" > dados/estudos.json; fi')
    os.system('if [ $(cat dados/backup-info.json | wc -l) -lt 2 ]; then echo "[]" > dados/backup-info.json; fi')    
    os.system('if [ $(cat dados/indexados/index_db.json | wc -l) -lt 2 ]; then echo "[]" > dados/indexados/index_db.json; fi')
    os.system('if [ $(cat dados/fragmentos/emitidos.json | wc -l) -lt 2 ]; then echo "[]" > dados/fragmentos/emitidos.json; fi')
    os.system('if [ $(cat dados/fragmentos/recebidos.json | wc -l) -lt 2 ]; then echo "[]" > dados/fragmentos/recebidos.json; fi')
    os.system('if [ $(cat seguranca/ccrypt-key | wc -c) -lt 5 ]; then randnum 1024 > seguranca/ccrypt-key; fi')
    os.chdir(init_dir)    


def backup_db(target_folder):
    check_folder = 0
    check_folder += int(getoutput("if [ -f {}/atendimentos.json ]; then echo 1; else echo 0; fi".format(target_folder)))
    check_folder += int(getoutput("if [ -f {}/corrigidos.json ]; then echo 1; else echo 0; fi".format(target_folder)))
    check_folder += int(getoutput("if [ -f {}/processos.json ]; then echo 1; else echo 0; fi".format(target_folder)))
    check_folder += int(getoutput("if [ -f {}/profissionais.json ]; then echo 1; else echo 0; fi".format(target_folder)))
    check_folder += int(getoutput("if [ -f {}/usuarios.json ]; then echo 1; else echo 0; fi".format(target_folder)))
    check_folder += int(getoutput("if [ -f {}/estudos.json ]; then echo 1; else echo 0; fi".format(target_folder)))
    check_folder += int(getoutput("if [ -f {}/backup-info.json ]; then echo 1; else echo 0; fi".format(target_folder)))
    check_folder += int(getoutput("if [ -d {}/indexados ]; then echo 1; else echo 0; fi".format(target_folder)))
    check_folder += int(getoutput("if [ -d {}/fragmentos ]; then echo 1; else echo 0; fi".format(target_folder)))
    check_folder += int(getoutput("if [ -f {}/indexados/index_db.json ]; then echo 1; else echo 0; fi".format(target_folder)))
    check_folder += int(getoutput("if [ -f {}/fragmentos/emitidos.json ]; then echo 1; else echo 0; fi".format(target_folder)))
    check_folder += int(getoutput("if [ -f {}/fragmentos/recebidos.json ]; then echo 1; else echo 0; fi".format(target_folder)))
    if check_folder == 12:
        print("Pasta de dados aparentemente íntegra...")
        bkfname = getoutput("date +%Y%U%u%H%M%S%N")+'.zip'
        os.system('zip "{bkf}" "{tf}" -9r'.format(bkf=bkfname, tf=target_folder))
        os.system('sps-encrypt "{bkf}"'.format(bkf=bkfname))
        os.system('rclone move "{bkf}.cpt" box:/sps_fup2/dbbk/'.format(bkf=bkfname))
    else:
        print("A estrutura da pasta de dados parece divergir...")


def restore_db():
    pass