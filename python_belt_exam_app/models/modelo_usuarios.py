import re
from flask import flash
from python_belt_exam_app.config.mysqlconnection import connectToMySQL

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
NOMBRE_APELLIDO_REGEX = re.compile(
    r'^[a-zA-ZÀ-ÿ\u00f1\u00d1][a-zA-ZÀ-ÿ\u00f1\u00d1]+$')  # Al menos dos caracteres, considerando alfabeto español
PASSWORD_REGEX = re.compile(r'^(?=.*[A-Z])(?=.*\d)[a-zA-Z\d]{1,}$')  # Al menos una mayúscula y 1 dígito


class Usuario:
    def __init__(self, usr_id, nombre, apellido, email, password, created_at, updated_at):
        self.usr_id = usr_id
        self.nombre = nombre
        self.apellido = apellido
        self.email = email
        self.password = password
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def agregaUsuario(cls, nuevoUsuario):
        query = "INSERT INTO usuarios(nombre, apellido, email, password) VALUES(%(nombre)s, %(apellido)s, %(email)s, %(password)s);"
        return connectToMySQL("python_belt_exam").query_db(query, nuevoUsuario)

    @classmethod
    def updateUsuario(cls, usuario):
        query = "UPDATE usuarios SET nombre = %(nombre)s, apellido = %(apellido)s, email = %(email)s WHERE usr_id = %(usr_id)s;"
        queryResult = connectToMySQL("python_belt_exam").query_db(query, usuario)
        print(f'Resultado UPDATE: {queryResult}')
        return queryResult

    @classmethod
    def verificaUsuario(cls, usuario):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL("python_belt_exam").query_db(query, usuario)
        if len(resultado) > 0:
            return Usuario(resultado[0]["usr_id"], resultado[0]["nombre"], resultado[0]["apellido"],
                           resultado[0]["email"], resultado[0]["password"], resultado[0]["created_at"],
                           resultado[0]["updated_at"])
        else:
            return None

    @classmethod
    def obtenerDatosUsuario(cls, usuario):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        queryResult = connectToMySQL("python_belt_exam").query_db(query, usuario)
        return queryResult[0] if len(queryResult) else None

    @classmethod
    def obtenerUsuarioPorId(cls, usuario):
        query = "SELECT * FROM usuarios WHERE usr_id = %(usr_id)s;"
        queryResult = connectToMySQL("python_belt_exam").query_db(query, usuario)
        return queryResult[0] if len(queryResult) else None

    @classmethod
    def validarRegistrado(cls, usuario):
        query = "SELECT * FROM usuarios WHERE email = %(email)s;"
        resultado = connectToMySQL("python_belt_exam").query_db(query, usuario)
        return len(resultado) > 0

    @classmethod
    def validarUpdateEmail(cls, usuario):
        query = "SELECT * FROM usuarios WHERE email = %(email)s AND usr_id <> %(usr_id)s;"
        resultado = connectToMySQL("python_belt_exam").query_db(query, usuario)
        return len(resultado) > 0

    @staticmethod
    def validarUsuario(usuario, formulario):
        es_valido = True  # asumimos que esto es true
        if formulario == "register":
            if len(usuario['nombre']) < 3:
                flash("El Nombre debe ser al menos de 3 caracteres.", formulario)
                es_valido = False
            elif not validarNombreApellido(usuario['nombre']):
                flash("El Nombre debe ser solo letras.", formulario)
                es_valido = False
            if len(usuario['apellido']) < 3:
                flash("El Apellido debe ser al menos de 3 caracteres.", formulario)
                es_valido = False
            elif not validarNombreApellido(usuario['apellido']):
                flash("El Apellido debe ser solo letras.", formulario)
                es_valido = False
            if usuario['password'] != usuario['cpassword']:
                flash("La Contraseña no coincide.", formulario)
                es_valido = False
            if not EMAIL_REGEX.match(usuario['email']):
                flash("Dirección de correo electrónico invalida!", formulario)
                es_valido = False
            if len(usuario['password']) < 8:
                flash("La Contraseña debe ser al menos de 8 caracteres.", formulario)
                es_valido = False
            elif not validarPassword(usuario['password']):
                flash("La Contraseña debe tener al menos un dígito y una mayúscula.", formulario)
                es_valido = False
        elif formulario == "login":
            if not EMAIL_REGEX.match(usuario['loginUsuario']):
                flash("Dirección de correo electrónico invalida!", formulario)
                es_valido = False
        elif formulario == "update":
            if len(usuario['nombre']) < 3:
                flash("El Nombre debe ser al menos de 3 caracteres.", formulario)
                es_valido = False
            elif not validarNombreApellido(usuario['nombre']):
                flash("El Nombre debe ser solo letras.", formulario)
                es_valido = False
            if len(usuario['apellido']) < 3:
                flash("El Apellido debe ser al menos de 3 caracteres.", formulario)
                es_valido = False
            elif not validarNombreApellido(usuario['apellido']):
                flash("El Apellido debe ser solo letras.", formulario)
                es_valido = False
            if not EMAIL_REGEX.match(usuario['email']):
                flash("Dirección de correo electrónico invalida!", formulario)
                es_valido = False
        return es_valido


def validarNombreApellido(data):
    es_valido = True
    if not NOMBRE_APELLIDO_REGEX.match(data):
        es_valido = False
    return es_valido


def validarPassword(data):
    es_valido = True
    if not PASSWORD_REGEX.match(data):
        es_valido = False
    return es_valido
