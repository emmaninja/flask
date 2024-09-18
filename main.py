from flask import Flask, request, jsonify
import sympy as sp
from sympy.parsing.latex import parse_latex  # Importando o parseador LaTeX do SymPy
import scipy.integrate as spi
import numpy as np
import os  # Importação do módulo os

app = Flask(__name__)

# Função para cálculos matemáticos complexos usando SymPy e SciPy
def calcular_expressao_complexa(expressao, latex=False):
    try:
        # Se a expressão estiver em LaTeX, usar o parseador de LaTeX do SymPy
        if latex:
            sympy_expr = parse_latex(expressao)
        else:
            sympy_expr = sp.sympify(expressao)  # Converte a expressão para uma forma simbólica
        
        # Tentativa de simplificar a expressão com SymPy
        try:
            simplificado = sp.simplify(sympy_expr)  # Tenta simplificar a expressão
            print(f"Resultado simplificado: {simplificado}")
            return simplificado
        except Exception as e_sympy:
            print(f"Erro ao simplificar com SymPy: {e_sympy}")
        
        # Tentar usar SciPy para integrais definidas, etc.
        try:
            # Exemplo: Integrar usando scipy se a expressão for uma integral definida
            if 'integrate' in expressao:
                # Substituir 'integrate' por uma função lambda para integração numérica
                # Exemplo: "integrate(x**2, (x, 0, 1))" -> integral de x^2 de 0 a 1
                expr_parts = expressao.replace('integrate', '').strip('()').split(',')
                func_to_integrate = sp.lambdify(sp.Symbol('x'), sp.sympify(expr_parts[0]), modules=['numpy'])
                a, b = float(expr_parts[1].split(' ')[1]), float(expr_parts[2].split(' ')[1])
                resultado = spi.quad(func_to_integrate, a, b)[0]  # Integrar de a a b
                print(f"Resultado da integral numérica: {resultado}")
                return resultado
        except Exception as e_scipy:
            print(f"Erro ao calcular com SciPy: {e_scipy}")
        
        # Se não for possível simplificar ou avaliar, lançar um erro
        raise ValueError('Expressão não pôde ser avaliada ou simplificada.')

    except Exception as e:
        print(f"Erro geral ao processar a expressão: {e}")
        return str(e)

@app.route('/')
def index():
    return jsonify({"Choo Choo": "Welcome to your Flask app 🚅"})

@app.route('/calcular', methods=['POST'])
def calcular():
    dados = request.json
    print(f"Dados recebidos: {dados}")  # Log da requisição recebida
    expressao = dados.get('expressao', '')
    latex = dados.get('latex', False)  # Verifica se a expressão está em LaTeX

    if not expressao:
        return jsonify({'erro': 'Nenhuma expressão fornecida'}), 400

    try:
        # Adicionando log para verificar a expressão recebida
        print(f"Expressão para cálculo: {expressao}")
        
        resultado = calcular_expressao_complexa(expressao, latex=latex)
        print(f"Resultado do cálculo: {resultado}")  # Log do resultado
        return jsonify({'resultado': str(resultado)})  # Converter resultado para string
    except ValueError as ve:
        print(f"Erro de valor: {ve}")  # Log do erro de valor
        return jsonify({'erro': str(ve)}), 400
    except Exception as e:
        print(f"Erro ao processar a expressão: {e}")  # Log de qualquer outro erro
        return jsonify({'erro': 'Erro ao processar a expressão'}), 500

if __name__ == '__main__':
    port = int(os.getenv("PORT", 8080))  # Use a porta definida no ambiente, ou 8080 como padrão
    app.run(debug=os.getenv("FLASK_DEBUG", "false").lower() == "true", host='0.0.0.0', port=port)
