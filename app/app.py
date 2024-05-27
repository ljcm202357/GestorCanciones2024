from flask import Flask, render_template, redirect, request, url_for, flash, jsonify, session, send_file
import mysql.connector
import bcrypt
from werkzeug.security import check_password_hash
from werkzeug.security import generate_password_hash
import logging
import base64
import io
# creamos una instancia de la clase flask

app = Flask(__name__)
# Este error indica que estás intentando usar sesiones en tu aplicación Flask,
# pero no has configurado una clave secreta (secret_key).
# La clave secreta es necesaria para firmar las sesiones y garantizar su seguridad.
app.secret_key = '51935349'

# configurar la conexion
db = mysql.connector.connect(
    host="localhost",
    user="root",
    password="",
    database="Agenda2024"

)
cursor = db.cursor()

# Configurar el registro
logging.basicConfig(level=logging.DEBUG)


def encriptarcontra(contraencrip):
    # generar un hash de la contraseña
    encriptar = bcrypt.hashpw(contraencrip.encode('utf-8'), bcrypt.gensalt())

    return encriptar


@app.route('/login', methods=['GET', 'POST'])
def login():

    if request.method == 'POST':
        # Obtener las credenciales del formulario
        username = request.form.get('txtusuario')
        password = request.form.get('txtcontrasena')

        # Consultar la base de datos para obtener el usuario
        cursor = db.cursor(dictionary=True)
        query = "SELECT usuarioper, contraper, roles FROM personas WHERE usuarioper = %s"
        cursor.execute(query, (username,))
        usuario = cursor.fetchone()

        if usuario and check_password_hash(usuario['contraper'], password):
            # Autenticación exitosa, establecer las variables de sesión
            session['usuario'] = usuario['usuarioper']
            session['rol'] = usuario['roles']

            # Redirigir según el rol del usuario
            if usuario['roles'] == 'administrador':
                return redirect(url_for('lista'))
            else:
                return redirect(url_for('mostrar_canciones'))
        else:
            # Credenciales inválidas, mostrar mensaje de error
            print("Credenciales incorrectas. Por favor, intenta nuevamente.")
            return render_template('login.html')

    # Si la solicitud es GET, renderizar el formulario de inicio de sesión
    return render_template('login.html')


@app.route('/logout')
def logout():
    # Elimina el nombre de usuario de la sesión
    session.pop('usuario', None)
    return redirect(url_for('login'))

# NO ALMACENAR CACHE DE LA PAGINA


@app.after_request
def add_header(response):
    response.headers['Cache-Control'] = 'no-cache, no-store, must-revalidate'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response


@app.route('/principal', methods=['GET', 'POST'])
def principal():
   # Verificar si el usuario ha iniciado sesión
    if 'usuario' in session:
        # Obtener el nombre de usuario de la sesión
        nombre_usuario = session['usuario']
        # Renderizar la plantilla de Principal.html
        return render_template('prin.html', nombre_usuario=nombre_usuario)
    else:
        # Si el usuario no ha iniciado sesión, redirigirlo a la página de inicio de sesión
        return redirect(url_for('login'))


@app.route('/lista', methods=['GET', 'POST'])
def lista():

    # Recuperar datos de la tabla Personas
    cursor = db.cursor()
    cursor.execute("SELECT *  FROM personas")
    usuarios = cursor.fetchall()

    # Pasar los datos a un template HTML para mostrar la lista
    return render_template('index.html', personas=usuarios)


@app.route('/Registrar', methods=['GET', 'POST'])
def registrar_usuario():
    if request.method == 'POST':
        Nombres = request.form.get('nombre')
        Apellidos = request.form.get('apellido')
        Email = request.form.get('email')
        Direccion = request.form.get('direccion')
        Telefono = request.form.get('telefono')
        Usuario = request.form.get('usuario')
        Contrasena = request.form.get('contrasena')
        roles = request.form.get('txtrol')
        Contrasenaencriptada = generate_password_hash(Contrasena)

        # Verificar si el usuario y el correo electrónico ya existen en la base de datos
        cursor = db.cursor()
        cursor.execute(
            "SELECT * FROM personas WHERE usuarioper = %s OR emailper = %s", (Usuario, Email))
        existing_user = cursor.fetchone()

        if existing_user:
            print("'El usuario o correo ya está registrado.")
            return render_template('Registrar.html')

    # insertar datos a la tabla personas

        cursor.execute("INSERT INTO Personas(nombreper,apellidoper,emailper,dirper,telper,usuarioper,contraper,roles)VALUES(%s,%s,%s,%s,%s,%s,%s,%s)",
                       (Nombres, Apellidos, Email, Direccion, Telefono, Usuario, Contrasenaencriptada, roles))
        db.commit()
        # flash('Usuario registrado correctamente', 'success')
        return redirect(url_for('login'))
    # Redirigir a la misma página después de procesar la solicitud POST
        return redirect(url_for('registrar_usuario'))

    # Si la solicitud es GET, renderizar el formulario
    return render_template('Registrar.html')


@app.route('/editar/<int:id>', methods=['POST', 'GET'])
def editar_usuario(id):
    # cursor = db.cursor()
    # cursor.execute('SELECT * FROM personas WHERE idper = %s', (id,))
    # data = cursor.fetchall()
    # cursor.close()
    # return render_template('editar.html', personas=data[0])
    cursor = db.cursor()

    if request.method == 'POST':
        nombre = request.form['nombreper']
        apellido = request.form['apellidoper']
        email = request.form['emailper']
        direccion = request.form['direccionper']
        telefono = request.form['telefonoper']
        usuario = request.form['usuarioper']
        contrasena = request.form['contrasenaper']

        # Actualizar los datos en la base de datos
        sql = "UPDATE personas SET nombreper=%s, apellidoper=%s, emailper=%s, dirper=%s, telper=%s, usuarioper=%s, contraper=%s WHERE idper=%s"
        cursor.execute(sql, (nombre, apellido, email, direccion,
                       telefono, usuario, contrasena, id))
        db.commit()

        # Redirigir a la página de lista después de editar
        return redirect(url_for('lista'))

    else:
        # Obtener los datos del usuario a editar
        cursor = db.cursor()
        cursor.execute("SELECT * FROM personas WHERE idper = %s", (id,))
        data = cursor.fetchall()
        cursor.close()
        return render_template('editar.html', personas=data[0])


@app.route('/eliminar/<int:id>', methods=['GET'])
def eliminar_usuario(id):
    cursor = db.cursor()
    cursor.execute('DELETE FROM personas WHERE idper = %s', (id,))
    db.commit()
    cursor.close()
    return redirect(url_for('lista'))

# agrgar canciones


@app.route('/agregarcanciones', methods=['GET', 'POST'])
def registrar_canciones():
    if request.method == 'POST':
        titulo = request.form.get('txttitulo')
        artista = request.form.get('txtartista')
        genero = request.form.get('txtgenero')
        precio = request.form.get('txtprecio')
        duracion = request.form.get('txtduracion')
        alanzamiento = request.form.get('txtlanzamiento')
        # Obtener la imagen del formulario
        imagen = request.files['txtimagen']
        imagen_blob = imagen.read()  # Leer los datos de la imagen

        # Definir un cursor
        cursor = db.cursor()

        try:
            # Insertar datos en la tabla canciones
            cursor.execute("INSERT INTO canciones(title, artist, genre, price, duration, alanzamiento, img) VALUES (%s, %s, %s, %s, %s, %s, %s)",
                           (titulo, artista, genero, precio, duracion, alanzamiento, imagen_blob))
            db.commit()
            print("Canción registrada correctamente")
            return redirect(url_for('lista'))
        except Exception as e:
            print("Error al registrar la canción:", e)
            db.rollback()  # Revertir cambios en caso de error
            return "Error al registrar la canción. Por favor, inténtalo de nuevo."

    # Si la solicitud es GET, renderizar el formulario
    return render_template('Acanciones.html')


def custom_b64encode(blob):
    return base64.b64encode(blob).decode('utf-8')

# Ruta para mostrar las canciones

# Ruta para mostrar una imagen específica por su ID


@app.route('/mostrar/<int:id>')
def mostrar(id):

    cursor = db.cursor()

    cursor.execute(
        "SELECT  img FROM canciones WHERE song_id = %s", (id,))
    data = cursor.fetchone()

    if data:

        imagen = base64.b64encode(data[0]).decode('utf-8')
        return render_template('canciones.html', imagen=imagen)
    else:
        return print("Imagen no encontrada")


@app.route('/canciones')
def mostrar_canciones():
    cursor = db.cursor()

    cursor.execute(
        "SELECT song_id,title, artist, genre, price, duration, alanzamiento, img FROM canciones")
    canciones = cursor.fetchall()

    if canciones:
        # Crear una lista para almacenar los datos de las canciones
        canciones_data = []
        for cancion in canciones:
            # Convertir la imagen a base64
            imagen = base64.b64encode(cancion[7]).decode('utf-8')
            # Agregar los datos de la canción junto con la imagen a la lista de canciones
            canciones_data.append({
                'idcancion':cancion[0],
                'titulo': cancion[1],
                'artista': cancion[2],
                'genero': cancion[3],
                'precio': cancion[4],
                'duracion': cancion[5],
                'lanzamiento': cancion[6],
                'imagen': imagen
            })
        return render_template('canciones.html', canciones=canciones_data)
    else:

        return "No se encontraron canciones"

@app.route('/agregar-al-carro',methods=['GET', 'POST'])
def agregar_al_carrito():

    idcan = request.form['idcan']
    titulocan = request.form['titulocan']
    preciocan = request.form['preciocan']

    if 'cart' not in session:
        session['cart'] = []


    session['cart'].append({'id':idcan,'titulo':titulocan,'precio':float (preciocan)})  
    session.modified = True

    print("contenido del carro",session['cart'])

    return jsonify({'message': 'Canción agregada al carro'})

@app.route('/carrito', methods = ['GET', 'POST'])
def ver_carrito():
  carro= session.get('cart',[])
  total = sum(item['precio'] for item in carro)

  return render_template('carrito.html',carro=carro,total=total)

# para ejecutar la aplicacion
if __name__ == '__main__':
    app.add_url_rule('/', view_func=lista)
    app.run(debug=True, port=5005)

# definir rutas
