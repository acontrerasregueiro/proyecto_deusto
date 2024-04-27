from flask import Flask, render_template,redirect
from flask import request
from flask import jsonify
import json
import fichero          #Realizamos las operaciones sobre el fichero

from jinja2 import Template

from flask_jwt_extended import create_access_token,create_refresh_token ,get_jwt_identity, jwt_required
from flask_jwt_extended import JWTManager
from flask import make_response
from flask_cors import CORS,cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

app.config["JWT_SECRET_KEY"] = "SECRETKEY"
jwt = JWTManager(app)

@app.route('/contenido', methods=['GET'])
def contenido():    
    data = fichero.leer_fichero()
    if isinstance(data,str):
        #Si nos devuelve un string ("error") es que no se encuentra el fichero
        return render_template('vacio.html')
    else:
        return render_template('contenido.html',data=data)

@app.route('/registrar', methods=['POST'])
def registrar():
    fichero.crear_fichero(request.form) 
    return jsonify(request.form), 200   

@app.route('/ver/<id>', methods = ['GET']) 
def ver(id): #Definimos una función llamada Inicio
    #Todos = Persona.leer_contacto('id', 'all') 
    #return render_template('/index.html', Todos = Todos, index_ver = index) #Retornornamos el template + Todos
    print('id : ', id)
    print('indice : ',fichero.buscar_registro(id))
    #datos = fichero.leer_registro(fichero.buscar_registro(id))
    #print(type(datos))
    #datos = json.loads(datos)
    #print(type(datos))
    datos = json.loads(fichero.buscar_registro(id))
    print('datos ' ,datos)
    return render_template('editar.html',datos = datos)   

@app.route('/', methods=['GET'])
def login():
    return render_template('index.html')

@app.route('/login', methods=['GET'])
def index():
    return render_template('login.html')


@app.route('/hello', methods=['POST','GET'])
def hello():
    user = request.form['name'] 
    password = request.form['password']
    if user != 'test' or password != 'test':
        return render_template('login.html')
    else:
        #Creamos el token
        access_token = create_access_token(identity=user)
        response = make_response(render_template('hello.html'))       
        response.set_cookie('access_token',access_token) 
        print(access_token)
        return response
    

@app.route('/holita', methods=['POST','GET'])
def holita():
    name = request.cookies.get('access_token')
    print(name)
    #return render_template('holita.html') 
    if name:
        return redirect("/protected")
    else:
        render_template('login.html')        

@app.route('/anadir', methods=['GET'])
def anadir():
    response = make_response(render_template('login.html')) 
    return response
    

@app.route('/user', methods=['GET'])
#@jwt_required()
def user():
    current_user = get_jwt_identity()
    return render_template('user.html')


@app.route('/register',methods=['GET'])
def register():
     return render_template('login.html')

@app.route('/protected', methods = ['GET','POST'])
#@jwt_required()
def protected():
    name = request.cookies.get('access_token')
    print(name)

    if name:
        return render_template('user.html')
    else:
        return render_template('login.html')


if __name__ == "__main__":    
    app.run(debug=True)