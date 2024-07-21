from flask import Flask, request, jsonify, send_from_directory
import mysql.connector

app = Flask(__name__)

# Configurações de conexão com o MySQL
db_config = {
    'user': 'root',
    'password': 'fnlj1984',
    'host': 'localhost',
    'database': 'meus_dados'
}

@app.route('/')
def index():
    return send_from_directory('templates', 'index.html')

@app.route('/static/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

@app.route('/search', methods=['GET'])
def search():
    query = request.args.get('query')
    if not query:
        return jsonify({'error': 'Query parameter is required'}), 400

    connection = mysql.connector.connect(**db_config)
    cursor = connection.cursor(dictionary=True)
    sql = "SELECT codigo, interprete, titulo FROM musica WHERE titulo LIKE %s OR interprete LIKE %s"
    search_term = '%' + query + '%'
    cursor.execute(sql, (search_term, search_term))
    results = cursor.fetchall()
    cursor.close()
    connection.close()

    return jsonify(results)

if __name__ == '__main__':
    app.run(debug=True)
