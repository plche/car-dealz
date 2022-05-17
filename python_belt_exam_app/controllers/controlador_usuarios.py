from flask import render_template, request, redirect, session, flash
from python_belt_exam_app import app
from python_belt_exam_app.models.modelo_carros import Carro
from python_belt_exam_app.models.modelo_usuarios import Usuario
from flask_bcrypt import Bcrypt

bcrypt = Bcrypt(app)


@app.route('/', methods=["GET"])
def despliegaRegistroLogin():
    return render_template("index.html")


@app.route('/dashboard', methods=["GET"])
def despliegaDashboard():
    if 'email' in session:
        carros = Carro.obtenerCarros()
        return render_template("dashboard.html", carros=carros)
    else:
        return redirect('/')


@app.route('/registroUsuario', methods=["POST"])
def registrarUsuario():
    datosFormulario = request.form
    if not Usuario.validarUsuario(datosFormulario, "register"):
        return redirect('/')
    valUser = {
        "email": datosFormulario["email"]
    }
    if Usuario.validarRegistrado(valUser):
        flash("Dirección de correo electrónico registrada!", "register")
        return redirect('/')
    encryptedPass = bcrypt.generate_password_hash(datosFormulario["password"])
    nuevoUsuario = {
        "nombre": datosFormulario["nombre"],
        "apellido": datosFormulario["apellido"],
        "email": datosFormulario["email"],
        "password": encryptedPass,
    }
    session["nombre"] = nuevoUsuario["nombre"]
    session["apellido"] = nuevoUsuario["apellido"]
    session["email"] = nuevoUsuario["email"]
    resultado = Usuario.agregaUsuario(nuevoUsuario)
    session["usr_id"] = resultado
    session["slr_id"] = resultado
    if type(resultado) is int and resultado != 0:
        return redirect('/dashboard')


@app.route('/login', methods=["POST"])
def loginUsuario():
    datosFormulario = request.form
    if not Usuario.validarUsuario(datosFormulario, "login"):
        return redirect('/')
    valUser = {
        "email": datosFormulario["loginUsuario"]
    }
    if not Usuario.validarRegistrado(valUser):
        flash("Dirección de correo electrónico no registrada!", "login")
        return redirect('/')

    tryUser = datosFormulario["loginUsuario"]
    tryPass = datosFormulario["passwordUsuario"]
    usuario = {
        "email": tryUser,
    }

    resultado = Usuario.verificaUsuario(usuario)

    if not bcrypt.check_password_hash(resultado.password, tryPass):
        flash("Contraseña incorrecta", "login")
        return redirect('/')
    else:
        session["nombre"] = resultado.nombre
        session["apellido"] = resultado.apellido
        session["email"] = resultado.email
        session["usr_id"] = resultado.usr_id
        session["slr_id"] = resultado.usr_id
        return redirect('/dashboard')


@app.route('/user/<id>', methods=["GET"])
def despliegaComprasUsuario(id):
    usr_id = int(id)
    if 'email' in session and session["usr_id"] == usr_id:
        data = {
            "usr_id": usr_id
        }
        carrosComprados = Carro.obtenerCarrosComprados(data)
        return render_template("usercar.html", carros=carrosComprados)
    else:
        return redirect('/dashboard')


@app.route('/logout', methods=["GET"])
def logoutUsuario():
    session.clear()
    return redirect('/')
