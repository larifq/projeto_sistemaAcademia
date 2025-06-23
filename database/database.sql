-- Criar o Banco de dados
CREATE DATABASE academia;

-- Criar a tabela de Planos
CREATE TABLE planos (
	id_plano INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- Chave Primária
	plano VARCHAR(20),
	preco NUMERIC(6,2)
);

-- Criar a tabela com os dados dos Alunos
CREATE TABLE alunos(
	id_aluno INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- Chave Primária
	nome VARCHAR(50),
	data_nascimento DATE,
	genero VARCHAR(20),
	telefone VARCHAR(15),
	cpf CHAR(11),
	email VARCHAR(255),
	data_matricula DATE,
	id_plano INT, CONSTRAINT fk_plano FOREIGN KEY (id_plano) REFERENCES planos(id_plano), -- Chave Estrangeira
	status VARCHAR(8)
);

-- Criar tabela para monitorar entrada e saída dos alunos
CREATE TABLE checkins(
	id_checkin INT GENERATED ALWAYS AS IDENTITY PRIMARY KEY, -- Chave Primária
	id_aluno INT, CONSTRAINT fk_aluno FOREIGN KEY (id_aluno) REFERENCES alunos(id_aluno), -- Chave Estrangeira
	checkin TIMESTAMP NOT NULL,
	checkout TIMESTAMP NULL
);

-- inserir o plano Premium no banco de dados planos
INSERT INTO planos (plano, preco) VALUES ('Premium', '450');

-- inserir o plano Gold no banco de dados planos
INSERT INTO planos (plano, preco) VALUES ('Gold', '350');

-- inserir o plano Basic no banco de dados planos
INSERT INTO planos (plano, preco) VALUES ('Basic', '120');
