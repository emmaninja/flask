from flask import Flask, request, jsonify
import math
import os

app = Flask(__name__)

# Função para cálculos matemáticos complexos
def calcular_expressao_complexa(expressao):
    try:
        # Ambiente seguro para avaliar a expressão
        safe_dict = {k: getattr(math, k) for k in dir(math) if not k.startswith("__")}
        safe_dict.update({'abs': abs, 'round': round})
        resultado = eval(expressao, {"__builtins__": None}, safe_dict)
        return resultado
    except Exception as e:
        return str(e)

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route('/calcular', methods=['POST'])
def calcular():
    dados = request.json
    expressao = dados.get('expressao', '')

    if not expressao:
        return jsonify({'erro': 'Nenhuma expressão fornecida'}), 400

    resultado = calcular_expressao_complexa(expressao)
    return jsonify({'resultado': resultado})

if __name__ == '__main__':
    app.run(debug=True, port=os.getenv("PORT", default=5000))
