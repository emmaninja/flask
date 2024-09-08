from flask import Flask, request, jsonify
from sympy import sympify, N
import os  # Importar o módulo os para pegar a variável PORT

app = Flask(__name__)

# Rota para cálculos matemáticos usando SymPy
@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.json
    expressao = data.get('expressao')
    
    try:
        resultado = N(sympify(expressao))
        return jsonify({'resultado': str(resultado)})
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

# Rota para validar conceitos matemáticos (usando SymPy para validar explicações)
@app.route('/validar_conceito', methods=['POST'])
def validar_conceito():
    data = request.json
    expressao = data.get('explicacao')

    try:
        # Aqui você pode usar o SymPy para validar a expressão
        resultado = N(sympify(expressao))
        return jsonify({'resultado': str(resultado), 'valido': True})
    except Exception as e:
        return jsonify({'erro': str(e), 'valido': False}), 400

# Inicializa o servidor Flask na porta definida pela variável de ambiente PORT ou a porta 5000 como padrão
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
