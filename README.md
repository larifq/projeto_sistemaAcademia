# Sistema de Cadastros

O projeto contém uma API constrída com FastAPI para realizar o cadastro dos alunos, tal como, registra a entrada e saída dos alunos.

* Criado em sistema Linux (Ubuntu)

# Pastas e Arquivos

```bash
projeto_sistemaAcademia/
├── database/
│   └── database.sql                 # Script para criação do banco de dados e tabelas
├── venv/                            # Ambiente virtual
├── data_database.py                 # Script que armazena as informações das credenciais para acessar o banco de dados
├── database.py                      # Script para conectar ao banco de dados
├── exeAPI.sh                        # Script para executar uma API (Linux/macOS)
├── exeAPI.bat                       # Script para executar uma API (Windows)
├── main.py                          # Código principal da API
└── requisitos.txt                   # Bibliotecas e dependências do projeto
```

## Instalação e Inicialização

    Para baixar o repositório utilize o git clone (https://github.com/larifq/projeto_sistemaAcademia.git).

### Banco de Dados
     1 - Instalar o banco de dados postgree (versão 17.5) 
     2 - Instalar a aplicação desktop ou web para administrar o Banco de Dados 
     3 - Em database.sql há o script para utilizar para criar o banco e as tabelas
     4 - No arquivo data_database.py insira suas credencias (usuario e senha)
     5 - Verificar se a porta que está utilizando é 5432. Se for outra porta, no arquivo database.py substitua a nova porta na variavel self.conecta_banco o código: `postgresql+psycopg2://{usuario}:{senha}@{hospedagem}:`**5432**`/{nome_db}`
     
### API - FastAPI
    Para executar a API, você pode rodar diretamente o arquivo exeAPI.sh (em sistemas Linux/macOS) ou o arquivo exeAPI.bat (no Windows).

    Caso o script não funcione no Windows, remova a pasta venv e crie o ambiente virtual novamente utilizando o comando: python -m venv venv

**Observação**: Para consultar as versões das bibliotecas usadas, consulte o arquivo requirements.txt, que pode ser usado para reinstalar as dependências.

## Swagger
    Para realizar o registro (POST) de alunos utilize: http://127.0.0.1:8000/docs#/default/registrar_aluno_alunos_registro_post
    Para realizar o registro (POST) do checkin utilize: http://127.0.0.1:8000/docs#/default/registrar_checkin_aluno_checkin_post

## Informações adicionais
    O que falta no projeto:
    1 - GET para informações de frequência e outro para probabilidade de abandono
    2 - RabbitMQ
    3 - Machine Learning
