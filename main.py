from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3 as sql

app = Flask(__name__, template_folder='templates')
app.secret_key = "admin123"  # Chave secreta para sessões

# Função para conectar ao banco de dados
def connect_db():
    return sql.connect('form_db.db')

# Rota para página de login
@app.route('/')
def login():
    return render_template('loginn.html')

# Rota para processar o formulário de login
@app.route('/login', methods=["POST", "GET"])
def login_process():
    tplog = request.form['tplog']
    username = request.form['User']
    password = request.form['senha']

    conn = connect_db()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios WHERE tplog=? AND username=? AND password=?", (tplog, username, password))
    user = cursor.fetchone()
    conn.close()

    if user:
        session['username'] = username
        session['tplog'] = tplog
        if tplog == 'Admin':
            return redirect('/admin_page')
        elif tplog == 'Advogado':
            return redirect('/admin_page')
        elif tplog == 'Cliente':
            return redirect('/cliente_page')
    else:
        flash("Acesso negado, redirecionando para a página de login em 5 segundos.", "danger")
        return render_template('redirect.html', login=url_for('login'), delay=5)

# Rota para logout
@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('tplog', None)
    flash("Você foi desconectado", "success")
    return redirect(url_for('login'))

# Rotas para páginas específicas após o login
@app.route('/admin_page')
def admin_page():
    if 'username' in session and session['tplog'] in ['Admin', 'Advogado']:
        con = connect_db()
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
        cur.execute("SELECT * FROM casos")
        casos = cur.fetchall()
        cur.execute("SELECT * FROM atividades")
        atividades = cur.fetchall()
        cur.execute("SELECT * FROM despesas")
        despesas = cur.fetchall()
        cur.execute("SELECT * FROM avaliacoes")
        avaliacoes = cur.fetchall()
        return render_template("admin_page.html", datas=data, casos=casos, atividades=atividades, despesas=despesas, avaliacoes=avaliacoes)
    else:
        flash("Acesso negado, redirecionando para a página de login em 5 segundos.", "danger")
        return render_template('redirect.html', target=url_for('login'), delay=5)

@app.route('/advogado_page')
def advogado_page():
    if 'username' in session and session['tplog'] == 'Advogado':
        con = connect_db()
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
        cur.execute("SELECT * FROM casos")
        casos = cur.fetchall()
        cur.execute("SELECT * FROM atividades")
        atividades = cur.fetchall()
        cur.execute("SELECT * FROM despesas")
        despesas = cur.fetchall()
        cur.execute("SELECT * FROM avaliacoes")
        avaliacoes = cur.fetchall()
        return render_template("advogado_page.html", datas=data, casos=casos, atividades=atividades, despesas=despesas, avaliacoes=avaliacoes)
    else:
        flash("Acesso negado, redirecionando para a página de login em 5 segundos.", "danger")
        return render_template('redirect.html', target=url_for('login'), delay=5)

@app.route('/cliente_page')
def cliente_page():
    if 'username' in session and session['tplog'] == 'Cliente':
        con = connect_db()
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("SELECT * FROM users")
        data = cur.fetchall()
        cur.execute("SELECT * FROM casos")
        casos = cur.fetchall()
        cur.execute("SELECT * FROM atividades")
        atividades = cur.fetchall()
        cur.execute("SELECT * FROM despesas")
        despesas = cur.fetchall()
        cur.execute("SELECT * FROM avaliacoes")
        avaliacoes = cur.fetchall()
        return render_template("cliente_page.html", datas=data, casos=casos, atividades=atividades, despesas=despesas, avaliacoes=avaliacoes)
    else:
        flash("Acesso negado, redirecionando para a página de login em 5 segundos.", "danger")
        return render_template('redirect.html', target=url_for('login'), delay=5)

@app.route("/add_user", methods=["POST", "GET"])
def add_user():
    if 'username' in session and (session['tplog'] == 'Admin' or session['tplog'] == 'Advogado'):
        if request.method == "POST":
            nome = request.form["nome"]
            idade = request.form["idade"]
            rua = request.form["rua"]
            cidade = request.form["cidade"]
            numero = request.form["numero"]
            estado = request.form["estado"]
            email = request.form["email"]
            
            # Dados do caso
            caso_cliente = request.form["caso_cliente"]
            caso_tipo = request.form["caso_tipo"]
            caso_datas = request.form["caso_datas"]
            caso_detalhes = request.form["caso_detalhes"]
            caso_partes = request.form["caso_partes"]
            
            # Dados das atividades
            atividade_descricao = request.form["atividade_descricao"]
            atividade_data = request.form["atividade_data"]
            
            # Dados das despesas
            despesa_tipo = request.form["despesa_tipo"]
            despesa_descricao = request.form["despesa_descricao"]
            despesa_valor = request.form["despesa_valor"]
            
            # Dados da avaliação
            avaliacao_descricao = request.form["avaliacao_descricao"]
            avaliacao_data = request.form["avaliacao_data"]
            avaliacao_status = request.form["avaliacao_status"]
            avaliacao_passos = request.form["avaliacao_passos"]
            
            con = connect_db()
            cur = con.cursor()
            cur.execute("INSERT INTO users (NOME, IDADE, RUA, CIDADE, NUMERO, ESTADO, EMAIL) VALUES (?, ?, ?, ?, ?, ?, ?)", (nome, idade, rua, cidade, numero, estado, email))
            user_id = cur.lastrowid
            
            cur.execute("INSERT INTO casos (CLIENTE_ID, CLIENTE, TIPO, DATAS, DETALHES, PARTES) VALUES (?, ?, ?, ?, ?, ?)", (user_id, caso_cliente, caso_tipo, caso_datas, caso_detalhes, caso_partes))
            cur.execute("INSERT INTO atividades (CLIENTE_ID, DESCRICAO, DATA) VALUES (?, ?, ?)", (user_id, atividade_descricao, atividade_data))
            cur.execute("INSERT INTO despesas (CLIENTE_ID, TIPO, DESCRICAO, VALOR) VALUES (?, ?, ?, ?)", (user_id, despesa_tipo, despesa_descricao, despesa_valor))
            cur.execute("INSERT INTO avaliacoes (CLIENTE_ID, DESCRICAO, DATA, STATUS, PASSOS) VALUES (?, ?, ?, ?, ?)", (user_id, avaliacao_descricao, avaliacao_data, avaliacao_status, avaliacao_passos))
            
            con.commit()
            flash("Dados cadastrados", "success")
            return redirect(url_for("admin_page"))
        return render_template("add_user.html")
    else:
        flash("Acesso negado, redirecionando para a página anterior em 5 segundos.", "danger")
        return render_template('redirect2.html', target=url_for('admin_page'), delay=5)

@app.route("/edit_user/<int:id>", methods=["POST", "GET"])
def edit_user(id):
    if 'username' in session and (session['tplog'] == 'Admin' or session['tplog'] == 'Advogado'):
        con = connect_db()
        con.row_factory = sql.Row
        cur = con.cursor()
        
        if request.method == "POST":
            nome = request.form["nome"]
            idade = request.form["idade"]
            rua = request.form["rua"]
            cidade = request.form["cidade"]
            numero = request.form["numero"]
            estado = request.form["estado"]
            email = request.form["email"]
            
            # Atualizar dados do usuário
            cur.execute("UPDATE users SET NOME=?, IDADE=?, RUA=?, CIDADE=?, NUMERO=?, ESTADO=?, EMAIL=? WHERE ID=?", (nome, idade, rua, cidade, numero, estado, email, id))
            
            # Atualizar dados do caso
            caso_cliente = request.form["caso_cliente"]
            caso_tipo = request.form["caso_tipo"]
            caso_datas = request.form["caso_datas"]
            caso_detalhes = request.form["caso_detalhes"]
            caso_partes = request.form["caso_partes"]
            cur.execute("UPDATE casos SET CLIENTE=?, TIPO=?, DATAS=?, DETALHES=?, PARTES=? WHERE CLIENTE_ID=?", (caso_cliente, caso_tipo, caso_datas, caso_detalhes, caso_partes, id))
            
            # Atualizar dados das atividades
            atividade_descricao = request.form["atividade_descricao"]
            atividade_data = request.form["atividade_data"]
            cur.execute("UPDATE atividades SET DESCRICAO=?, DATA=? WHERE CLIENTE_ID=?", (atividade_descricao, atividade_data, id))
            
            # Atualizar dados das despesas
            despesa_tipo = request.form["despesa_tipo"]
            despesa_descricao = request.form["despesa_descricao"]
            despesa_valor = request.form["despesa_valor"]
            cur.execute("UPDATE despesas SET TIPO=?, DESCRICAO=?, VALOR=? WHERE CLIENTE_ID=?", (despesa_tipo, despesa_descricao, despesa_valor, id))
            
            # Atualizar dados da avaliação
            avaliacao_descricao = request.form["avaliacao_descricao"]
            avaliacao_data = request.form["avaliacao_data"]
            avaliacao_status = request.form["avaliacao_status"]
            avaliacao_passos = request.form["avaliacao_passos"]
            cur.execute("UPDATE avaliacoes SET DESCRICAO=?, DATA=?, STATUS=?, PASSOS=? WHERE CLIENTE_ID=?", (avaliacao_descricao, avaliacao_data, avaliacao_status, avaliacao_passos, id))
            
            con.commit()
            flash("Dados atualizados", "success")
            return redirect(url_for("admin_page"))
        con = sql.connect("form_db.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from users where ID=?", (id,))
        data = cur.fetchone()
        
        # Obter dados do usuário
        cur.execute("SELECT * FROM users WHERE ID=?", (id,))
        user_data = cur.fetchone()
        
        # Obter dados do caso
        cur.execute("SELECT * FROM casos WHERE CLIENTE_ID=?", (id,))
        caso_data = cur.fetchone()
        
        # Obter dados das atividades
        cur.execute("SELECT * FROM atividades WHERE CLIENTE_ID=?", (id,))
        atividades_data = cur.fetchall()
        
        # Obter dados das despesas
        cur.execute("SELECT * FROM despesas WHERE CLIENTE_ID=?", (id,))
        despesas_data = cur.fetchall()
        
        # Obter dados da avaliação
        cur.execute("SELECT * FROM avaliacoes WHERE CLIENTE_ID=?", (id,))
        avaliacoes_data = cur.fetchall()
        
        return render_template("edit_user.html", datas=data,casos=caso_data, user_data=user_data, caso_data=caso_data, atividades_data=atividades_data, despesas_data=despesas_data, avaliacoes_data=avaliacoes_data)
    else:
        flash("Acesso negado, redirecionando para a página anterior em 5 segundos.", "danger")
        return render_template('redirect2.html', target=url_for('admin_page'), delay=5)

@app.route("/delete_user/<int:id>", methods=["GET"])
def delete_user(id):
    if 'username' in session and session['tplog'] == 'Admin':
        con = connect_db()
        cur = con.cursor()
        cur.execute("DELETE FROM users WHERE ID=?", (id,))
        cur.execute("DELETE FROM casos WHERE CLIENTE_ID=?", (id,))
        cur.execute("DELETE FROM atividades WHERE CLIENTE_ID=?", (id,))
        cur.execute("DELETE FROM despesas WHERE CLIENTE_ID=?", (id,))
        cur.execute("DELETE FROM avaliacoes WHERE CLIENTE_ID=?", (id,))
        con.commit()
        flash("Dados deletados", "warning")
        return redirect(url_for("admin_page"))
    else:
        flash("Acesso negado, redirecionando para a página anterior em 5 segundos.", "danger")
        return render_template('redirect2.html', target=url_for('admin_page'), delay=5)

if __name__ == '__main__':
    app.run(debug=True)
