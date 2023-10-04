# Imports
from config import *
from database import Register

# Create own NumberedCanvas class object Canvas
class NumberedCanvas(Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.page_numbers = []

    def showPage(self):
        self.page_numbers.append(self._pageNumber)
        self._startPage()

    def save(self):
        page_count = len(self.page_numbers)
        for i, page_number in enumerate(self.page_numbers):
            self.restoreState()
            self.setFont("Helvetica", 10)
            self.drawRightString(
                7.5 * inch, 0.75 * inch, f"Pagina {page_number} de {page_count}"
            )
            self.showPage()
        super().save()

# Upload Folder
CARPETA = os.path.join("uploads")
app.config["CARPETA"] = CARPETA

@app.route("/uploads/<nombrefoto>")
def uploads(nombrefoto):
    return send_from_directory(app.config["CARPETA"], nombrefoto)


# send password to user-email
def send_password(email, data):
    msg = Message(
        f"Hola! {email} Establece tu nueva contraseña a continuacion",
        sender="upttinfo@gmail.com",
        recipients=["{}".format(email)],
    )
    msg.body = "Para Cambiar Tu Contraseña ingresa en el siguiente link: {}".format(
        data
    )
    mail.send(msg)
    return "Mensage Enviado!!"


# home route
@app.route("/home")
def home():
    return render_template("home.html")


@app.route("/download")
def download():
    return send_file("static/plantilla/form.doc", as_attachment=True)


# requisites route
@app.route("/requisitos")
def requisitos():
    return render_template("requisites.html")


# Universities
@app.route("/sedes")
def sedes():
    return render_template("sedes.html")


# Images
@app.route("/galeria")
def galeria():
    return render_template("gallery.html")


# Contact Form
@app.route("/contacto")
def contacto():
    return render_template("contact.html")


# Not Found
@app.errorhandler(404)
def not_found(e):
    return render_template("404.html"), 404

# Server Error
@app.errorhandler(505)
def server_error(e):
    return render_template("505.html"), 505


# Login
@app.route("/login",methods=["GET","POST"])
@app.route("/", methods=["GET", "POST"])
def login():
    """
    Procesa el inicio de sesión de usuarios.

    Esta función maneja tanto la visualización del formulario de inicio de sesión (GET) como el procesamiento de los
    datos de inicio de sesión ingresados por el usuario (POST). Verifica las credenciales proporcionadas y, si son
    válidas, redirige al usuario a su área de cuenta. En caso de una solicitud GET, muestra el formulario de inicio
    de sesión.

    Args:
        Ninguno (Los datos de inicio de sesión se toman de la solicitud POST).

    Returns:
        Si se recibe una solicitud POST con credenciales válidas, redirige al usuario a su área de cuenta.
        Si se recibe una solicitud GET o las credenciales no son válidas, muestra la página de inicio de sesión.
    """
    
    if request.method == "POST":
        usuario = request.form["usuario"]
        contraseña = request.form["password"]

        # execute query
        cursors = mysql.connection.cursor()
        cursors.execute(
            "SELECT * FROM users WHERE usuario = %s",
            (
                usuario,
            ),
        )

        account = cursors.fetchone()

        if account and bcrypt.check_password_hash(account[9],contraseña):
            session["logeado"] = True
            session["id"] = account[0]
            session["usuario"] = account[8]
            session["email"] = account[5]

            now = datetime.now()
            hora_entrada = now.strftime("%I:%M %p")

            session["hora_entrada"] = hora_entrada

            cursors.execute("SELECT * FROM users WHERE id = %s", (session["id"],))
            user = cursors.fetchone()

            # return render_template('dashboard.html',user=user)
            return redirect(url_for("cuenta"))

        else:
            flash("Usuario/Contraseña Incorrecta!")

    return render_template("login.html")


# lOGOUT
@app.route("/logout", methods=["GET", "POST"])
def logout():
    if "logeado" in session:
        hora_entrada = session["hora_entrada"]
        del session["hora_entrada"]

        hora_salida = datetime.now().strftime("%I:%M %p")
        session["hora_salida"] = hora_salida

        # SET HOURS TO 0

        #cur = mysql.connection.cursor()
        #cur.execute('UPDATE users set hora_entrada=NULL,hora_salida=NULL WHERE id=%s',(session["id"],))
        #mysql.connection.commit()

    session.pop("logeado", None)
    session.pop("id", None)
    session.pop("usuario", None)
    session.pop("hora_salida", None)
    session.pop("hora_entrada_marcada", None)


    return redirect(url_for("login"))


def GetHourFromDb(id):
	conn = mysql.connection.cursor()

	query = "SELECT hora_entrada FROM users WHERE id = %s "
	conn.execute(query,(id,))
	result = conn.fetchone()

	if result:
		hora_entrada = result[0]
	else:
		return None

@app.route("/cuenta", methods=["GET", "POST"])
def cuenta():
    if "logeado" in session:
        usuario = None
        user = None
        cursor = mysql.connection.cursor()


        if request.method == "POST":
            # get cedula
            cedula = request.form.get("cedula")
            
            if cedula: 
                # check cedula
                cursor.execute('SELECT * FROM users WHERE usuario = %s ',(cedula,))
                account = cursor.fetchone()

                if account:
                    return redirect(url_for('generar_informe_asistencia'))
                else:
                    flash("Usuario No Registrado!","danger")


            tipo = request.form.get("tipo")
            hora_actual = obtener_hora_actual()
            hora_inicio = time.time()

            cursor.execute("SELECT * FROM users WHERE id = %s", (session["id"],))
            user = cursor.fetchone()


            # Marcar la hora de entrada
            if tipo == "entrada":
                    cursor.execute(
                        "UPDATE users SET hora_entrada = %s WHERE id = %s",
                        (hora_actual, session["id"]),
                    )
                    mysql.connection.commit()
                    
            # Marcar la hora de salida
            elif tipo == "salida":
                    cursor.execute(
                            "UPDATE users SET hora_salida = %s WHERE id = %s",
                            (hora_actual, session["id"])
                    )
                    mysql.connection.commit()

        cursor = mysql.connection.cursor()
        cursor.execute("SELECT * FROM users WHERE id = %s", (session["id"],))
        user = cursor.fetchone()

        hora_entrada = user[12] if user and user[12] else ""
        hora_salida = user[13] if user and user[13] else ""

        # Determinar si los botones de marcar hora de entrada y salida deben estar deshabilitados
        marcar_entrada_deshabilitado = user[12] is not None
        marcar_salida_deshabilitado = user[12] is None

        # tasks functions
        email = session['email']
        cursor.execute("SELECT * FROM tasks WHERE email = %s", [email])
        tasks = cursor.fetchall()
        
        insertObject = []
        columnNames = [column[0] for column in cursor.description]
        for record in tasks:
            insertObject.append(dict(zip(columnNames, record)))

        return render_template(
            "dashboard.html",
            usuario=usuario,
            hora_entrada=hora_entrada,
            hora_salida=hora_salida,
            user=user,
            marcar_entrada_deshabilitado=marcar_entrada_deshabilitado,
            marcar_salida_deshabilitado=marcar_salida_deshabilitado,
            tasks=insertObject
        )

    return redirect(url_for("login"))


def obtener_hora_actual():
    # Crea un objeto timezone-aware usando pytz
    timezone = pytz.timezone('America/Caracas') 
    now = datetime.now(timezone)
    hora_actual = now.strftime("%I:%M %p")
    return hora_actual

# reset password
@app.route("/olvidocontraseña", methods=["GET", "POST"])
def olvidocontraseña():
    msg = ""
    if "logeado" in session:
        return redirect("/")  # redirect user if is located in dashboard`
    elif request.method == "POST" and "correo" in request.form:
        correo = request.form["correo"]
        token = str(uuid.uuid4())
        cursors = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        result = cursors.execute("SELECT * FROM users WHERE correo = % s", [correo])

        if result:
            data = cursors.fetchone()
            cursors = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursors.execute(
                "UPDATE users SET token=%s WHERE correo=%s", [token, correo]
            )
            mysql.connection.commit()

            host = "http://127.0.0.1:5000"
            data = "http://{}/cambiarcontraseña/{}".format(host, token)
            send_password(correo, data)  # send the password to the email

            msg = "Contraseña Enviada a su Email"
        else:
            msg = "!Correo Electronico No encontrado"

    return render_template("forgot.html", msg=msg)


# reset password
@app.route("/cambiarcontraseña/<token>", methods=["GET", "POST"])
def cambiarcontraseña(token):
    msg = ""
    if "logeado" in session:
        return redirect("/")

    if request.method == "POST":
        password = request.form["password"]
        confirmpassword = request.form["confirmpassword"]
        token1 = str(uuid.uuid4())

        if password != confirmpassword:
            flash("Las contraseñas no coinciden")
            return redirect("cambiarcontraseña")

        cursors = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
        cursors.execute("SELECT * FROM users WHERE token = % s", [token])
        user = cursors.fetchone()

        if user:
            cursors = mysql.connection.cursor(MySQLdb.cursors.DictCursor)
            cursors.execute(
                "UPDATE users SET token=%s,contraseña=%s WHERE token=%s",
                [token1, password, token],
            )
            mysql.connection.commit()
            cursors.close()
            msg = "Contraseña Actualizada Exitosamente!"
            return redirect("/")
        else:
            msg = "Token Invalido"
            return redirect("/")
    return render_template("reset.html", msg=msg)


# Register
@app.route("/registro", methods=["GET", "POST"])
def registro():
    if request.method == "POST":
        nombre = request.form["nombre"]
        apellido = request.form["apellido"]
        edad = request.form["edad"]
        fecha = request.form["fecha_nacimiento"]
        correo = request.form["correo"]
        direccion = request.form["direccion"]
        numero = request.form["numero_telefono"]
        usuario = request.form["usuario"]
        password = request.form["contraseña"]
        tipo_cargo = request.form["tipocargo"]
        imagen = request.files["imagen"]
        imagen_filename = imagen.filename

         # Register
        register = Register(nombre,apellido,edad,fecha,correo,direccion,numero,usuario,password,tipo_cargo,imagen)

        if not is_valid(imagen_filename):
            flash("Por favor, sube una imagen válida (jpg, png, jpeg)")
        elif register.check_user():
            flash("La cuenta Ya existe!","danger")
        else:
            register.query()
            flash('Registro Exitosamente!',"success")

    return render_template("register.html")



@app.route("/perfil", methods=["GET", "POST"])
def perfil():
    if "logeado" in session:
        # Conectar a la base de datos
        cur = mysql.connection.cursor()

        # Realizar una consulta para obtener los datos del usuario actual
        #cur.execute("SELECT nombre, apellido, edad, fecha, correo, direccion, numero, usuario, tipocargo FROM users WHERE id = %s", (session["id"],))
        cur.execute('SELECT * FROM users WHERE id = %s',(session["id"],))
        usuario_actual = cur.fetchone()

        if request.method == "POST":
            # Obtener los datos proporcionados por el usuario
            nombre = request.form.get("nombre")
            apellido = request.form.get("apellido")
            edad = request.form.get("edad")
            fecha_nac = request.form.get("fecha")
            correo = request.form.get("correo")
            direccion = request.form.get("direccion")
            numero_tel = request.form.get("numero")
            usuario = request.form.get("usuario")
            password = request.form.get("contraseña")
            tipo_cargo = request.form.get("tipocargo")
            imagen = request.files["imagen"]  # Asegura que el campo se llame "imagen"
            imagen_filename = imagen.filename


            # Validar que el archivo sea una imagen
            if not is_valid(imagen_filename):
                flash("Por favor, sube una imagen válida (jpg, png, jpeg)")
            else:

                # SQL
                sql = "UPDATE users SET"

                # Construir la consulta de actualización dinámicamente
                valores = []
                if nombre:
                    sql += " nombre=%s,"
                    valores.append(nombre)
                if apellido:
                    sql += " apellido=%s,"
                    valores.append(apellido)
                if edad:
                    sql += " edad=%s,"
                    valores.append(edad)
                if fecha_nac:
                    sql += " fecha=%s,"
                    valores.append(fecha_nac)
                if correo:
                    sql += " correo=%s,"
                    valores.append(correo)
                if direccion:
                    sql += " direccion=%s,"
                    valores.append(direccion)
                if numero_tel:
                    sql += " numero=%s,"
                    valores.append(numero_tel)
                if usuario:
                    sql += " usuario=%s,"
                    valores.append(usuario)
                if password:
                    sql += " contraseña=%s,"
                    valores.append(password)
                if tipo_cargo:
                    sql += " tipocargo=%s,"
                    valores.append(tipo_cargo)
                if imagen:
                    now = datetime.now()
                    tiempo = now.strftime("%Y%H%M%S")
                    new_image = tiempo + imagen.filename
                    imagen.save("uploads/" + new_image)
                    sql += " imagen=%s,"
                    valores.append(new_image)
                    
                    # Eliminar la última coma de la consulta
                    sql = sql.rstrip(",")
                    
                    # Agregar la condición para actualizar un usuario específico
                    sql += " WHERE id=%s"
                    valores.append(session["id"])
                    
                    # Ejecutar la consulta de actualización
                    cur.execute(sql, tuple(valores))
                    mysql.connection.commit()   
        
            return render_template("profile.html", usuario=usuario_actual)
        return render_template("profile.html", usuario=usuario_actual)
    return redirect(url_for('logout'))

# func to check allow extensions
def allowed_image(filename):
    allowed_extensions = {"jpg", "jpeg", "png"}
    return "." in filename and filename.rsplit(".", 1)[1].lower() in allowed_extensions


# create object Custom for blue background
class CustomDocTemplate(BaseDocTemplate):
    def __init__(self, filename, **kwargs):
        super().__init__(filename, **kwargs)
        self.addPageTemplates(
            [PageTemplate(id="CustomTemplate", frames=[Frame(0, 0, 612, 792)])]
        )

@app.route("/generate_carnet", methods=["GET", "POST"])
def generate_carnet():
    """
    Genera un carnet de identificación para un usuario y lo guarda en la base de datos.

    Esta función crea un carnet de identificación único para un usuario proporcionado y lo almacena
    en la base de datos asociándolo con el usuario. El carnet se genera a partir del nombre, el apellido
    y, opcionalmente, algún otro atributo único del usuario. El carnet resultante se guarda en la base de datos
    y se asocia con el usuario.

    Args:
        usuario (str): El identificador único del usuario para el que se generará el carnet.
        nombre (str): El nombre del usuario, que puede ser parte de la información utilizada para generar el carnet.
        apellido (str): El apellido del usuario, que también puede ser parte de la información para el carnet.

    Returns:
        str: El carnet de identificación generado para el usuario.
    """

    if request.method == "POST":
        # Obtener la cedula del usuario desde el formulario
        cedula = request.form["cedula"]

        # Establecer conexión con la base de datos
        cursor = mysql.connection.cursor()

        # Realizar consulta SQL para obtener los datos del usuario
        query = f"SELECT nombre, tipocargo, usuario, imagen FROM users WHERE usuario = '{cedula}'"
        cursor.execute(query)
        usuario = cursor.fetchone()

        if usuario is None:
            flash("El Usuario no existe!")
            return redirect("/generate_carnet")

        nombre = usuario[0]
        tipo_cargo = usuario[1]
        cedula = usuario[2]
        imagen_usuario = usuario[3]

        # Generar el codigo de barras unico basado en la cedula
        barcode_path = f"uploads/carnets/barcode_{cedula}"
        code128_barcode = Code128(cedula, writer=ImageWriter())
        code128_barcode.save(barcode_path)

        # Crear el directorio "uploads/carnets" si no existe
        if not os.path.exists("uploads/carnets"):
            os.makedirs("uploads/carnets")

        # Generar el carnet PDF
        pdf_path = f"uploads/carnets/carnet_{cedula}.pdf"

        if os.path.exists(pdf_path):
            flash("Lo sentimos el carnet ya ha sido creado!")
            return redirect("/generate_carnet")

        # Definir estilos de texto
        styles = getSampleStyleSheet()
        titulo_style = styles["Heading1"]
        titulo_style.alignment = 1
        contenido_style = ParagraphStyle(
            name="contenido", parent=styles["BodyText"], alignment=1
        )

        # Crear elementos del carnet
        elements = []

        # Agregar Titulo
        titulo = Paragraph(
            "Universidad Politecnica Territorial Mario Briceño Iragory", titulo_style
        )
        elements.append(titulo)
        elements.append(Spacer(1, 12))

        # Agregar imagen del usuario
        imagen_path = os.path.join(app.config["CARPETA"], imagen_usuario)
        imagen = Image(imagen_path, width=200, height=200)
        elements.append(imagen)
        elements.append(Spacer(1, 12))

        # Agregar nombre, Cedula y tipo de cargo
        contenido = Paragraph(
            f"<br/><br/><b>Nombre:</b> {nombre}<br/><b>Cédula:</b> {cedula}<br/><b>Tipo de cargo:</b> {tipo_cargo}<br/><br/>",
            contenido_style,
        )
        elements.append(contenido)
        elements.append(Spacer(1, 12))

        # Agregar cÃ³digo de barras
        barcode_image_path = f"uploads/carnets/barcode_{cedula}.png"
        barcode_image = Image(barcode_image_path, width=250, height=50)
        elements.append(barcode_image)

        # Generar el carnet PDF
        doc = SimpleDocTemplate(pdf_path, pagesize=letter, canvasmaker=NumberedCanvas)
        doc.build(elements)

        # Devolver el carnet generado al cliente
        with open(pdf_path, "rb") as file:
            response = make_response(file.read())
            response.headers["Content-Type"] = "application/pdf"
            response.headers[
                "Content-Disposition"
            ] = f"inline; filename=carnet_{cedula}.pdf"

        return send_file(pdf_path, as_attachment=True)

    return render_template("generate_carnet.html")


def carnet_existe(cedula):
    """
    Verifica si existe un carnet asociado a una cédula en la base de datos.

    Esta función verifica si ya existe un carnet asociado a la cédula proporcionada en la base de datos
    de usuarios. Retorna True si se encuentra al menos un carnet asociado a la cédula, y False en caso contrario.

    Args:
        cedula (str): El número de cédula a verificar en la base de datos.

    Returns:
        bool: True si existe al menos un carnet asociado a la cédula dada en la base de datos, False en caso contrario.
    """
    # Establecer conexión con la base de datos
    cursor = mysql.connection.cursor()

    # Realizar consulta SQL para verificar si existe un carnet para la cédula dada
    query = f"SELECT COUNT(*) FROM users WHERE usuario = '{cedula}'"
    cursor.execute(query)
    count = cursor.fetchone()[0]

    # Si el resultado es mayor a cero, significa que ya existe un carnet para la cédula
    if count > 0:
        return True

    return False


# Task Route
@app.route('/new-task', methods=['POST'])
def newTask():
    """
    Crea una nueva tarea y la guarda en la base de datos.

    Esta función permite a un usuario autenticado crear una nueva tarea proporcionando un título y una descripción
    en el formulario POST. La tarea se asocia con el correo electrónico del usuario y se registra con la fecha y hora
    actual. Después de crear y guardar la tarea, redirige al usuario a la página de cuenta.

    Args:
        Ninguno (Los datos se toman de la sesión y el formulario POST).

    Returns:
        Después de crear y guardar con éxito la nueva tarea en la base de datos, redirige al usuario a la página de cuenta.
    """

    if 'logeado' in session:
        title = request.form['title']
        description = request.form['description']
        email = session['email']
        d = datetime.now()
        dateTask = d.strftime("%Y-%m-%d %H:%M:%S")

        if title and description and email:
            cur = mysql.connection.cursor()
            sql = "INSERT INTO tasks (email, title, description, date_task) VALUES (%s, %s, %s, %s)"
            data = (email, title, description, dateTask)
            cur.execute(sql, data)
            mysql.connection.commit()
        return redirect(url_for('cuenta'))


@app.route("/delete-task", methods=["POST"])
def deleteTask():
    """
    Elimina una tarea de la base de datos.

    Esta función permite eliminar una tarea específica de la base de datos en función del ID proporcionado
    en la solicitud POST. Después de eliminar la tarea, redirige al usuario a la página de cuenta.

    Args:
        Ninguno (Los datos se toman de la solicitud POST).

    Returns:
        Después de eliminar con éxito la tarea de la base de datos, redirige al usuario a la página de cuenta.
    """

    cur = mysql.connection.cursor()
    id = request.form['id']
    sql = "DELETE FROM tasks WHERE id = %s"
    data = (id,)
    cur.execute(sql, data)
    mysql.connection.commit()
    return redirect(url_for('cuenta'))


@app.route("/guardar_asistencia", methods=["POST"])
def guardar_asistencia():
    """
    Guarda la asistencia de un empleado en la base de datos.

    Si el usuario está autenticado, permite guardar la asistencia de un empleado en la base de datos.
    Esto se hace mediante una solicitud POST que incluye la fecha y el estado (por ejemplo, "presente" o "ausente")
    de la asistencia que se va a guardar.

    Args:
        Ninguno (Los datos se toman de la sesión y el formulario POST).

    Returns:
        Si se envía una solicitud POST válida y se guarda la asistencia correctamente, se redirige al usuario
        a la página de asistencia con un mensaje de éxito.
        Si se produce un error al guardar la asistencia, se muestra un mensaje de error y se revierte la
        transacción de la base de datos.
        Si el usuario no está autenticado, se redirige a la página de inicio de sesión.
    """

    if "logeado" in session:
        if request.method == "POST":
            date = request.form.get("date")
            status = request.form.get("status")

            # Lógica para guardar la asistencia en la base de datos
            cursor = mysql.connection.cursor()

            # Inserta los nuevos datos de asistencia
            insert_query = "INSERT INTO users_attendance (user_id, date, status) VALUES (%s, %s, %s)"
            data = (session["id"],date,status)

            try:
                cursor.execute(insert_query, data)
                mysql.connection.commit()
                flash("Asistencia guardada con éxito", "success")
            except Exception as e:
                mysql.connection.rollback()
                flash(f"Error al guardar la asistencia: {str(e)}", "danger")
        
            return redirect(url_for('asistencia'))

        return redirect(url_for('asistencia'))
    
    return url_for('login')



@app.route('/generar_informe_asistencia', methods=['GET', 'POST'])
def generar_informe_asistencia():
    """
    Genera un informe de asistencia para un empleado en función de la fecha seleccionada.

    Si el usuario está autenticado, permite generar un informe de asistencia para el empleado
    actual en función de la fecha proporcionada. El informe incluye el número de días de presencia
    y ausencia para ese empleado en el período especificado.

    Args:
        Ninguno (Los datos se toman de la sesión y el formulario POST).

    Returns:
        Si se envía una solicitud POST válida, se renderiza un informe de asistencia en HTML
        que muestra la presencia y la ausencia del empleado en la fecha seleccionada.
        Si se recibe una solicitud GET o no se proporciona una fecha válida, se muestra una página
        en blanco con el formulario para seleccionar la fecha.
    """

    if 'logeado' in session:
        if request.method == 'POST':
            #start_date = request.form.get('start')
            #end_date = request.form.get('end')
            date_time = request.form.get('date')

            # Lógica para obtener el informe de asistencia
            cursor = mysql.connection.cursor()

            query = """
            SELECT
                u.nombre AS Empleado,
                SUM(CASE WHEN ua.status = 'presente' THEN 1 ELSE 0 END) AS Presencia,
                SUM(CASE WHEN ua.status = 'ausente' THEN 1 ELSE 0 END) AS Ausencia
            FROM
                users_attendance ua
            INNER JOIN
                users u ON ua.user_id = u.id
            WHERE
                ua.user_id = %s AND ua.date >= %s 
            GROUP BY
                u.nombre;
            """

            cursor.execute(query, (session['id'], date_time))
            informe_asistencia = cursor.fetchall()
            informe_asistencia = [{'Empleado': row[0], 'Presencia': int(row[1]), 'Ausencia': int(row[2])} for row in informe_asistencia]

            return render_template('informe_asistencia.html', UserAsist=informe_asistencia)
        
        return render_template('informe_asistencia.html')
    
    return redirect(url_for('login'))


@app.route("/asistencia",methods=['GET'])
def asistencia():
    """
    Ruta de visualización de la página de asistencia.

    Esta función verifica si el usuario está autenticado mediante la sesión. Si el usuario está autenticado,
    muestra la página de asistencia. Si el usuario no está autenticado, redirige a la página de cierre de sesión.

    Returns:
        render_template: La página HTML de asistencia si el usuario está autenticado.
        redirect: Redirección a la página de cierre de sesión si el usuario no está autenticado.
    """

    if "logeado" in session:
        return render_template("asistencia.html")
    
    return redirect(url_for('logout'))

if __name__ == "__main__":
    app.run(debug=True)
