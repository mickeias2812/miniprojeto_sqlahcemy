CREATE DATABASE IF NOT EXISTS db_trabalho3B;
USE db_trabalho3B;

CREATE TABLE Autores (
    ID_autor INT AUTO_INCREMENT PRIMARY KEY,
    Nome_autor VARCHAR(100),
    Nacionalidade VARCHAR(50),
    Data_nascimento DATE,
    Biografia TEXT
);

CREATE TABLE Generos (
    ID_genero INT AUTO_INCREMENT PRIMARY KEY,
    Nome_genero VARCHAR(50)
);

CREATE TABLE Editoras (
    ID_editora INT AUTO_INCREMENT PRIMARY KEY,
    Nome_editora VARCHAR(100),
    Endereco_editora TEXT
);

CREATE TABLE Livros (
    ID_livro INT AUTO_INCREMENT PRIMARY KEY,
    Titulo VARCHAR(150),
    Autor_id INT,
    ISBN VARCHAR(30),
    Ano_publicacao INT,
    Genero_id INT,
    Editora_id INT,
    Quantidade_disponivel INT,
    Resumo TEXT,
    FOREIGN KEY (Autor_id) REFERENCES Autores(ID_autor),
    FOREIGN KEY (Genero_id) REFERENCES Generos(ID_genero),
    FOREIGN KEY (Editora_id) REFERENCES Editoras(ID_editora)
);

CREATE TABLE Usuarios (
    ID_usuario INT AUTO_INCREMENT PRIMARY KEY,
    Nome_usuario VARCHAR(100),
    Email VARCHAR(100),
    Numero_telefone VARCHAR(20),
    Data_inscricao DATE,
    Multa_atual DECIMAL(10,2)
);

CREATE TABLE Emprestimos (
    ID_emprestimo INT AUTO_INCREMENT PRIMARY KEY,
    Usuario_id INT,
    Livro_id INT,
    Data_emprestimo DATE,
    Data_devolucao_prevista DATE,
    Status_emprestimo VARCHAR(20),
    FOREIGN KEY (Usuario_id) REFERENCES Usuarios(ID_usuario),
    FOREIGN KEY (Livro_id) REFERENCES Livros(ID_livro)
);
