from flask import Flask, request, jsonify
import sympy as sp
from latex2sympy2 import latex2sympy  # Importando o latex2sympy2 para converter LaTeX
import os

app = Flask(__name__)

def calcular_expressao(expressao, latex=False):
    try:
        if latex:
            # Convertendo expressão LaTeX para SymPy usando latex2sympy2
            try:
                sympy_expr = latex2sympy(expressao)
            except Exception as e:
                return f"Erro ao converter LaTeX para SymPy: {str(e)}"
        else:
            # Converter a expressão diretamente para SymPy se não estiver em LaTeX
            sympy_expr = sp.sympify(expressao)

        # Avaliar o tipo de operação a ser realizada
        if isinstance(sympy_expr, sp.Basic):
            # Tentar simplificar a expressão
            resultado = sp.simplify(sympy_expr)
        else:
            # Avaliação numérica
            resultado = sympy_expr.evalf()

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
