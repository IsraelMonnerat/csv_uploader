CREATE TABLE users_data (
  id SERIAL PRIMARY KEY,
  nome VARCHAR(100),
  data_nascimento DATE,
  genero VARCHAR(10),
  nacionalidade VARCHAR(50),
  data_criacao DATE,
  data_atualizacao DATE
);