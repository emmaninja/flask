from flask import Flask, request, jsonify
import sympy as sp
from pylatexenc.latex2text import LatexNodes2Text  # Importando para converter LaTeX em texto
import os

app = Flask(__name__)

def calcular_expressao(expressao, latex=False):
    try:
        if latex:
            # Converter expressão LaTeX para texto usando pylatexenc
            try:
                text_expr = LatexNodes2Text().latex_to_text(expressao)
                sympy_expr = sp.sympify(text_expr)
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
