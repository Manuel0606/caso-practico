from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, flash
from config import *
from flask_login import LoginManager, current_user, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
from werkzeug.utils import secure_filename
import os
# from flask_limiter import Limiter
# from flask_limiter.util import get_remote_address

from models.ModelUser import ModelUser
from models.entities.User import User

app = Flask(__name__)

csrf = CSRFProtect()

con_bd = EstablecerConexion()

# limiter = Limiter(app=app, key_func=get_remote_address)

login_manager_app = LoginManager(app)

@login_manager_app.user_loader
def load_user(id):
    return ModelUser.get_by_id(con_bd, id)

# Constantes

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'pdf', 'doc', 'docx'}

# --------------------------------------------------
# Rutas de la aplicación
# --------------------------------------------------

# Root

@app.route('/')
def index():
    crearTablaUsers()
    return redirect(url_for('login'))

@app.route('/home')
@login_required
def home():
    return render_template('usuario.html')

@app.route('/apartamento')
@login_required
def apartamento():
    recibos = []
    data = {
        "recibos" : recibos
    }
    return render_template('apartamento.html', data=data)

@app.route('/torre')
@login_required
def torre():
    recibos = []
    data = {
        "recibos" : recibos
    }
    return render_template('torre.html', data=data)

@app.route('/login', methods=['GET', 'POST'])
# @limiter.limit("10/minute")
def login():
    crearTablaUsers()
    if request.method == 'POST':
        # print(request.form['email'])
        # print(request.form['password'])
        user = User(0, request.form['email'], request.form['password'], '0')
        logged_user = ModelUser.login(con_bd, user)
        if logged_user != None:
            if logged_user.password:
                login_user(logged_user)
                return redirect(url_for('home'))
            else:
                print('Contraseña invalida')
                return render_template('auth/login.html')
        else:
            print('Usuario no encontrado')
            return render_template('auth/login.html')
    else:
        return render_template('auth/login.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


@app.route('/new_user')
def new_user():
  return render_template('auth/new.html')

@app.route('/signup', methods=['POST'])
def add_user():
  crearTablaUsers()
  cursor = con_bd.cursor()
  form = request.form
  email = form['email']
  nombre = form['nombre']
  password = User.passwordHash(form['password'])
  if email and password:
    sql = """
    INSERT INTO
      users (
        email,
        password,
        nombre
      )
      VALUES
      ( %s, %s, %s);
    """
    cursor.execute(sql,(email, password, nombre))
    con_bd.commit()
    return redirect(url_for('index'))
  else:
    return "Error"
  
@app.route('/consultar', methods=['GET', 'POST'])
def consultar():
    crearTablaReciboPublicoApartamento()
    cursor = con_bd.cursor()
    if request.method == 'POST':
        form = request.form
        torre = form['torre']
        apartamento = form['apartamento']
        servicio_publico = form['servicio_publico']
        if torre and apartamento and (servicio_publico != 'Todos'):
            sql = """
                SELECT *
                FROM recibo_publico_apartamento
                WHERE torre = %s AND apartamento = %s AND servicio_publico = %s;
            """
            cursor.execute(sql,(torre, apartamento, servicio_publico))
            try:
                con_bd.commit()
                results = cursor.fetchall()
            except Exception as e:
                flash(f'Error en la consulta, torre: {torre}, apartamento: {apartamento}, servicio_publico: {servicio_publico}' + e)
                return redirect(request.referrer)
        elif torre and apartamento:
            sql = """
                SELECT *
                FROM recibo_publico_apartamento
                WHERE torre = %s AND apartamento = %s;
            """
            cursor.execute(sql,(torre, apartamento))
            try:
                con_bd.commit()
                results = cursor.fetchall()
            except Exception as e:
                flash(f'Error en la consulta, torre: {torre}, apartamento: {apartamento}' + e)
                return redirect(request.referrer)
        else:
            flash('Elige una torre y un apartamento')
            return redirect(request.referrer)
    else:
        try:
            sql = """
                SELECT *
                FROM recibo_publico_apartamento;
            """
            cursor.execute(sql)
            con_bd.commit()
            results = cursor.fetchall()
        except Exception as e:
            flash('Error en la consulta: ' + e)
            return redirect(request.referrer)
    recibos = []
    for row in results:
        recibo = {
            "id" : row[0],
            "torre" : row[1],
            "apartamento" : row[2],
            "servicio_publico" : row[3],
            "consumo" : row[4],
            "valor" : row[5],
            "fecha_corte" : row[6],
            "fecha_recibo" : row[7]
        }
        recibos.append(recibo)
    data = {
        "recibos" : recibos
    }
    return render_template('consultar.html', data=data)

@app.route('/crear_recibo_publico_apartamento', methods=['POST'])
@login_required
def crear_recibo_publico_apartamento():
    crearTablaReciboPublicoApartamento()
    if request.method == 'POST':
        form = request.form
        torre = form['torre']
        apartamento = form['apartamento']
        servicio_publico = form['servicio_publico']
        consumo = form['consumo']
        valor = form['valor']
        fecha_corte = form['fecha_corte']
        fecha_recibo = form['fecha_recibo']
        if torre and apartamento and servicio_publico and consumo and valor and fecha_corte and fecha_recibo:
            cursor = con_bd.cursor()
            try:
                sql = """
                INSERT INTO
                    recibo_publico_apartamento (
                        torre,
                        apartamento,
                        servicio_publico,
                        consumo,
                        valor,
                        fecha_corte,
                        fecha_recibo
                    )
                    VALUES
                    ( %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(sql,(torre, apartamento, servicio_publico, consumo, valor, fecha_corte, fecha_recibo))
                con_bd.commit()
                flash('Recibo Publico Apartamento creado exitosamente')
                return redirect(url_for('consultar'))
            except Exception as e:
                flash('Error en la consulta: ' + e)
    return redirect(request.referrer)

@app.route('/crear_recibo_publico_torre', methods=['POST'])
@login_required
def crear_recibo_publico_torre():
    crearTablaReciboPublicoTorre()
    if request.method == 'POST':
        form = request.form
        numero_torre = form['numero_torre']
        servicio_publico = form['servicio_publico']
        consumo = form['consumo']
        valor = form['valor']
        fecha_corte = form['fecha_corte']
        fecha_recibo = form['fecha_recibo']
        foto_servicio_publico = request.files['foto_servicio_publico'] if 'foto_servicio_publico' in request.files else None
        
        if foto_servicio_publico:
            filename = secure_filename(foto_servicio_publico.filename)
            if allowed_file(filename) == False:
                flash('Error Al Crear El Post: El Archivo No Es Valido', 'danger')
                return redirect(request.referrer)
            base_path = os.path.dirname(__file__)
            filename_complete = create_filename_complete(filename)
            createUploadsFolder()
            foto_servicio_publico_route = os.path.join(base_path, app.config['UPLOAD_FOLDER'], filename_complete)
            try:
                foto_servicio_publico.save(foto_servicio_publico_route)
            except Exception as e:
                flash('Error Al Crear El Post: ' + str(e), 'danger')
        else:
            filename_complete = ""

        if numero_torre and servicio_publico and consumo and valor and fecha_corte and fecha_recibo:
            cursor = con_bd.cursor()
            try:
                sql = """
                INSERT INTO
                    recibo_publico_torre (
                        numero_torre,
                        servicio_publico,
                        consumo,
                        valor,
                        fecha_corte,
                        fecha_recibo,
                        foto_servicio_publico
                    )
                    VALUES
                    ( %s, %s, %s, %s, %s, %s, %s);
                """
                cursor.execute(sql,(numero_torre, servicio_publico, consumo, valor, fecha_corte, fecha_recibo, filename_complete))
                con_bd.commit()
                crear_recibos_publicos_apartamentos(numero_torre, servicio_publico, fecha_corte, fecha_recibo)
                flash('Recibo Publico Torre Creado Correctamente', 'success')
                return redirect(url_for('consultar'))
            except Exception as e:
                flash('Error en la consulta: ' + e)
    return redirect(request.referrer)

def crear_recibos_publicos_apartamentos(numero_torre, servicio_publico, fecha_corte, fecha_recibo):
    cursor = con_bd.cursor()
    sql = """
        INSERT INTO
            recibo_publico_apartamento (
                torre,
                apartamento,
                servicio_publico,
                fecha_corte,
                fecha_recibo
            )
            VALUES
            ( %s, %s, %s, %s, %s);
    """
    try:
        for i in range(1, 13):
            cursor.execute(sql,(numero_torre, str(i), servicio_publico, fecha_corte, fecha_recibo))
            con_bd.commit()
    except Exception as e:
        flash('Error en la creación de recibos publicos por apartamento: ' + e)

def create_filename_complete(filename):
    now = datetime.now()
    short_date = now.strftime("%Y%m%d")
    filename_complete = f"{short_date}_{str(current_user.id)}_{filename}"
    return filename_complete

def allowed_file(file):
    file = file.split('.')
    if file[1] in ALLOWED_EXTENSIONS:
        return True
    return False

def createUploadsFolder():
    base_path = os.path.dirname(__file__)
    uploads_folder = os.path.join(base_path, app.config['UPLOAD_FOLDER'])
    if not os.path.exists(uploads_folder):
        os.makedirs(uploads_folder)



def crearTablaUsers():
    cursor = con_bd.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users(
        id serial NOT NULL,
        email character varying(30),
        password character varying(160),
        nombre character varying(30),
        tipo_usuario character varying(30),
        CONSTRAINT pk_user_id PRIMARY KEY (ID)
        );
    ''')
    con_bd.commit()

def crearTablaReciboPublicoApartamento():
    cursor = con_bd.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recibo_publico_apartamento(
        id serial NOT NULL,
        torre character varying(30),
        apartamento character varying(30),
        servicio_publico character varying(30),
        consumo integer,
        valor integer,
        fecha_corte timestamp without time zone,
        fecha_recibo timestamp without time zone,
        CONSTRAINT pk_recibo_publico_apartamento_id PRIMARY KEY (ID)
        );
    ''')
    con_bd.commit()

def crearTablaReciboPublicoTorre():
    cursor = con_bd.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS recibo_publico_torre(
        id serial NOT NULL,
        numero_torre character varying(30),
        servicio_publico character varying(30),
        consumo integer,
        valor integer,
        fecha_corte timestamp without time zone,
        fecha_recibo timestamp without time zone,
        foto_servicio_publico BYTEA,
        CONSTRAINT pk_recibo_publico_torre_id PRIMARY KEY (ID)
        );
    ''')
    con_bd.commit()

def status_401(error):
    return redirect(url_for('login'))
    # return "<h1>Acceso invalido</h1>", 401

def status_404(error):
    return "<h1>Página no encontrada</h1>", 404

if __name__ == '__main__':
    app.config.from_object(config['development'])
    csrf.init_app(app)
    app.register_error_handler(401, status_401)
    app.register_error_handler(404, status_404)
    app.run(port=5004)