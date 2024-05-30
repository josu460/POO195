from flask import Flask , request, jsonify
#importar conexion a la base de datos
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

# Ruta simple
# @app.route('/')
# def principal():
#     return 'Hola Mundo'

@app.route('/pruebaConexion')
def pruebaConexion():
    try:
        cursor =mysql.connection.cursor()
        cursor.execute("Select 1")
        datos = cursor.fetchone()
        return jsonify({'status': 'Conexion exitosa', 'data': datos})
    except Exception as ex:
        return jsonify({'status': 'Error de conexion', 'mensaje': str(ex)})

# Ruta doble
@app.route('/usuario')
@app.route('/saludar')
def saludos():
    return 'Hola Mundo Josue'

# Rutas con parámetros
@app.route('/hi/<nombre>')
def hi(nombre):
    return f'Hola, {nombre}!'


#definicion de metodos de trabajo 
@app.route('/formulario/', methods=['GET', 'POST'])
def formulario():
    if request.method == 'GET':
        return 'No es seguro enviar password por GET'
    elif request.method == 'POST':
        return 'POST si es seguro para passwords'
    
#Manejo de excepciones para rutas 

@app.errorhandler(404)
def paginano(e):
    return 'Revisa tu sintaxis: No encontre nada'


if __name__ == '__main__':
    # El puerto es donde se ejecutará la aplicación y debug=True activa el modo de depuración.
    app.run(port=3000, debug=True)
