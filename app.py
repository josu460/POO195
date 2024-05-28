from flask import Flask , request
# Se crea una instancia de Flask, que es la aplicación web.
app = Flask(__name__)

# Ruta simple
@app.route('/')
def principal():
    return 'Hola Mundo'

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
