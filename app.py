from flask import Flask, render_template, request, url_for, redirect
import sqlite3

app = Flask(__name__)
PATH = 'fabrica.db'

def get_db():
    conn = sqlite3.connect(PATH)
    conn.row_factory = sqlite3.Row
    return conn

def start_db():
    db = get_db()
    with open('schema.sql') as f:
        db.executescript(f.read())
    db.commit()
    db.close()

@app.route('/')
def index():
    db = get_db()
    alunos = db.execute('SELECT * FROM aluno').fetchall()
    db.close()
    return render_template('index.html', alunos=alunos)

@app.route('/add', methods=('GET', 'POST'))
def cadastro():
    if request.method == 'POST':
        nome = request.form['nome']
        idade = request.form['idade']
        curso = request.form['curso']

        db = get_db()
        db.execute('INSERT INTO aluno (nome, idade, curso) VALUES (?, ?, ?)', (nome, idade, curso))
        db.commit()
        db.close()
        return redirect(url_for('index'))

    return render_template('cadastro.html')

if __name__ == '__main__':
    start_db()
    app.run(debug=True)
