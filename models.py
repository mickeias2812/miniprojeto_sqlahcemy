import mysql.connector

# Configuração do banco
db_config = {
    'host': 'localhost',
    'user': 'root',
    'password': 'SENHA_DO_MYSQL',  # 🔹 coloque sua senha
    'database': 'db_trabalho3B'
}

def get_connection():
    return mysql.connector.connect(**db_config)

# ======================
# 📚 LIVROS
# ======================

def listar_livros():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Livros")
    livros = cursor.fetchall()
    cursor.close()
    conn.close()
    return livros

def adicionar_livro(titulo, isbn, ano, qtd):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Livros (Titulo, ISBN, Ano_publicacao, Quantidade_disponivel)
        VALUES (%s, %s, %s, %s)
    """, (titulo, isbn, ano, qtd))
    conn.commit()
    cursor.close()
    conn.close()

# ======================
# 👤 USUÁRIOS
# ======================

def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return usuarios

def adicionar_usuario(nome, email, telefone, data_inscricao, multa_atual=0.0):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("""
        INSERT INTO Usuarios (Nome_usuario, Email, Numero_telefone, Data_inscricao, Multa_atual)
        VALUES (%s, %s, %s, %s, %s)
    """, (nome, email, telefone, data_inscricao, multa_atual))
    conn.commit()
    cursor.close()
    conn.close()
