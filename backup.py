# coding: utf8

import requests
import os
import time
import datetime
import pipes
from pcloud import PyCloud

    
# NOME BACKUP
NOME = 'SISTEMA'
# DADOS BANCO DE DADOS 
DB_HOST = 'localhost'
DB_USER = db_user.value
DB_USER_PASSWORD = db_pass.value
# Dados pcloud
pcloud_user= email.value
pcloud_senha = senha.value
#NOME DO BANCO DE DADOS
DB_NAME = db_name.value
#O CAMINHO AONDE VOCÊ QUER GUARDAR O BACKUP NO PC
BACKUP_PATH = 'bd'
# ARQUIVO DUMP MARIADB E MYSQL
dump1= 'mysqldump.exe'

#Gerar o nome do arquivo de acordo com a base de dados e a data e a hora atual 
data_atual = datetime.date.today()
DATETIME = time.strftime('%d_%m_%Y-%H-%M-%S')
TODAYBACKUPPATH = BACKUP_PATH + '/' + NOME + '_' +DATETIME


def check_internet():
    ''' checar conexÃ£o de internet '''
    url = 'https://www.google.com'
    timeout = 5
    try:
        requests.get(url, timeout=timeout)
        return True
    except requests.exceptions.ConnectionError:
        return False


#verficar se a pasta exites, caso não será criado.
try:
    os.stat(TODAYBACKUPPATH)
    print("diretorio não existe a pasta"+str(TODAYBACKUPPATH))
except:
    os.mkdir(TODAYBACKUPPATH)
    
    print("diretorio--criada---"+str(TODAYBACKUPPATH))

   
dumpcmd = dump1+" -h " + DB_HOST + " -u " + DB_USER + " -p" + DB_USER_PASSWORD + " " + DB_NAME + " --hex-blob > " + pipes.quote(TODAYBACKUPPATH) + "/" +NOME + '_'+data_atual.strftime('%d_%m_%Y_') + ".sql"
os.system(dumpcmd)


print ("")
print ("Backup local realizado com sucesso!")
print ("Confira o seu backup na pasta '" + TODAYBACKUPPATH + "' directory")



if not check_internet():
    print('Internet fora do ar!');
    conexao = False;
else:
		print('Internet OK!')
		conexao = True;
		pc = PyCloud(pcloud_user, pcloud_senha)

		pc.listfolder(path='/BACKUP - BANCO DE DADOS - DEMO')
		pc.createfolder(path='/BACKUP - BANCO DE DADOS - DEMO/'+NOME+'_'+DATETIME)

		pc.uploadfile(files=[TODAYBACKUPPATH+'/'+NOME+'_'+data_atual.strftime('%d_%m_%Y_') +'.sql'], path='/BACKUP - BANCO DE DADOS - DEMO/'+NOME+'_'+DATETIME)
		print('upload realizado com sucesso...')

		print ("Seu Backup esta na nuvem!")
print ("-----------------------------------------------")
print ("Backup Completo")
print ("-----------------------------------------------")
print ("---------------------^-^-----------------------")


