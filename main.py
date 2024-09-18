from flask import Flask, request, jsonify
import sympy as sp
from sympy.parsing.latex import parse_latex
import os

app = Flask(__name__)

def calcular_expressao(expressao, latex=False):
    try:
        if latex:
            # Remover duplicações de barras invertidas
            expressao = expressao.encode('utf-8').decode('unicode_escape')

            # Processamento da expressão LaTeX
            if r'\lim' in expressao:
                # Extrair a parte da expressão com o limite
                expressao = expressao.replace(r'\lim', 'limit')  # simplificar para a detecção do limite
                if '_{' in expressao and '}' in expressao:
                    # Extrair o valor de x e a direção (se houver)
                    partes = expressao.split('}')
                    limite_de = partes[0].split('_')[1].replace('{', '').replace('x \\to ', '')
                    direcao = '+' if '^+' in limite_de else '-' if '^-' in limite_de else ''
                    valor_limite = limite_de.replace('^+', '').replace('^-', '')
                    
                    # Extrair a função que será usada no limite
                    funcao = partes[1]
                    
                    # Criar expressão SymPy para o limite
                    sympy_expr = sp.limit(parse_latex(funcao), sp.Symbol('x'), sp.sympify(valor_limite), dir=direcao)
                else:
                    return "Expressão de limite inválida."
            else:
                # Tentar fazer o parsing da expressão como LaTeX normalmente
                sympy_expr = parse_latex(expressao)
        else:
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
