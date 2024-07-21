from flask import Flask, request, render_template, url_for, redirect, flash
from flask_mysqldb import MySQL
import os
from werkzeug.utils import secure_filename

app = Flask(__name__)
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_USER'] = 'root'
app.config['MYSQL_PASSWORD'] = ''
app.config['MYSQL_DB'] = 'bdflask'
#configuración de la carpeta para subir de imagenes a la carpeta uploads
app.config['UPLOAD_FOLDER'] = "C:/Users/Windows/Documents/GitHub/POO195/CrudAlbums/static/uploads"
app.config['ALLOWED_EXTENSIONS'] = {'png', 'jpg', 'jpeg'}

app.secret_key = 'mysecretkey'
# aqui es para que solo te deje subir imagenes png, jpg, jpeg
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in app.config['ALLOWED_EXTENSIONS']

mysql = MySQL(app)

# Manejo de excepciones
@app.errorhandler(404)
def paginano(e):
    return 'Revisar tu sintaxis: No encontré nada'

@app.route('/')
def index():
    try:
        cursor = mysql.connection.cursor()
        cursor.execute('SELECT * FROM albums')
        consultaA = cursor.fetchall()
        print(consultaA)
        return render_template('index.html', albums=consultaA)
    except Exception as e:
        print(e)
        return 'Error al obtener los álbumes'

@app.route('/GuardarAlbum', methods=['GET','POST'])
def guardarAlbum():
    if request.method == 'POST':
        try:
            Fnombre = request.form['txtTitulo']
            Fartista = request.form['txtArtista']
            Fanio = request.form['txtAnio']
            Fimagen = request.files['Imagen']
# aqui se verifica si se subio la imagen y si esta permitida en los parametros 
            if Fimagen and allowed_file(Fimagen.filename):
                filename = secure_filename(Fimagen.filename)
#aqui se genera la ruta donde se guardara la imagen 
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                Fimagen.save(file_path)
#genera la url de la imagen
                imagen_url = request.host_url + 'static/uploads/' + filename  
            else:
                imagen_url = None
                print('No se subió imagen')
            # Enviamos a la BD
            cursor = mysql.connection.cursor()
    #insertamos los datos en la tabla albums
            cursor.execute('INSERT INTO albums(titulo, artista, anio, imagen_url) VALUES(%s, %s, %s, %s)', (Fnombre, Fartista, Fanio, imagen_url))
            mysql.connection.commit()
            flash('Álbum guardado correctamente')
            print('Álbum guardado correctamente en la base de datos')
            return redirect(url_for('index'))
        
        except Exception as e:
            flash('Error al guardar el álbum: ' + str(e))
            return redirect(url_for('index'))

@app.route('/editar/<id>')
def editar(id):
    cur= mysql.connection.cursor()
    cur.execute('select * from albums where idAlbum=%s',[id])
    albumE= cur.fetchone()
    return render_template('editar.html', album= albumE)

@app.route('/ActualizarAlbum/<id>', methods=['POST'])
def ActualizarAlbum(id):
    if request.method == 'POST':
        try:
            Ftitulo = request.form['txtTitulo']
            Fartista = request.form['txtArtista']
            Fanio = request.form['txtAnio']
            Fimagen = request.files.get('Imagen')
            cursor = mysql.connection.cursor()
            if Fimagen and allowed_file(Fimagen.filename):
                filename = secure_filename(Fimagen.filename)
                file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                Fimagen.save(file_path)
                imagen_url = request.host_url + 'static/uploads/' + filename 
                #Actualiza el album si quieres cambiar la imagen
                cursor.execute('UPDATE albums SET titulo=%s , artista=%s , anio=%s, imagen_url=%s where idAlbum=%s', (Ftitulo, Fartista, Fanio, imagen_url, id))
            else:

            # Enviamos a la BD
           # actualiza el album si no quieres cambiar la imagen
                cursor.execute('UPDATE albums set titulo=%s , artista=%s , anio=%s where idAlbum=%s', (Ftitulo, Fartista, Fanio, id))
            mysql.connection.commit()
            flash('Álbum editado correctamente')
            return redirect(url_for('index'))
        
        except Exception as e:
            flash('Error al guardar el álbum: ' + str(e))
            return redirect(url_for('index'))

@app.route('/eliminar/<id>')
def eliminar(id):
    try:
        cur = mysql.connection.cursor()
        cur.execute('DELETE FROM albums WHERE idAlbum = %s', [id])
        mysql.connection.commit()
        flash('Álbum eliminado correctamente')
        return redirect(url_for('index'))
    except Exception as e:
        flash('Error al eliminar el álbum: ' + str(e))
        return redirect(url_for('index'))



if __name__ == '__main__':
    app.run(port=10000, debug=True)