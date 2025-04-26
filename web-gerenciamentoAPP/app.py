# Importar as bibliotecas necessárias
from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from bson import ObjectId
from pymongo import MongoClient
import os

# Inicialização do Flask
app = Flask(__name__)
app.secret_key = 'Megamind2.0'  # Chave secreta da sessão

# Conectando ao MongoDB
client = MongoClient("mongodb://localhost:27017/")
db = client['gerenciador_app']

# Coleções do MongoDB
usuarios_collection = db['usuarios']
produtos_collection = db['produtos']
clientes_collection = db['clientes']
contas_collection = db['contas']

#Cria o Usuário admin com senha 1234 se não existir
if not usuarios_collection.find_one({"username": "admin"}):
    usuarios_collection.insert_one({
        "username": "admin",
        "password_hash": generate_password_hash("1234")
    })

# Configuração do Flask-Login
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'  # Rota para onde será redirecionado se não estiver logado

# Classe de usuário
class User(UserMixin):
    def __init__(self, user_data):
        self.id = str(user_data['_id'])  # ID do Mongo
        self.username = user_data['username']

@login_manager.user_loader
def load_user(user_id):
    user_data = usuarios_collection.find_one({"_id": ObjectId(user_id)})
    if user_data:
        return User(user_data)
    return None

# Página inicial
@app.route('/')
def index():
    return render_template('home.html')

# Importa as rotas das views (crie o arquivo views.py para organizar seu código)
try:
    from views import *
except ImportError:
    pass  # Só evita erro se o arquivo ainda não existir

# Roda o app
if __name__ == '__main__':
    app.run(debug=True)
