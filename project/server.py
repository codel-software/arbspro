from flask import Flask, send_from_directory
import threading

# Inicialize o Flask
app = Flask(__name__, static_folder='public')

# Servir o arquivo index.html


@app.route('/')
def serve_index():
    return send_from_directory(app.static_folder, 'index.html')

# Servir os arquivos JSON


@app.route('/<path:filename>')
def serve_json(filename):
    return send_from_directory(app.static_folder, filename)

# Iniciar o servidor Flask em uma thread separada


app.run(host='0.0.0.0', port=5000, debug=False, use_reloader=False)
