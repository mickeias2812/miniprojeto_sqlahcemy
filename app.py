from flask import Flask, render_template, request, redirect, url_for, flash
import mysql.connector

app = Flask(__name__)
app.secret_key = "MEGA_SUPER_DIFICIL"  # para mensagens flash

# Configuração do MySQL
db_config = {
    'host':'localhost',
    'user':'root',
    'password':'SUA_SENHA',
    'database':'db_trabalho3B'
}

def get_db_connection():
    return mysql.connector.connect(**db_config)


@app.route('/autores/adicionar', methods=['GET','POST'])
def adicionar_autor():
    if request.method == 'POST':
        nome = request.form['nome']
        nac = request.form['nacionalidade']
        data = request.form['data']
        bio = request.form['biografia']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Autores (Nome_autor, Nacionalidade, Data_nascimento, Biografia) VALUES (%s,%s,%s,%s)",
                       (nome, nac, data, bio))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Autor adicionado!', 'success')
        return redirect(url_for('listar_autores'))
    return render_template('autores/adicionar.html')

@app.route('/autores')
def listar_autores():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Autores")
    autores = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('autores/listar.html', autores=autores)

@app.route('/autores/editar/<int:id>', methods=['GET','POST'])
def editar_autor(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Autores WHERE ID_autor=%s", (id,))
    autor = cursor.fetchone()
    if request.method == 'POST':
        nome = request.form['nome']
        nac = request.form['nacionalidade']
        data = request.form['data']
        bio = request.form['biografia']
        cursor.execute("""
            UPDATE Autores SET Nome_autor=%s, Nacionalidade=%s, Data_nascimento=%s, Biografia=%s
            WHERE ID_autor=%s
        """, (nome, nac, data, bio, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Autor atualizado!', 'success')
        return redirect(url_for('listar_autores'))
    cursor.close()
    conn.close()
    return render_template('autores/editar.html', autor=autor)


@app.route('/autores/excluir/<int:id>')
def excluir_autor(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Autores WHERE ID_autor=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Autor excluído!', 'info')
    return redirect(url_for('listar_autores'))

@app.route('/generos')
def listar_generos():
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Generos")
    generos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('generos/listar.html', generos=generos)

@app.route('/generos/adicionar', methods=['GET','POST'])
def adicionar_genero():
    if request.method == 'POST':
        nome = request.form['nome']
        conn = get_db_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Generos (Nome_genero) VALUES (%s)", (nome,))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Gênero adicionado!', 'success')
        return redirect(url_for('listar_generos'))
    return render_template('generos/adicionar.html')

@app.route('/generos/editar/<int:id>', methods=['GET','POST'])
def editar_genero(id):
    conn = get_db_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Generos WHERE ID_genero=%s", (id,))
    genero = cursor.fetchone()
    if request.method == 'POST':
        nome = request.form['nome']
        cursor.execute("UPDATE Generos SET Nome_genero=%s WHERE ID_genero=%s", (nome,id))
        conn.commit()
        cursor.close()
        conn.close()
        flash('Gênero atualizado!', 'success')
        return redirect(url_for('listar_generos'))
    cursor.close()
    conn.close()
    return render_template('generos/editar.html', genero=genero)

@app.route('/generos/excluir/<int:id>')
def excluir_genero(id):
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Generos WHERE ID_genero=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash('Gênero excluído!', 'info')
    return redirect(url_for('listar_generos'))

# -------------------- EDITORAS --------------------
# Funcionalidade CRUD igual (listar, adicionar, editar, excluir)
# -------------------- LIVROS --------------------
# Funcionalidade CRUD igual (usar joins para exibir autor, gênero, editora)
# -------------------- USUÁRIOS --------------------
# Funcionalidade CRUD igual (nome, email, telefone, data, multa)
# -------------------- EMPRÉSTIMOS --------------------
# Funcionalidade CRUD igual (select com join para exibir livro e usuário)

# Para cada tabela, você replica o mesmo padrão: listar, adicionar, editar, excluir.

if __name__ == '__main__':
    app.run(debug=True)