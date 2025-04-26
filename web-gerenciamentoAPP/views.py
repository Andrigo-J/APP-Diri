from app import app
from flask import render_template, request, redirect, url_for, flash
from pymongo import MongoClient
from flask_login import login_required, logout_user, UserMixin, login_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
# Initialize MongoDB client and define the collection
client = MongoClient('mongodb://localhost:27017/')
db = client['your_database_name']  # Replace 'your_database_name' with your database name
usuarios_collection = db['usuarios']  # Replace 'usuarios' with your collection name

class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])
        self.username = user_data['username']

@app.route('/home.html')
def home_page():
    return render_template('home.html')

@app.route('/cadastro', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if usuarios_collection.find_one({'username': username}):
            flash("Nome de usuário já existe. Escolha outro.")
            return redirect(url_for('cadastro'))

        hashed_pw = generate_password_hash(password)
        usuarios_collection.insert_one({
            'username': username,
            'password_hash': hashed_pw
        })
        flash("Cadastro realizado com sucesso! Faça login.")
        return redirect(url_for('login'))

    return render_template('cadastro.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        user_data = usuarios_collection.find_one({'username': username})

        if user_data and check_password_hash(user_data['password_hash'], password):
            user = User(user_data)
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Usuário ou senha inválidos')

    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/clientes.html')
@login_required
def clientes_page():
    return render_template('clientes.html')

@app.route('/financeiro.html')
@login_required
def financeiro_page():
    return render_template('financeiro.html')

@app.route('/produtos.html')
@login_required
def produtos_page():
    return render_template('produtos.html')

@app.route('/login.html')
@login_required
def login_page():
    return render_template('login.html')

@app.route('/estoque.html')
@login_required
def estoque_page():
    return render_template('estoque.html')