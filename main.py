from flask import Flask, request, jsonify
import sympy as sp
from sympy.parsing.sympy_parser import parse_expr
import latex2sympy2 as latex2sympy
import os
import logging
import base64

app = Flask(__name__)

# Configurar o logger
logging.basicConfig(level=logging.INFO)

def calcular_expressao(expressao):
    try:
        # Log da expressão recebida
        logging.info(f"Expressão recebida: {expressao}")
        
        # Remover caracteres de início e fim indesejados (como $ ou \(...\))
        expressao = expressao.strip()
        if expressao.startswith('$$') and expressao.endswith('$$'):
            expressao = expressao[2:-2]
        elif expressao.startswith('$') and expressao.endswith('$'):
            expressao = expressao[1:-1]
        elif expressao.startswith('\\(') and expressao.endswith('\\)'):
            expressao = expressao[2:-2]
        logging.info(f"Expressão após remover delimitadores: {expressao}")

        # Tentar processar como expressão SymPy normal
        try:
            sympy_expr = parse_expr(expressao, transformations='all')
        except:
            # Se falhar, tentar processar como LaTeX
            sympy_expr = latex2sympy.latex2sympy(expressao)

        logging.info(f"Expressão convertida para SymPy: {sympy_expr}")

        # Substituir funções trigonométricas com argumentos em graus para radianos
        def to_radians(expr):
            if isinstance(expr, sp.Function) and expr.func in [sp.sin, sp.cos, sp.tan]:
                return expr.func(expr.args[0] * sp.pi / 180)
            return expr

        sympy_expr = sympy_expr.replace(to_radians)

        # Avaliar a expressão
        resultado = sympy_expr.evalf() if sympy_expr.is_Number else sp.simplify(sympy_expr)
        logging.info(f"Resultado da expressão: {resultado}")

        return resultado
    except Exception as e:
        logging.error(f"Erro ao processar a expressão: {str(e)}")
        return f"Erro ao processar a expressão: {str(e)}"

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route('/calcular', methods=['POST'])
def calcular():
    dados = request.json
    expressao = dados.get('expressao', '')

    # Log da entrada original
    logging.info(f"Entrada original recebida: {dados}")

    if not expressao:
        return jsonify({'erro': 'Nenhuma expressão fornecida'}), 400

    try:
        # Processar a expressão
        resultado = calcular_expressao(expressao)
        return jsonify({'resultado': str(resultado)})
    except Exception as e:
        logging.error(f"Erro ao processar a expressão: {str(e)}")
        return jsonify({'erro': f'Erro ao processar a expressão: {str(e)}'}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true", host='0.0.0.0', port=port)
