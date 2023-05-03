from flask import Flask, render_template, request, redirect, url_for, flash
from config import *
from flask_login import LoginManager, login_user, logout_user, login_required
from flask_wtf.csrf import CSRFProtect
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

@app.route('/')
def index():
    crearTablaUsers()
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
# @limiter.limit("10/minute")
def login():
    crearTablaUsers()
    if request.method == 'POST':
        # print(request.form['email'])
        # print(request.form['password'])
        user = User(0, request.form['email'], request.form['password'])
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
      ( %s, %s);
    """
    cursor.execute(sql,(email, password, nombre))
    con_bd.commit()
    return redirect(url_for('index'))
  else:
    return "Error"
  
@app.route('/consultar', methods=['GET', 'POST'])
def consultar():
    # debugger
    crearTablaReciboPublicoApartamento()
    cursor = con_bd.cursor()
    recibos = []
    if request.method == 'POST':
        form = request.form
        torre = form['torre']
        apartamento = form['apartamento']
        if torre and apartamento:
            import pdb; pdb.set_trace()
            try:
                sql = """
                SELECT
                    *
                FROM
                    recibo_publico_apartamento
                WHERE
                    torre = %s AND apartamento = %s;
                """
                cursor.execute(sql,(torre, apartamento))
                con_bd.commit()
                results = cursor.fetchall()
            except Exception as e:
                print(f'Error en la consulta, torre: {torre}, apartamento: {apartamento}' + e)
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
            print('Error en la consulta' + e)
            return redirect(request.referrer)
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

@app.route('/home')
@login_required
def home():
    return render_template('home.html')

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))


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