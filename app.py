from flask import Flask, render_template, request, redirect, url_for, flash
from db.connection import get_connection  # seu módulo de conexão

app = Flask(__name__)
app.secret_key = "MEGA_SUPER_DIFICIL"  # para mensagens flash

# -------------------- PÁGINA INICIAL --------------------
@app.route("/")
def index():
    return render_template("base.html")


# -------------------- AUTORES --------------------
@app.route('/autores/adicionar', methods=['GET','POST'])
def adicionar_autor():
    if request.method == 'POST':
        nome = request.form['nome']
        nac = request.form['nacionalidade']
        data = request.form['data_nascimento']
        bio = request.form['biografia']
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(
            "INSERT INTO Autores (Nome_autor, Nacionalidade, Data_nascimento, Biografia) VALUES (%s,%s,%s,%s)",
            (nome, nac, data, bio)
        )
        conn.commit()
        cursor.close()
        conn.close()
        flash('Autor adicionado!', 'success')
        return redirect(url_for('listar_autores'))
    return render_template('autores/adicionar.html')

@app.route('/autores')
def listar_autores():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Autores")
    autores = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('autores/listar.html', autores=autores)

@app.route('/autores/editar/<int:id>', methods=['GET','POST'])
def editar_autor(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Autores WHERE ID_autor=%s", (id,))
    autor = cursor.fetchone()

    if request.method == 'POST':
        nome = request.form['nome']
        nac = request.form['nacionalidade']
        data = request.form['data_nascimento']
        bio = request.form['biografia']
        cursor.execute(
            "UPDATE Autores SET Nome_autor=%s, Nacionalidade=%s, Data_nascimento=%s, Biografia=%s WHERE ID_autor=%s",
            (nome, nac, data, bio, id)
        )
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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Livros WHERE Autor_id=%s", (id,))
    if cursor.fetchone()[0] > 0:
        flash("Não é possível excluir este autor porque ele tem livros cadastrados!", "error")
    else:
        cursor.execute("DELETE FROM Autores WHERE ID_autor=%s", (id,))
        conn.commit()
        flash("Autor excluído!", "info")
    cursor.close()
    conn.close()
    return redirect(url_for('listar_autores'))


# -------------------- GÊNEROS --------------------
@app.route('/generos')
def listar_generos():
    conn = get_connection()
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
        conn = get_connection()
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
    conn = get_connection()
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
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM Livros WHERE Genero_id=%s", (id,))
    if cursor.fetchone()[0] > 0:
        flash("Não é possível excluir este gênero porque existem livros vinculados a ele!", "error")
    else:
        cursor.execute("DELETE FROM Generos WHERE ID_genero=%s", (id,))
        conn.commit()
        flash("Gênero excluído!", "info")
    cursor.close()
    conn.close()
    return redirect(url_for('listar_generos'))


# -------------------- LIVROS --------------------

# Adicionar livro
@app.route('/livros/adicionar', methods=['GET', 'POST'])
def adicionar_livro():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Carregar listas para os selects
    cursor.execute("SELECT * FROM Autores")
    autores = cursor.fetchall()

    cursor.execute("SELECT * FROM Generos")
    generos = cursor.fetchall()

    cursor.execute("SELECT * FROM Editoras")
    editoras = cursor.fetchall()

    if request.method == 'POST':
        titulo = request.form.get('titulo')
        autor_id = request.form.get('autor_id')
        genero_id = request.form.get('genero_id')
        editora_id = request.form.get('editora_id')
        isbn = request.form.get('isbn')
        ano = request.form.get('ano')
        qtd = request.form.get('quantidade')
        resumo = request.form.get('resumo')

        # Função auxiliar para checar FK
        def checar_fk(tabela, coluna, valor):
            cursor.execute(f"SELECT COUNT(*) AS total FROM {tabela} WHERE {coluna}=%s", (valor,))
            resultado = cursor.fetchone()
            return resultado and resultado['total'] > 0

        if not checar_fk("Autores", "ID_autor", autor_id):
            flash("Autor não existe!", "error")
            cursor.close()
            conn.close()
            return redirect(url_for('adicionar_livro'))

        if not checar_fk("Generos", "ID_genero", genero_id):
            flash("Gênero não existe!", "error")
            cursor.close()
            conn.close()
            return redirect(url_for('adicionar_livro'))

        if not checar_fk("Editoras", "ID_editora", editora_id):
            flash("Editora não existe!", "error")
            cursor.close()
            conn.close()
            return redirect(url_for('adicionar_livro'))

        # Inserir livro
        cursor.execute("""
            INSERT INTO Livros (Titulo, Autor_id, ISBN, Ano_publicacao, Genero_id, Editora_id, Quantidade_disponivel, Resumo)
            VALUES (%s,%s,%s,%s,%s,%s,%s,%s)
        """, (titulo, autor_id, isbn, ano, genero_id, editora_id, qtd, resumo))

        conn.commit()
        flash("Livro adicionado!", "success")
        cursor.close()
        conn.close()
        return redirect(url_for('listar_livros'))

    cursor.close()
    conn.close()
    return render_template('livros/adicionar.html', autores=autores, generos=generos, editoras=editoras)

# Listar livros
@app.route('/livros')
def listar_livros():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT Livros.*, 
               Autores.Nome_autor,
               Generos.Nome_genero,
               Editoras.Nome_editora
        FROM Livros
        LEFT JOIN Autores ON Livros.Autor_id = Autores.ID_autor
        LEFT JOIN Generos ON Livros.Genero_id = Generos.ID_genero
        LEFT JOIN Editoras ON Livros.Editora_id = Editoras.ID_editora
    """)
    livros = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('livros/listar.html', livros=livros)

# -------------------- EDITAR LIVRO --------------------
@app.route('/livros/editar/<int:id>', methods=['GET', 'POST'])
def editar_livro(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)

    # Pega o livro que será editado
    cursor.execute("SELECT * FROM Livros WHERE ID_livro=%s", (id,))
    livro = cursor.fetchone()

    # Pega listas para os selects
    cursor.execute("SELECT * FROM Autores")
    autores = cursor.fetchall()

    cursor.execute("SELECT * FROM Generos")
    generos = cursor.fetchall()

    cursor.execute("SELECT * FROM Editoras")
    editoras = cursor.fetchall()

    if request.method == 'POST':
        titulo = request.form['titulo']
        autor_id = request.form['autor_id']
        genero_id = request.form['genero_id']
        editora_id = request.form['editora_id']
        isbn = request.form['isbn']
        ano = request.form['ano']
        qtd = request.form['quantidade']
        resumo = request.form['resumo']

        # Atualiza o livro
        cursor.execute("""
            UPDATE Livros SET
                Titulo=%s, Autor_id=%s, ISBN=%s, Ano_publicacao=%s,
                Genero_id=%s, Editora_id=%s, Quantidade_disponivel=%s, Resumo=%s
            WHERE ID_livro=%s
        """, (titulo, autor_id, isbn, ano, genero_id, editora_id, qtd, resumo, id))

        conn.commit()
        cursor.close()
        conn.close()
        flash("Livro atualizado com sucesso!", "success")
        return redirect(url_for('listar_livros'))

    cursor.close()
    conn.close()
    return render_template('livros/editar.html', livro=livro, autores=autores, generos=generos, editoras=editoras)


# -------------------- EXCLUIR LIVRO --------------------
@app.route('/livros/excluir/<int:id>')
def excluir_livro(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Livros WHERE ID_livro=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Livro excluído com sucesso!", "info")
    return redirect(url_for('listar_livros'))


# -------------------- EDITORAS --------------------
@app.route('/editoras/adicionar', methods=['GET', 'POST'])
def adicionar_editora():
    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("INSERT INTO Editoras (Nome_editora, Endereco_editora) VALUES (%s, %s)", 
                       (nome, endereco))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Editora adicionada!", "success")
        return redirect(url_for('listar_editoras'))
    return render_template('editoras/adicionar.html')

@app.route('/editoras')
def listar_editoras():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Editoras")
    editoras = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('editoras/listar.html', editoras=editoras)


@app.route('/editoras/editar/<int:id>', methods=['GET','POST'])
def editar_editora(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Editoras WHERE ID_editora=%s", (id,))
    editora = cursor.fetchone()

    if request.method == 'POST':
        nome = request.form['nome']
        endereco = request.form['endereco']
        cursor.execute("UPDATE Editoras SET Nome_editora=%s, Endereco_editora=%s WHERE ID_editora=%s",
                       (nome, endereco, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Editora atualizada!", "success")
        return redirect(url_for('listar_editoras'))

    cursor.close()
    conn.close()
    return render_template('editoras/editar.html', editora=editora)

@app.route('/editoras/excluir/<int:id>')
def excluir_editora(id):
    conn = get_connection()
    cursor = conn.cursor()
    # Verifica se existem livros vinculados à editora
    cursor.execute("SELECT COUNT(*) FROM Livros WHERE Editora_id=%s", (id,))
    if cursor.fetchone()[0] > 0:
        flash("Não é possível excluir esta editora porque existem livros vinculados a ela!", "error")
    else:
        cursor.execute("DELETE FROM Editoras WHERE ID_editora=%s", (id,))
        conn.commit()
        flash("Editora excluída!", "info")
    cursor.close()
    conn.close()
    return redirect(url_for('listar_editoras'))


# -------------------- USUÁRIOS --------------------
@app.route('/usuarios')
def listar_usuarios():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Usuarios")
    usuarios = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('usuarios/listar.html', usuarios=usuarios)

@app.route('/usuarios/adicionar', methods=['GET','POST'])
def adicionar_usuario():
    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        data = request.form['data']
        multa = request.form['multa']

        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute("""
            INSERT INTO Usuarios (Nome_usuario, Email, Numero_telefone, Data_inscricao, Multa_atual)
            VALUES (%s,%s,%s,%s,%s)
        """, (nome, email, telefone, data, multa))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Usuário adicionado!", "success")
        return redirect(url_for('listar_usuarios'))

    return render_template('usuarios/adicionar.html')

@app.route('/usuarios/editar/<int:id>', methods=['GET','POST'])
def editar_usuario(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Usuarios WHERE ID_usuario = %s", (id,))
    usuario = cursor.fetchone()

    if not usuario:
        flash("Usuário não encontrado!", "error")
        cursor.close()
        conn.close()
        return redirect(url_for('listar_usuarios'))

    if request.method == 'POST':
        nome = request.form['nome']
        email = request.form['email']
        telefone = request.form['telefone']
        data = request.form['data']
        multa = request.form['multa']

        cursor.execute("""
            UPDATE Usuarios
            SET Nome_usuario=%s, Email=%s, Numero_telefone=%s, Data_inscricao=%s, Multa_atual=%s
            WHERE ID_usuario=%s
        """, (nome, email, telefone, data, multa, id))
        conn.commit()
        flash("Usuário atualizado com sucesso!", "success")
        cursor.close()
        conn.close()
        return redirect(url_for('listar_usuarios'))

    cursor.close()
    conn.close()
    return render_template("usuarios/editar.html", usuario=usuario)

@app.route('/usuarios/excluir/<int:id>')
def excluir_usuario(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Usuarios WHERE ID_usuario=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Usuário excluído!", "info")
    return redirect(url_for('listar_usuarios'))


# -------------------- EMPRÉSTIMOS --------------------
@app.route('/emprestimos')
def listar_emprestimos():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("""
        SELECT Emprestimos.*, Usuarios.Nome_usuario, Livros.Titulo
        FROM Emprestimos
        LEFT JOIN Usuarios ON Emprestimos.Usuario_id = Usuarios.ID_usuario
        LEFT JOIN Livros ON Emprestimos.Livro_id = Livros.ID_livro
    """)
    emprestimos = cursor.fetchall()
    cursor.close()
    conn.close()
    return render_template('emprestimos/listar.html', emprestimos=emprestimos)

@app.route('/emprestimos/adicionar', methods=['GET','POST'])
def adicionar_emprestimo():
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Usuarios")
    usuarios = cursor.fetchall()
    cursor.execute("SELECT * FROM Livros")
    livros = cursor.fetchall()
    cursor.close()
    conn.close()

    if request.method == 'POST':
        usuario = request.form['usuario']
        livro = request.form['livro']
        data_emp = request.form['data_emprestimo']
        data_prev = request.form['data_prevista']
        status = request.form['status']

        conn2 = get_connection()
        cursor2 = conn2.cursor()
        cursor2.execute("""
            INSERT INTO Emprestimos (Usuario_id, Livro_id, Data_emprestimo, Data_devolucao_prevista, Status_emprestimo)
            VALUES (%s,%s,%s,%s,%s)
        """, (usuario, livro, data_emp, data_prev, status))
        conn2.commit()
        cursor2.close()
        conn2.close()
        flash("Empréstimo adicionado!", "success")
        return redirect(url_for('listar_emprestimos'))

    return render_template('emprestimos/adicionar.html', usuarios=usuarios, livros=livros)


@app.route('/emprestimos/editar/<int:id>', methods=['GET','POST'])
def editar_emprestimo(id):
    conn = get_connection()
    cursor = conn.cursor(dictionary=True)
    cursor.execute("SELECT * FROM Emprestimos WHERE ID_emprestimo=%s", (id,))
    emprestimo = cursor.fetchone()

    cursor.execute("SELECT * FROM Usuarios")
    usuarios = cursor.fetchall()

    cursor.execute("SELECT * FROM Livros")
    livros = cursor.fetchall()

    if request.method == 'POST':
        usuario_id = request.form['usuario']
        livro_id = request.form['livro']
        data_emp = request.form['data_emprestimo']
        data_prev = request.form['data_prevista']
        status = request.form['status']

        cursor.execute("""
            UPDATE Emprestimos SET Usuario_id=%s, Livro_id=%s, 
            Data_emprestimo=%s, Data_devolucao_prevista=%s, Status_emprestimo=%s
            WHERE ID_emprestimo=%s
        """, (usuario_id, livro_id, data_emp, data_prev, status, id))
        conn.commit()
        cursor.close()
        conn.close()
        flash("Empréstimo atualizado!", "success")
        return redirect(url_for('listar_emprestimos'))

    cursor.close()
    conn.close()
    return render_template("emprestimos/editar.html", emprestimo=emprestimo, usuarios=usuarios, livros=livros)

@app.route('/emprestimos/excluir/<int:id>')
def excluir_emprestimo(id):
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("DELETE FROM Emprestimos WHERE ID_emprestimo=%s", (id,))
    conn.commit()
    cursor.close()
    conn.close()
    flash("Empréstimo excluído!", "info")
    return redirect(url_for('listar_emprestimos'))


if __name__ == '__main__':
    app.run(debug=True)
