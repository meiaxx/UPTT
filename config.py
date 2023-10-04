# Imports #
from flask import (
    Flask,
    render_template,
    request,
    redirect,
    url_for,
    session,
    flash,
    send_file,
    send_from_directory,
    make_response,
    jsonify,
)
import MySQLdb.cursors
from flask_mysqldb import MySQL
from flask_mail import Mail, Message
import os
import random
import string
import uuid
from datetime import datetime,timedelta
import pytz
from flask_bcrypt import Bcrypt
import time


# reportlab
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.platypus import (
    SimpleDocTemplate,
    Paragraph,
    Spacer,
    Image,
    BaseDocTemplate,
    Frame,
    PageTemplate,
)

from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
import barcode
from barcode import Code128
from barcode.writer import ImageWriter
from reportlab.lib.units import inch
from reportlab.pdfgen.canvas import Canvas
import os

# all password character's
# this is for generate key
characters = string.digits + string.ascii_letters + string.punctuation
length = 32

# start app
app = Flask(__name__)

# security anti-CSRF
app.secret_key = "".join(random.sample(characters, length))

# MYSQL DB config
app.config["MYSQL_HOST"] = "127.0.0.1"
app.config["MYSQL_USER"] = "root"
app.config["MYSQL_PASSWORD"] = "password"
app.config["MYSQL_DB"] = "uptt"

mysql = MySQL(app)

# Email Config
app.config["MAIL_SERVER"] = "smtp.gmail.com"
app.config["MAIL_PORT"] = 587
app.config["MAIL_USE_SSL"] = False
app.config["MAIL_USERNAME"] = "upttinfo@gmail.com"  # h4A7zhhchkTCz9L
app.config["MAIL_PASSWORD"] = "dwjedtkldbdjwkvk"  # upttinfo@gmail.com
app.config["MAIL_USE_TLS"] = True

mail = Mail(app)

# Bcrypt
bcrypt = Bcrypt(app)

# Upload Folder
CARPETA = os.path.join("uploads")
app.config["CARPETA"] = CARPETA


from werkzeug.utils import secure_filename

# Secure Image filename
def is_valid(filename):
    """ Check valid image type filename """
    allowed_extensions = {"jpg", "jpeg", "png", "gif"}
    filename = secure_filename(filename)
    file_extension = filename.rsplit(".", 1)[-1].lower()
    if file_extension in allowed_extensions:
        return True
    return False
