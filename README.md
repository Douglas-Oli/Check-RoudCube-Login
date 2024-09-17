# RoundCube Login Test Script

Este script em Python foi criado para testar o login em uma interface web RoundCube. Ele é compatível com Nagios e pode ser usado para monitoramento de serviços de email. O script mede o tempo de resposta das requisições e verifica se o login foi bem-sucedido.

## Pré-requisitos
- Python 3.x
- Bibliotecas Python: requests, beautifulsoup4

Você pode instalar as dependências usando o seguinte comando:

```
pip install requests beautifulsoup4
```

## Configuração
Antes de executar o script, configure as seguintes variáveis conforme suas necessidades:

- `login_page_url`: URL para acessar o formulário de login.
- `login_url`: URL para onde os dados de login são enviados.
- `login_data_timezone`: Fuso horário para o login.
- `login_data_user`: Nome de usuário para o login.
- `login_data_pass`: Senha para o login.

```
login_page_url = 'https://webmail.com.br/?_task=login'
login_url = 'https://webmail.com.br/?_task=login'
login_data_timezone = 'America/Sao_Paulo'
login_data_user = 'exemplo@dominio.com'
login_data_pass = 'senha@321'
```
## Funcionamento
1. O script faz uma requisição GET para obter a página de login e verificar o tempo de resposta.
2. Ele analisa o HTML para encontrar o token CSRF necessário para o login.
3. Envia uma requisição POST com os dados de login e o token CSRF.
Verifica o tempo de resposta da requisição POST e a presença de um link específico na resposta HTML para determinar se o login foi bem-sucedido.
4. Registra todas as mensagens e tempos de resposta em um arquivo de log chamado execution_log.txt.

## Mensagens e Códigos de Saída
- `0` - Login bem-sucedido.
- `1` - Tempo de resposta alto.
- `2` - Erro crítico (falha na requisição ou login).

## Exemplo de Uso
Execute o script com o seguinte comando:

```
python3 nome_do_script.py
```

Certifique-se de substituir nome_do_script.py pelo nome real do seu script.

## Contato
Se você tiver dúvidas ou precisar de suporte, entre em contato com:

- Douglas Oli. Silva
- Email: contact@douglas-olis.com.br
