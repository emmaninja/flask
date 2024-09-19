from flask import Flask, request, jsonify
import sympy as sp
import latex2sympy2 as latex2sympy
import logging

app = Flask(__name__)

# Configurar o logger
logging.basicConfig(level=logging.INFO)

def calcular_expressao(expressao):
    try:
        # Log da expressão recebida
        logging.info(f"Expressão LaTeX recebida: {expressao}")

        # Processar LaTeX usando latex2sympy
        sympy_expr = latex2sympy.latex2sympy(expressao)
        logging.info(f"Expressão convertida para SymPy: {sympy_expr}")

        # Avaliar a expressão
        resultado = sp.simplify(sympy_expr)
        logging.info(f"Resultado da expressão: {resultado}")

        return resultado
    except Exception as e:
        logging.error(f"Erro ao processar a expressão: {str(e)}")
        return f"Erro ao processar a expressão: {str(e)}"

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
    app.run(debug=True, host='0.0.0.0', port=8080)
