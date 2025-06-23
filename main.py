# Importa a função do FastAPI para criar a api
from fastapi import FastAPI, HTTPException
from typing import Optional
# Importa decimal para usar na validação dos dados
from decimal import Decimal
# Importa Enum para usar na validação dos dados
from enum import Enum
# Importa datetime e date para usar na validação dos dados
from datetime import date, datetime
# Importa as funcionalidades do Pydantic para validação dos dados
from pydantic import BaseModel, Field, EmailStr
# função text do sqlalchemy para escrever as query
from sqlalchemy import text
# Importar a função conexao_banco do arquivo database.py para realizar as operações dentro do banco
from database import extrai_banco
# Importar os dados pessoais (usuario, senha, hospedagem e database)
import data_database as bd

# Criar instância da classe do fastapi
api = FastAPI(debug=True)

# Extrai os dados pessoais do banco de dados
usuario, senha, hospedagem, nome_db = bd.dados() 

# Conexão com o banco de dados - utiliza os dados pessoais como entrada
conexao_bd = extrai_banco(usuario, senha, hospedagem, nome_db)

# Variavel tabela_alunos que armazena a tabela alunos extraída do banco de dados 
tabela_alunos = conexao_bd.extrair_tabela_alunos()

# Cria uma classe para definir os planos
class Defini_planos(str, Enum):
    premium = 'Premium'
    gold = 'Gold'
    basic = 'Basic'

# Validação dos dados da tabela alunos (Pydantic)
class Valida_alunos(BaseModel):
    nome: str = Field(max_length=50)
    data_nascimento: date
    genero: str = Field(max_length=20)
    telefone: str = Field(max_length=20)
    cpf: str = Field(min_length=11, max_length=11, description='Digite apenas os números do cpf')
    email: EmailStr = Field(max_length=255)
    data_matricula: date
    plano: Defini_planos = Field(description='Escolha um dos planos: Premium, Gold e Basic') # Ele aceita apenas Premium, Gold e Basic
    status: str = Field(max_length=8)

# Validação dos dados da tabela alunos (Pydantic)
class Valida_checkin(BaseModel):
        id_aluno: int
        checkin: datetime = Field(default_factory=datetime.now())
        checkout: Optional[datetime] = None

@api.post('/alunos/registro')
async def registrar_aluno(aluno: Valida_alunos):
    # Criar variável que recebe query para pegar o id_plano
    query_selecionaIdPlano = text("SELECT id_plano FROM planos WHERE plano = :tipos_planos") 
    try: 
        with conexao_bd.conecta_banco.begin() as conecta:
            # Executa a query para pegar o id_plano ao invés de plano (Premium, Gold ou Basic)
            id_plano = conecta.execute(query_selecionaIdPlano, {"tipos_planos": aluno.plano}).scalar()
            # Query que vai inserir os dados do aluno
            query_registrarAluno = text("INSERT INTO alunos (nome, data_nascimento, genero, telefone, cpf, email, data_matricula, id_plano, status) VALUES (:nome, :data_nascimento, :genero, :telefone, :cpf, :email, :data_matricula, :id_plano, :status)")
            # Executa a query no banco para inserir os dados dos alunos
            conecta.execute(query_registrarAluno,
                {
                "nome": aluno.nome, 
                "data_nascimento": aluno.data_nascimento, 
                "genero": aluno.genero, 
                "telefone": aluno.telefone,
                "cpf": aluno.cpf,
                "email": aluno.email,
                "data_matricula": aluno.data_matricula,
                "id_plano": id_plano,
                "status": aluno.status
                }
            )
    except:
        # Se der algum problema ao inserir os dados dos aluno realiza rollback
        conecta.rollback()
        raise

@api.post('/aluno/checkin')
async def registrar_checkin(checkin: Valida_checkin):
     try:
        with conexao_bd.conecta_banco.begin() as conecta:
            # Query para verificar se o id_aluno está cadastrado
            query_verificaidAluno = text("SELECT id_aluno FROM alunos WHERE id_aluno = :id_aluno")
            
            # Verificar se o id_aluno está cadastrado no banco de dados
            verificar_idaluno = conecta.execute(query_verificaidAluno,
            {
            'id_aluno': checkin.id_aluno,
            }).fetchone()

            #Se o aluno não estiver cadastrado, ocorre erro
            if not verificar_idaluno:
                raise HTTPException(status_code=404, detail="Aluno não encontrado.")
            
            
            #Query para verificar se há alguma entrada (checkin) sem saída
            query_verificaCheckout = text("SELECT id_checkin FROM checkins WHERE id_aluno = :id_aluno AND checkout IS NULL ORDER BY checkin DESC LIMIT 1")

            # Verificar se há algum registro no checkout dentro do banco de dados
            banco_verificaCheckout = conecta.execute(query_verificaCheckout,
            {
            'id_aluno': checkin.id_aluno,
            }).fetchone()
            
            
            # Se não houver registro, ele realizar a inserção
            if banco_verificaCheckout:
                query_registrarCheckout = text('UPDATE checkins SET checkout = :checkout WHERE id_checkin = :id_checkin ')
                conecta.execute(query_registrarCheckout,
                    {
                    'id_checkin': banco_verificaCheckout[0],
                    'checkout': datetime.now()
                    })
                    
            else:
                query_registroCheckin = text("INSERT INTO checkins (id_aluno, checkin) VALUES (:id_aluno, :checkin)")        

                # Se o aluno estiver cadastrado, realiza o registro do checkin
                conecta.execute(query_registroCheckin,
                {
                'id_aluno': checkin.id_aluno,
                'checkin': checkin.checkin
                })

     except Exception as e:
        conecta.rollback()
        raise HTTPException(status_code=500, detail='Algo deu errado no cadastro! Tente novamente.')

'''@api.get('/aluno/{id}/frequencia')
async def verifica_frequenciaAluno(id: int):
    # Verificação se o id_aluno existe 
    with conexao_bd.conecta_banco.connect() as conecta:
        query_verificaidAluno = text("SELECT id_aluno FROM alunos WHERE id_aluno = :id_aluno")
        verificar_idaluno = conecta.execute(query_verificaidAluno,
            {
            'id_aluno': id,
            }).fetchone()
        
        if not verificar_idaluno:
            raise HTTPException(status_code=500, detail=f'Aluno não encontrado!')
'''