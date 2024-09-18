from flask import Flask, request, jsonify
import sympy as sp
from sympy.parsing.latex import parse_latex
import os

app = Flask(__name__)

# Função para calcular a expressão
def calcular_expressao(expressao, latex=False):
    try:
        # Se a expressão estiver em LaTeX, converter para uma expressão SymPy
        if latex:
            # Tentar fazer o parsing da expressão como LaTeX
            sympy_expr = parse_latex(expressao)
        else:
            sympy_expr = sp.sympify(expressao)
        
        # Avaliar o tipo de operação a ser realizada
        if isinstance(sympy_expr, sp.Limit):
            # Calcular o limite se a expressão contiver um objeto de limite
            resultado = sympy_expr.doit()
        else:
            # Tentar simplificar a expressão
            resultado = sp.simplify(sympy_expr)
        
        # Verificar se a expressão simplificada é um número
        if resultado.is_number:
            # Avaliação numérica
            resultado = resultado.evalf()
        
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
