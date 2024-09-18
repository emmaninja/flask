from flask import Flask, request, jsonify
import sympy as sp
import latex2sympy2 as latex2sympy
import os

app = Flask(__name__)

def calcular_expressao(expressao, latex=False):
    try:
        if latex:
            print(f"Expressão original recebida: {expressao}")  # Print antes da substituição
            # Remover escapes adicionais da expressão
            expressao = expressao.replace('\\\\', '\\')  # Substitui '\\' por '\'
            print(f"Expressão após substituir barras invertidas: {expressao}")  # Print após a substituição
            # Processar LaTeX usando latex2sympy
            sympy_expr = latex2sympy.latex2sympy(expressao)
            print(f"Expressão convertida para SymPy: {sympy_expr}")  # Print antes da avaliação
        else:
            sympy_expr = sp.sympify(expressao)

        # Avaliar o tipo de operação a ser realizada
        if isinstance(sympy_expr, sp.Basic):
            # Tentar simplificar a expressão
            resultado = sp.simplify(sympy_expr)
        else:
            # Avaliação numérica
            resultado = sympy_expr.evalf()

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

