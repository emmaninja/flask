from flask import Flask, request, jsonify
from sympy import sympify, N
import os  # Importar o módulo os para pegar a variável PORT

app = Flask(__name__)

@app.route('/calcular', methods=['POST'])
def calcular():
    data = request.json
    expressao = data.get('expressao')
    
    try:
        resultado = N(sympify(expressao))
        return jsonify({'resultado': str(resultado)})
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
