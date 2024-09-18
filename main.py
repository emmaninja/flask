from flask import Flask, request, jsonify
import sympy as sp
from sympy.parsing.latex import parse_latex
import os

app = Flask(__name__)

# Função para cálculos matemáticos complexos usando SymPy
def calcular_expressao_complexa(expressao, latex=False):
    try:
        # Se a expressão estiver em LaTeX, usar o parseador de LaTeX do SymPy
        if latex:
            sympy_expr = parse_latex(expressao)
        else:
            sympy_expr = sp.sympify(expressao)  # Converte a expressão para uma forma simbólica
        
        # Cálculo específico, como limites
        if sympy_expr.has(sp.Limit):
            resultado = sympy_expr.doit()
        else:
            # Tentativa de simplificar a expressão com SymPy
            resultado = sp.simplify(sympy_expr)
        
        print(f"Resultado: {resultado}")
        return resultado
    except Exception as e:
        print(f"Erro ao processar a expressão: {e}")
        return str(e)

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route('/calcular', methods=['POST'])
def calcular():
    dados = request.json
    print(f"Dados recebidos: {dados}")
    expressao = dados.get('expressao', '')
    latex = dados.get('latex', False)

    if not expressao:
        return jsonify({'erro': 'Nenhuma expressão fornecida'}), 400

    try:
        resultado = calcular_expressao_complexa(expressao, latex=latex)
        print(f"Resultado do cálculo: {resultado}")
        return jsonify({'resultado': str(resultado)})
    except ValueError as ve:
        print(f"Erro de valor: {ve}")
        return jsonify({'erro': str(ve)}), 400
    except Exception as e:
        print(f"Erro ao processar a expressão: {e}")
        return jsonify({'erro': 'Erro ao processar a expressão'}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true", host='0.0.0.0', port=port)
