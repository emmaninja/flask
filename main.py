from flask import Flask, request, jsonify
import sympy as sp
from sympy.parsing.latex import parse_latex  # Importando o parseador LaTeX do SymPy
import os  # Importação do módulo os

app = Flask(__name__)

# Função para cálculos matemáticos complexos usando SymPy
def calcular_expressao_complexa(expressao, latex=False):
    try:
        # Se a expressão estiver em LaTeX, usar o parseador de LaTeX do SymPy
        if latex:
            sympy_expr = parse_latex(expressao)
        else:
            sympy_expr = sp.sympify(expressao)  # Converte a expressão para uma forma simbólica
        
        # Se for um limite, calcular o limite
        if sympy_expr.has(sp.Limit):
            limite = sympy_expr.limit()
            print(f"Resultado do limite: {limite}")
            return limite

        # Simplificar ou avaliar a expressão
        resultado = sp.simplify(sympy_expr)
        print(f"Resultado simplificado: {resultado}")
        return resultado

    except Exception as e:
        print(f"Erro ao processar a expressão: {e}")
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
