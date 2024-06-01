from flask import Flask,request,render_template, jsonify
from flask_mysqldb import MySQL
# Se crea una instancia de Flask, que es la aplicación web.
app = Flask(__name__)
#parametros de conexion a la base de datos
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bdflask'
 #variable de conexion a la base de datos
mysql = MySQL(app)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/guardaralbum', methods=['POST'])
def guardaralbum():
    if request.method == 'POST':
        titulo = request.form['txtTitulo']
        artista = request.form['txtArtista']
        anio = request.form['txtAnio']
        print(titulo, artista, anio)
        return 'Datos recibidos en en el server'
@app.errorhandler(404)
def paginano(e):
    return 'Revisa tu sintaxis: No encontre nada'

if __name__ == '__main__':
    app.run(port=3000, debug=True)