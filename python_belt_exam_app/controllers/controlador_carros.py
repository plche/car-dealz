from flask import flash, redirect, render_template, request, session
from python_belt_exam_app import app
from python_belt_exam_app.models.modelo_carros import Carro
from python_belt_exam_app.models.modelo_usuarios import Usuario


@app.route('/new', methods=["GET"])
def despliegaAddCarro():
    if 'email' in session:
        return render_template("addcar.html")
    else:
        return redirect('/')


@app.route('/new', methods=["POST"])
def registrarCarro():
    datosFormulario = request.form
    if not Carro.validarCarro(datosFormulario, "carro"):
        return redirect('/new')
    nuevoCarro = {
        "price": int(datosFormulario["price"]),
        "model": datosFormulario["model"],
        "make": datosFormulario["make"],
        "year": int(datosFormulario["year"]),
        "description": datosFormulario["description"],
        "slr_id": session["slr_id"],
        "byr_id": None,
    }
    resultado = Carro.agregarCarro(nuevoCarro)
    if type(resultado) is int and resultado != 0:
        return redirect('/dashboard')


@app.route('/edit/<id>', methods=["GET"])
def despliegaEditCarro(id):
    if 'email' in session:
        data = {
            "car_id": int(id)
        }
        carro = Carro.obtenerDetallesCarro(data)
        return render_template("updatecar.html", carro=carro)
    else:
        return redirect('/')


@app.route('/update/<id>', methods=["POST"])
def actualizarCarro(id):
    if 'email' in session:
        datosFormulario = request.form
        if not Carro.validarCarro(datosFormulario, "update"):
            return redirect('/edit/' + id)
        actualizadoCarro = {
            "car_id": int(id),
            "price": int(datosFormulario["price"]),
            "model": datosFormulario["model"],
            "make": datosFormulario["make"],
            "year": int(datosFormulario["year"]),
            "description": datosFormulario["description"]
        }
        resultado = Carro.modificarCarro(actualizadoCarro)
        if resultado is None:
            return redirect('/dashboard')
    else:
        return redirect('/')


@app.route('/show/<id>', methods=["GET"])
def despliegaDetallesCarro(id):
    if 'email' in session:
        data = {
            "car_id": int(id)
        }
        carro = Carro.obtenerDetallesCarro(data)
        dataUsuario = {
            "usr_id": carro["slr_id"]
        }
        usuarioSeller = Usuario.obtenerUsuarioPorId(dataUsuario)
        seller = usuarioSeller["nombre"] + " " + usuarioSeller["apellido"]
        return render_template("showcar.html", carro=carro, seller=seller)
    else:
        return redirect('/')


@app.route('/purchase/<car_id>/<byr_id>', methods=["POST"])
def comprarCarro(car_id, byr_id):
    if 'email' in session:
        data = {
            "car_id": int(car_id),
            "byr_id": int(byr_id)
        }
        resultado = Carro.actualizarCarro(data)
        print("controlador_carros:59:resultado:", resultado)
        return redirect('/dashboard')
    else:
        return redirect('/')

@app.route('/delete/<id>', methods=["POST"])
def eliminarCarro(id):
    if 'email' in session:
        data = {
            "car_id": int(id)
        }
        print("DATA VIENE ASI: ", data)
        resultado = Carro.removerCarro(data)
        print("ESTO VIENE DE ELIMINAR EL CARRO: ", resultado)
        return redirect('/dashboard')
    else:
        return redirect('/')
