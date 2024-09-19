from flask import Flask, request, jsonify, session, redirect, url_for
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
import latex2sympy2 as latex2sympy
import os
import logging
import base64
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.secret_key = os.urandom(24)  # Chave secreta para a sessão

# Configurar o logger
logging.basicConfig(level=logging.INFO)

# Simulação de banco de dados em memória (você pode substituir por um banco de dados real)
users_db = {}

def calcular_expressao(expressao):
    try:
        # Log da expressão recebida
        logging.info(f"Expressão recebida: {expressao}")
        
        # Remover caracteres de início e fim indesejados (como $ ou \(...\))
        expressao = expressao.strip()
        if expressao.startswith('$$') and expressao.endswith('$$'):
            expressao = expressao[2:-2]
        elif expressao.startswith('$') and expressao.endswith('$'):
            expressao = expressao[1:-1]
        elif expressao.startswith('\\(') and expressao.endswith('\\)'):
            expressao = expressao[2:-2]
        logging.info(f"Expressão após remover delimitadores: {expressao}")

        # Tentar processar como expressão SymPy normal
        try:
            sympy_expr = parse_expr(expressao, transformations='all')
        except:
            # Se falhar, tentar processar como LaTeX
            sympy_expr = latex2sympy.latex2sympy(expressao)

        logging.info(f"Expressão convertida para SymPy: {sympy_expr}")

        # Avaliar a expressão
        resultado = sympy_expr.evalf() if sympy_expr.is_Number else sp.simplify(sympy_expr)
        logging.info(f"Resultado da expressão: {resultado}")

        return resultado
    except Exception as e:
        logging.error(f"Erro ao processar a expressão: {str(e)}")
        return f"Erro ao processar a expressão: {str(e)}"

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route('/calcular', methods=['POST'])
def calcular():
    dados = request.json
    expressao = dados.get('expressao', '')

    # Log da entrada original
    logging.info(f"Entrada original recebida: {dados}")

    if not expressao:
        return jsonify({'erro': 'Nenhuma expressão fornecida'}), 400

    try:
        # Processar a expressão
        resultado = calcular_expressao(expressao)
        return jsonify({'resultado': str(resultado)})
    except Exception as e:
        logging.error(f"Erro ao processar a expressão: {str(e)}")
        return jsonify({'erro': f'Erro ao processar a expressão: {str(e)}'}), 500

# Rota para registro
@app.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    if not username or not password:
        return jsonify({"error": "Nome de usuário e senha são obrigatórios"}), 400

    if username in users_db:
        return jsonify({"error": "Usuário já existe"}), 400

    # Hash da senha para armazená-la de forma segura
    hashed_password = generate_password_hash(password)
    users_db[username] = hashed_password

    return jsonify({"message": "Usuário registrado com sucesso"}), 200

# Rota para login
@app.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data.get('username')
    password = data.get('password')

    # Verifica se o usuário existe e se a senha está correta
    if username in users_db and check_password_hash(users_db[username], password):
        session['username'] = username  # Salva o usuário na sessão
        return jsonify({"message": "Login bem-sucedido"}), 200

    return jsonify({"error": "Nome de usuário ou senha incorretos"}), 401

# Rota para logout
@app.route('/logout', methods=['GET'])
def logout():
    session.pop('username', None)
    return redirect(url_for('index'))

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true", host='0.0.0.0', port=port)
