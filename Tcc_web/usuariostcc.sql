CREATE DATABASE tcc;

USE tcc;

CREATE TABLE usuarios (
id INT AUTO_INCREMENT PRIMARY KEY,
nome VARCHAR(100),
email VARCHAR(100) UNIQUE,
senha VARCHAR(255),
telefone VARCHAR(20),
cep VARCHAR(10),
bairro VARCHAR(100),
endereco VARCHAR(150)
);


CREATE TABLE denuncia (
id INT AUTO_INCREMENT PRIMARY KEY,
categoria VARCHAR(100),
bairro VARCHAR(100),
descricao TEXT,
foto VARCHAR(255),
data_ocorrencia DATE,
anonimo TINYINT(1) DEFAULT 0,
usuario_id INT NULL,

status ENUM('Em andamento', 'Solucionada') DEFAULT 'Em andamento',
protocolo VARCHAR(20) UNIQUE,
data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);


INSERT INTO denuncia 
(categoria, bairro, descricao, foto, data_ocorrencia, anonimo, usuario_id, status, protocolo)
VALUES 
(
'Roubo',
'Centro',
'Assalto próximo ao mercado',
NULL,
'2026-08-03',
1,
NULL,
'Em andamento',
'DEN-2026-1234'
);