from flask import Flask, request, jsonify
import math
import os
import re

app = Flask(__name__)

# Função para validar expressões matemáticas
def validar_expressao(expressao):
    # Permitir apenas números, operadores e funções matemáticas básicas
    padrao = r'^[0-9+\-*/()., ]+$'
    if not re.match(padrao, expressao):
        raise ValueError('Error: not a mathematical expression')
    return True

# Função para cálculos matemáticos complexos
def calcular_expressao_complexa(expressao):
    try:
        validar_expressao(expressao)  # Validação extra da expressão
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
    print(f"Dados recebidos: {dados}")  # Log da requisição recebida
    expressao = dados.get('expressao', '')

    if not expressao:
        return jsonify({'erro': 'Nenhuma expressão fornecida'}), 400

    try:
        # Adicionando log para verificar a expressão recebida
        print(f"Expressão para cálculo: {expressao}")
        
        resultado = calcular_expressao_complexa(expressao)
        print(f"Resultado do cálculo: {resultado}")  # Log do resultado
        return jsonify({'resultado': resultado})
    except ValueError as ve:
        print(f"Erro de valor: {ve}")  # Log do erro de valor
        return jsonify({'erro': str(ve)}), 400
    except Exception as e:
        print(f"Erro ao processar a expressão: {e}")  # Log de qualquer outro erro
        return jsonify({'erro': 'Erro ao processar a expressão'}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))  # Use a porta definida no ambiente, ou 8080 como padrão
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true", host='0.0.0.0', port=port)

