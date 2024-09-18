from flask import Flask, request, jsonify
import sympy as sp  # Biblioteca SymPy para cálculos simbólicos

app = Flask(__name__)

# Função para cálculos matemáticos complexos usando SymPy
def calcular_expressao_complexa(expressao):
    try:
        # Tentativa de processar a expressão com SymPy
        try:
            sympy_result = sp.sympify(expressao).evalf()  # Avaliar a expressão simbólica
            print(f"Resultado SymPy: {sympy_result}")
            return sympy_result
        except Exception as e_sympy:
            print(f"Erro ao processar com SymPy: {e_sympy}")
        
        # Se a expressão não puder ser processada, lançar um erro
        raise ValueError('Expressão não pôde ser avaliada por SymPy.')

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

    if not expressao:
        return jsonify({'erro': 'Nenhuma expressão fornecida'}), 400

    try:
        # Adicionando log para verificar a expressão recebida
        print(f"Expressão para cálculo: {expressao}")
        
        resultado = calcular_expressao_complexa(expressao)
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
