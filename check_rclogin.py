#!/usr/bin/env python3
# -----------------------------------------------------------------------
# Script criado em 16/09/2024 por Douglas Oli. Silva
# Email: contact@douglas-olis.com.br
#
# Plugin criado para testar login em RoundCube compatível com Nagios
# -----------------------------------------------------------------------

# -----------------------------------------------------------------------
# Imports para execução do script
import requests
from bs4 import BeautifulSoup
import sys
import time
from datetime import datetime
import subprocess

# -----------------------------------------------------------------------
# Variáveis globais para execução do script

#   Define o limite de tempo em segundos para a resposta
TIMEOUT_WARNING_THRESHOLD = 5

#   URL para acessar o formulário de login. Em alguns casos podem conter a mesma URL!
login_page_url = 'https://webmail.com.br/?_task=login'
login_url = 'https://webmail.com.br/?_task=login'

#   Dados para o formulário de login
login_data_timezone = 'America/Sao_Paulo'
login_data_user = 'exemplo@dominio.com'
login_data_pass = 'senha@321'

#   Iniciar uma sessão para manter cookies e outros dados
session = requests.Session()

#   Adicionar headers, se necessário
headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
}

# -----------------------------------------------------------------------
# Início da execução

#   Função para salvar uma mensagem em um arquivo de log com a hora atual.
def log_message(message):
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    with open("execution_log.txt", "a") as log_file:
        log_file.write(f"{current_time} - {message}\n")

#   Medir o tempo de resposta da requisição GET
start_time = time.time()
response = session.get(login_page_url, headers=headers)
get_duration = time.time() - start_time

#   Verificar o status da requisição GET
if response.status_code != 200:
    error_message = f"CRITICAL: Erro na requisição GET. Status code: {response.status_code}"
    print(error_message)
    log_message(error_message)
    sys.exit(2)

#   Verificar o tempo de resposta da requisição GET
if get_duration > TIMEOUT_WARNING_THRESHOLD:
    # Cria a mensagem de aviso com a saída do script shell
    warning_message = f"WARNING: Tempo de resposta da requisição foi alto: {get_duration:.2f} segundos."
    print(warning_message)
    log_message(warning_message)
    sys.exit(1)

#   Analisar o HTML para encontrar o token CSRF
soup = BeautifulSoup(response.text, 'html.parser')
csrf_token_input = soup.find('input', {'name': '_token'})

#   Verificar se o campo _token foi encontrado e extrair o valor
if not csrf_token_input:
    error_message = "CRITICAL: Campo _token não encontrado no HTML."
    print(error_message)
    log_message(error_message)
    sys.exit(2)

csrf_token = csrf_token_input['value']

#   Dados do formulário de login com o token CSRF extraído
login_data = {
    '_token': csrf_token,
    '_task': 'login',
    '_action': 'login',
    '_timezone': login_data_timezone,
    '_url': '',
    '_user': login_data_user,
    '_pass': login_data_pass
}

#   Medir o tempo de resposta da requisição POST
start_time = time.time()
login_response = session.post(login_url, data=login_data, headers=headers, allow_redirects=True)
post_duration = time.time() - start_time

#   Verificar o status da requisição POST
if login_response.status_code != 200:
    error_message = f"CRITICAL: Erro na requisição POST. Status code: {login_response.status_code}"
    print(error_message)
    log_message(error_message)
    sys.exit(2)

#   Verificar o tempo de resposta da requisição POST
if post_duration > TIMEOUT_WARNING_THRESHOLD:
    warning_message = f"WARNING: Tempo de resposta da requisição POST foi alto: {post_duration:.2f} segundos"
    print(warning_message)
    log_message(warning_message)
    sys.exit(1)

#   Analisar o HTML da resposta para verificar a presença da linha esperada
soup = BeautifulSoup(login_response.text, 'html.parser')

#   Verificar se a linha com "Caixa de entrada" está presente, pois indica um login bem sucedido
expected_link = '<a href="./?_task=mail&amp;_mbox=INBOX" onclick="return rcmail.command(\'list\',\'INBOX\',this,event)" rel="INBOX">Caixa de entrada</a>'
if expected_link in login_response.text:
    success_message = (f"OK: Login bem-sucedido. Link 'Caixa de entrada' encontrado. "
                       f"Tempo de resposta da requisição GET: {get_duration:.2f} segundos. "
                       f"Tempo de resposta da requisição POST: {post_duration:.2f} segundos.")
    print(success_message)
    log_message(success_message)
    sys.exit(0)
else:
    error_message = (f"CRITICAL: Falha no login. Link 'Caixa de entrada' não encontrado. "
                     f"Tempo de resposta da requisição GET: {get_duration:.2f} segundos. "
                     f"Tempo de resposta da requisição POST: {post_duration:.2f} segundos.")
    print(error_message)
    log_message(error_message)
    sys.exit(2)
