from flask import Flask, jsonify, request

app = Flask(__name__)

# Rota de teste
@app.route('/')
def home():
    return jsonify({"mensagem": "API funcionando!"})

# Rota GET
@app.route('/opponents', methods=['GET'])
def get_usuarios():
    return jsonify(["Alice", "Bob", "Carlos"])

# Rota POST
@app.route('/formations', methods=['GET'])
def criar_usuario():
    return jsonify(["Alice", "Bob", "Carlos"])

if __name__ == '__main__':
    app.run(debug=True)