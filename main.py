from flask import Flask, render_template, request, redirect, url_for, flash
import sqlite3 as sql

app = Flask(__name__, template_folder='templates')

# Rota para página de login
@app.route('/')
def login():
    return render_template('loginn.html')


# Rota para processar o formulário de login
@app.route('/login', methods=['POST'])
def login_process():
    tplog = request.form['tplog']
    username = request.form['User']
    password = request.form['senha']

    # Conectar ao banco de dados SQLite
    conn = sql.connect('usuarios.db')
    cursor = conn.cursor()

    # Consultar o banco de dados para verificar as credenciais
    print("Consulta SQL:", "SELECT * FROM usuarios WHERE tplog=? AND username=? AND password=?", (tplog, username, password))
    cursor.execute("SELECT * FROM usuarios WHERE tplog=? AND username=? AND password=?", (tplog, username, password))
    user = cursor.fetchone()
    print("Usuário encontrado:", user)

    # Fechar a conexão com o banco de dados
    conn.close()

    if user:
        if tplog == 'Admin':
            return redirect('/admin_page')
        elif tplog == 'Advogado':
            return redirect('/advogado_page')
        elif tplog == 'Cliente':
            return redirect('/cliente_page')
    else:
        return "Credenciais inválidas"

# Rotas para páginas específicas após o login
@app.route('/admin_page')
def admin_page():
    con = sql.connect("form_db.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from users")
    data=cur.fetchall()
    return render_template ("admin_page.html", datas=data)

@app.route('/advogado_page')
def advogado_page():
    con = sql.connect("form_db.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from users")
    data=cur.fetchall()
    return render_template ("advogado_page.html", datas=data)

@app.route('/cliente_page')
def cliente_page():
    con = sql.connect("form_db.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from users")
    data=cur.fetchall()
    return render_template ("cliente_page.html", datas=data)

def index():
    con = sql.connect("form_db.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from users")
    data=cur.fetchall()
    return render_template ("admin_page.html", datas=data)

@app.route("/add_user", methods=["POST", "GET"])
def add_user():
    if request.method=="POST":
        nome=request.form["nome"]
        idade=request.form["idade"]
        rua=request.form["rua"]
        cidade=request.form["cidade"]
        numero=request.form["numero"]
        estado=request.form["estado"]
        email=request.form["email"]
        con=sql.connect("form_db.db")
        cur=con.cursor()
        cur.execute("insert into users(NOME,IDADE,RUA,CIDADE,NUMERO,ESTADO,EMAIL) values (?,?,?,?,?,?,?)", (nome, idade, rua, cidade, numero, estado, email))
        con.commit()
        flash("Dados cadastrados", "success")
        return redirect(url_for("admin_page"))
    return render_template("add_user.html")

@app.route("/edit_user/<string:id>", methods=["POST","GET"])
def edit_user(id):
    if request.method=="POST":
        nome=request.form["nome"]
        idade=request.form["idade"]
        rua=request.form["rua"]
        cidade=request.form["cidade"]
        numero=request.form["numero"]
        estado=request.form["estado"]
        email=request.form["email"]
        con=sql.connect("form_db.db")
        cur=con.cursor()
        cur.execute("update users set NOME=?,IDADE=?,RUA=?,CIDADE=?,NUMERO=?,ESTADO=?,EMAIL=? where ID=?", (nome,idade,rua,cidade,numero,estado,email,id))
        con.commit()
        flash("Dados atualizados", "success")
        return redirect(url_for("admin_page"))
    con=sql.connect("form_db.db")
    con.row_factory=sql.Row
    cur=con.cursor()
    cur.execute("select * from users where ID =?", (id,))
    data=cur.fetchone()
    return render_template("edit_user.html", datas=data)

@app.route("/delete_user/<string:id>", methods=["GET"])
def delete_user(id):
    con=sql.connect("form_db.db")
    cur=con.cursor()
    cur.execute("delete from users where ID=?", (id,))
    con.commit()
    flash("Dados deletados", "warning")
    return redirect(url_for("add_user"))


if __name__ == '__main__':
    app.secret_key="admin123"
    app.run(debug=True)
