from flask import Flask, render_template, request, redirect, url_for, flash, session
import sqlite3 as sql

app = Flask(__name__, template_folder='templates')
app.secret_key = "admin123"  # Chave secreta para sessões

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

    # Conectar ao banco de dados SQLite
    conn = sql.connect('usuarios.db')
    cursor = conn.cursor()

    # Consultar o banco de dados para verificar as credenciais
    cursor.execute("SELECT * FROM usuarios WHERE tplog=? AND username=? AND password=?", (tplog, username, password))
    user = cursor.fetchone()

    # Fechar a conexão com o banco de dados
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
    if 'username' in session and session['tplog'] == 'Admin' or 'Advogado':
        con = sql.connect("form_db.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from users")
        data = cur.fetchall()
        return render_template("admin_page.html", datas=data)
    else:
        flash("Acesso negado, redirecionando para a página de login em 5 segundos.", "danger")
        return render_template('redirect.html', target=url_for('login'), delay=5)

@app.route('/advogado_page')
def advogado_page():
    if 'username' in session and session['tplog'] == 'Advogado':
        con = sql.connect("form_db.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from users")
        data = cur.fetchall()
        return render_template("advogado_page.html", datas=data)
    else:
        flash("Acesso negado, redirecionando para a página de login em 5 segundos.", "danger")
        return render_template('redirect.html', target=url_for('login'), delay=5)

@app.route('/cliente_page')
def cliente_page():
    if 'username' in session and session['tplog'] == 'Cliente':
        con = sql.connect("form_db.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from users")
        data = cur.fetchall()
        return render_template("cliente_page.html", datas=data)
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
            con = sql.connect("form_db.db")
            cur = con.cursor()
            cur.execute("insert into users(NOME, IDADE, RUA, CIDADE, NUMERO, ESTADO, EMAIL) values (?, ?, ?, ?, ?, ?, ?)",
                        (nome, idade, rua, cidade, numero, estado, email))
            con.commit()
            flash("Dados cadastrados", "success")
            return redirect(url_for("admin_page"))
        return render_template("add_user.html")
    else:
        flash("Acesso negado, redirecionando para a página anterior em 5 segundos.", "danger")
        return render_template('redirect2.html', target=url_for('admin_page'), delay=5)


@app.route("/edit_user/<string:id>", methods=["POST", "GET"])
def edit_user(id):
    if 'username' in session and (session['tplog'] == 'Admin' or session['tplog'] == 'Advogado'):
        if request.method == "POST":
            nome = request.form["nome"]
            idade = request.form["idade"]
            rua = request.form["rua"]
            cidade = request.form["cidade"]
            numero = request.form["numero"]
            estado = request.form["estado"]
            email = request.form["email"]
            con = sql.connect("form_db.db")
            cur = con.cursor()
            cur.execute("update users set NOME=?, IDADE=?, RUA=?, CIDADE=?, NUMERO=?, ESTADO=?, EMAIL=? where ID=?",
                        (nome, idade, rua, cidade, numero, estado, email, id))
            con.commit()
            flash("Dados atualizados", "success")
            return redirect(url_for("admin_page"))
        con = sql.connect("form_db.db")
        con.row_factory = sql.Row
        cur = con.cursor()
        cur.execute("select * from users where ID=?", (id,))
        data = cur.fetchone()
        return render_template("edit_user.html", datas=data)
    else:
        flash("Acesso negado, redirecionando para a página anterior em 5 segundos.", "danger")
        return render_template('redirect2.html', target=url_for('admin_page'), delay=5)

@app.route("/delete_user/<string:id>", methods=["GET"])
def delete_user(id):
    if 'username' in session and session['tplog'] == 'Admin':
        con = sql.connect("form_db.db")
        cur = con.cursor()
        cur.execute("delete from users where ID=?", (id,))
        con.commit()
        flash("Dados deletados", "warning")
        return redirect(url_for("admin_page"))
    else:
        flash("Acesso negado, redirecionando para a página anterior em 5 segundos.", "danger")
        return render_template('redirect2.html', target=url_for('admin_page'), delay=5)

if __name__ == '__main__':
    app.run(debug=True)
