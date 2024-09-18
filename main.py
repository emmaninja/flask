from flask import Flask, request, jsonify
import sympy as sp
from latex2sympy2 import latex2sympy
import os

app = Flask(__name__)

# Função para converter LaTeX para SymPy usando latex2sympy2
def latex_to_sympy(latex_expr):
    try:
        sympy_expr = latex2sympy(latex_expr)
        return sympy_expr
    except Exception as e:
        return f"Erro ao converter LaTeX para SymPy: {str(e)}"

# Função para calcular a expressão
def calcular_expressao(expressao, latex=False):
    try:
        if latex:
            # Converter a expressão LaTeX para SymPy
            sympy_expr = latex_to_sympy(expressao)
            if isinstance(sympy_expr, str) and "Erro ao converter" in sympy_expr:
                return sympy_expr
            resultado = sp.simplify(sympy_expr)
        else:
            # Avaliar a expressão diretamente usando SymPy
            sympy_expr = sp.sympify(expressao)
            resultado = sp.simplify(sympy_expr)

        # Retornar o resultado
        return resultado
    except Exception as e:
        return f"Erro ao processar a expressão: {str(e)}"

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route('/calcular', methods=['POST'])
def calcular():
    dados = request.json
    expressao = dados.get('expressao', '')
    latex = dados.get('latex', False)

    if not expressao:
        return jsonify({'erro': 'Nenhuma expressão fornecida'}), 400

    try:
        # Processar a expressão
        resultado = calcular_expressao(expressao, latex=latex)
        return jsonify({'resultado': str(resultado)})
    except Exception as e:
        return jsonify({'erro': f'Erro ao processar a expressão: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true", host='0.0.0.0', port=port)
