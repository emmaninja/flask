from flask import Flask, request, jsonify
import sympy as sp
import latex2sympy2 as latex2sympy
import os
import logging
import re

app = Flask(__name__)

# Configurar o logger
logging.basicConfig(level=logging.INFO)

def limpar_expressao(expressao):
    """
    Função para limpar a expressão LaTeX, removendo delimitadores extras
    e tratando barras invertidas.
    """
    # Remover delimitadores LaTeX
    expressao = re.sub(r'^\$+|\$+$|^\\\(|\\\)$|^\\\[|\\\]$', '', expressao)

    return expressao

def calcular_expressao(expressao, latex=False):
    try:
        logging.info(f"Expressão original recebida: {expressao}")  # Log da expressão original

        if latex:
            # Limpar a expressão
            expressao_limpa = limpar_expressao(expressao)
            logging.info(f"Expressão após limpeza: {expressao_limpa}")  # Log após a limpeza

            # Use a expressão como uma string "raw" para evitar problemas de barras invertidas
            try:
                sympy_expr = latex2sympy.latex2sympy(rf"{expressao_limpa}")
                logging.info(f"Expressão convertida para SymPy: {sympy_expr}")  # Log antes da avaliação
            except Exception as e:
                logging.error(f"Erro ao converter LaTeX para SymPy: {str(e)}")
                return f"Erro ao converter LaTeX para SymPy: {str(e)}"
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
        logging.error(f"Erro ao processar a expressão: {str(e)}")  # Log em caso de erro
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
        logging.error(f"Erro ao processar a expressão: {str(e)}")  # Log em caso de erro
        return jsonify({'erro': f'Erro ao processar a expressão: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true", host='0.0.0.0', port=port)
