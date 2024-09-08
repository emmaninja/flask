from flask import Flask, request, jsonify
import os
from sympy import sympify, N

app = Flask(__name__)

@app.route('/calcular-passo', methods=['POST'])
def calcular_passo():
    data = request.json
    expressao = data.get('expressao')
    
    try:
        # Avalia a expressão matemática usando SymPy
        resultado = N(sympify(expressao))  # Converte a expressão para valor numérico
        return jsonify({'resultado': str(resultado)})
    except Exception as e:
        return jsonify({'erro': str(e)}), 400

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get("PORT", 5000)))
