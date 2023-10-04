# Database Querys-Connections
from config import *

class Register:
    """ Register UPTT """
    def __init__(self,nombre,apellido,edad,fecha,correo,direccion,numero,usuario,contraseña,tipocargo,imagen):
        self.nombre = nombre
        self.apellido = apellido
        self.edad = edad
        self.fecha = fecha
        self.correo = correo
        self.direccion = direccion
        self.numero = numero
        self.usuario = usuario
        self.contraseña = contraseña
        self.tipocargo = tipocargo
        self.imagen = imagen

    def check_user(self):
        cursor = mysql.connection.cursor()

        cursor.execute('SELECT * FROM users WHERE usuario = %s OR correo = %s OR numero = %s',(self.usuario,self.correo,self.numero,))
        
        ExistUser = cursor.fetchone()
        if ExistUser:
            return True

    def query(self):
        # cursor to connect to Database
        cursor = mysql.connection.cursor()
        
        # Image proccessing
        now = datetime.now() # actual hour

        TimeStamp = now.strftime("%Y%H%M%S")
        name_image = TimeStamp + self.imagen.filename
         
        # Password Encrypt
        hashed_password = bcrypt.generate_password_hash(self.contraseña).decode('utf-8')
         
        # save it in uploads folder
        self.imagen.save('uploads/' + name_image)

        sql_query = """
            INSERT INTO users
            (
                nombre,
                apellido,
                edad,
                fecha,
                correo,
                direccion,
                numero,
                usuario,
                contraseña,
                tipocargo,
                imagen
            ) VALUES(%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
            """

        values = (
                self.nombre,
                self.apellido,
                self.edad,
                self.fecha,
                self.correo,
                self.direccion,
                self.numero,
                self.usuario,
                hashed_password,
                self.tipocargo,
                name_image
            )
            
        # commit
        cursor.execute(sql_query,values)
        mysql.connection.commit()


class Update:
    def __init__(self):
        pass