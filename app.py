from flask import Flask, render_template, request, session, redirect, url_for
import mysql.connector

app = Flask(__name__)

app.secret_key = 'Claudia13'
usuarios = {'andres':'41662431'}

# Conexión a la base de datos MySQL
db_connection = mysql.connector.connect(
    host="localhost",
    user="root",
    password="20011074",
    database="qbandres"
)

# Rutas

# Ruta para la página principal
@app.route('/')
def index():
    return render_template('index.html')

# Ruta para el inicio de sesión
@app.route('/login', methods=['POST'])
def login():
    username = request.form['username']
    password = request.form['password']

    if username in usuarios and usuarios[username] == password:
        session['username'] = username
        return redirect(url_for('main'))
    else:
        return render_template('index.html', error='Credenciales incorrectas')

# Ruta para la página principal después de iniciar sesión
@app.route('/main')
def main():
    if 'username' in session:
        # Consulta a la base de datos para obtener datos de la tabla "budget"
        cursor = db_connection.cursor()
        cursor.execute("SELECT * FROM budget")
        table_data = cursor.fetchall()
        cursor.close()
        return render_template('main.html', table_data=table_data)
    else:
        return redirect(url_for('index'))

# Ruta para agregar un nuevo gasto
@app.route('/agregar_gasto')
def agregar_gasto():
    return render_template('agregar_gasto.html')

# Ruta para editar un gasto
@app.route('/editar/<int:id>', methods=['GET', 'POST'])
def editar(id):
    if 'username' in session:
        if request.method == 'POST':
            # Procesar la solicitud de edición y actualizar la base de datos
            nuevo_nombre = request.form['nuevo_nombre']
            nueva_descripcion = request.form['nueva_descripcion']
            nueva_cantidad = request.form['nueva_cantidad']
            nuevo_tipo = request.form['nuevo_tipo']
            nueva_clase = request.form['nueva_clase']
            nueva_fecha = request.form['nueva_fecha']

            cursor = db_connection.cursor()
            update_query = "UPDATE budget SET NOMBRE = %s, DESCRIPTION = %s, CANT = %s, TIPO = %s, CLASS = %s, DATE_EXE = %s WHERE ID = %s"
            cursor.execute(update_query, (nuevo_nombre,nueva_descripcion, nueva_cantidad, nuevo_tipo, nueva_clase, nueva_fecha, id))
            db_connection.commit()
            cursor.close()

            return redirect(url_for('main'))

        else:
            # Obtener los detalles del gasto a editar
            cursor = db_connection.cursor()
            cursor.execute("SELECT * FROM budget WHERE ID = %s", (id,))
            gasto = cursor.fetchone()
            cursor.close()

            return render_template('editar_gasto.html', gasto=gasto)

    else:
        return redirect(url_for('index'))
    

@app.route('/eliminar/<int:id>', methods=['GET', 'POST'])
def eliminar(id):
    if 'username' in session:
        if request.method == 'GET':
            cursor = db_connection.cursor()
            delete_query = "DELETE FROM budget WHERE ID = %s"
            cursor.execute(delete_query, (id,))
            db_connection.commit()
            cursor.close()
            print("Deleted row with ID:", id)  # Add a print statement for debugging
            return redirect(url_for('main'))
    return redirect(url_for('main'))

@app.route('/procesar_gasto', methods=['POST'])
def procesar_gasto():
    if 'username' in session:
        nombre = request.form['nombre']
        descripcion = request.form['descripcion']
        cantidad = float(request.form['cantidad'])
        tipo = request.form['tipo']
        clase = request.form['clase']
        fecha = request.form['fecha']

        # Cambiar el signo de la cantidad según el tipo (Gasto o Ingreso)
        if tipo == 'GASTO':
            cantidad = -cantidad  # Hacer la cantidad negativa para gastos

        # Aquí debes ejecutar una consulta SQL para insertar los datos del nuevo gasto en la tabla 'budget'
        cursor = db_connection.cursor()
        insert_query = "INSERT INTO budget (NOMBRE, DESCRIPTION, CANT, TIPO, CLASS, DATE_EXE) VALUES (%s, %s, %s, %s, %s, %s)"
        cursor.execute(insert_query, (nombre, descripcion, cantidad, tipo, clase, fecha))
        db_connection.commit()
        cursor.close()

        return redirect(url_for('main'))
    else:
        return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
