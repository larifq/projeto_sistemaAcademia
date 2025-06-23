from sqlalchemy import create_engine, Table, MetaData # importar o create_engine para conectar ao banco
import psycopg2


class extrai_banco():
    # Função de construção que irá conectar e refletir o banco de dados
    def __init__(self, usuario, senha, hospedagem, nome_db):
        # Dados de acesso ao Banco de Dados
        self.usuario = usuario
        self.senha = senha
        self.hospedagem = hospedagem
        self.nome_db = nome_db
        # Conectar-se ao banco de dados - psycopg2 (conversa com o postgree) 
        self.conecta_banco = create_engine(f'postgresql+psycopg2://{usuario}:{senha}@{hospedagem}:5432/{nome_db}') 

        # Refletir todas tabelas do banco de dados
        self.metadata = MetaData()
        self.metadata.reflect(bind=self.conecta_banco)

    #Criar função para puxar a tabela alunos do banco de dados
    def extrair_tabela_alunos(self):
        return self.metadata.tables['alunos']

    #Criar função para puxar a tabela planos do banco de dados
    def extrair_tabela_planos(self):
        return self.metadata.tables['planos']
    
    #Criar função para puxar a tabela checkins do banco de dados
    def extrair_tabela_checkins(self):
        return self.metadata.tables['checkins']