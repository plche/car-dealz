from flask import flash
from python_belt_exam_app.config.mysqlconnection import connectToMySQL


class Carro:
    def __init__(self, car_id, price, model, make, year, description, slr_id, byr_id, created_at, updated_at):
        self.car_id = car_id
        self.price = price
        self.model = model
        self.make = make
        self.year = year
        self.description = description
        self.slr_id = slr_id
        self.byr_id = byr_id
        self.created_at = created_at
        self.updated_at = updated_at

    @classmethod
    def agregarCarro(cls, nuevoCarro):
        query = "INSERT INTO carros(price, model, make, year, description, slr_id, byr_id) VALUES(%(price)s, %(model)s, %(make)s, %(year)s, %(description)s, %(slr_id)s, %(byr_id)s);"
        return connectToMySQL("python_belt_exam").query_db(query, nuevoCarro)

    @classmethod
    def obtenerCarros(cls):
        query = "SELECT * FROM carros, usuarios WHERE slr_id = usr_id;"
        return connectToMySQL("python_belt_exam").query_db(query)

    @classmethod
    def obtenerCarrosComprados(cls, data):
        query = "SELECT * FROM carros WHERE byr_id = %(usr_id)s;"
        return connectToMySQL("python_belt_exam").query_db(query, data)

    @staticmethod
    def validarCarro(carro, formulario):
        es_valido = True  # asumimos que esto es true
        if formulario == "carro" or formulario == "update":
            if len(carro['price']) < 1:
                flash("El Precio debe ser proporcionado.", formulario)
                es_valido = False
            elif int(carro['price']) < 1:
                flash("El precio debe ser al menos mayor que 0.", formulario)
                es_valido = False
            if len(carro['model']) < 1:
                flash("El Modelo debe ser proporcionado.", formulario)
                es_valido = False
            if len(carro['make']) < 1:
                flash("El Fabricante debe ser proporcionado.", formulario)
                es_valido = False
            if len(carro['year']) < 1:
                flash("El Año debe ser proporcionado.", formulario)
                es_valido = False
            elif int(carro['year']) < 1:
                flash("El Año debe ser al menos mayor uqe 0.", formulario)
                es_valido = False
            if len(carro['description']) < 1:
                flash("La Descripción debe ser proporcionada.", formulario)
                es_valido = False
        return es_valido

    @classmethod
    def obtenerDetallesCarro(cls, data):
        query = "SELECT * FROM carros WHERE car_id = %(car_id)s;"
        queryResult = connectToMySQL("python_belt_exam").query_db(query, data)
        return queryResult[0] if len(queryResult) else None

    @classmethod
    def actualizarCarro(cls, data):
        query = "UPDATE carros SET byr_id = %(byr_id)s WHERE car_id = %(car_id)s;"
        queryResult = connectToMySQL("python_belt_exam").query_db(query, data)
        print(f'Resultado UPDATE: {queryResult}')
        return queryResult

    @classmethod
    def modificarCarro(cls, data):
        query = "UPDATE carros SET price = %(price)s, model = %(model)s, make = %(make)s, year = %(year)s, description = %(description)s WHERE car_id = %(car_id)s;"
        queryResult = connectToMySQL("python_belt_exam").query_db(query, data)
        print(f'Resultado UPDATE: {queryResult}')
        return queryResult

    @classmethod
    def removerCarro(cls, data):
        query = "DELETE FROM carros WHERE car_id = %(car_id)s;"
        try:
            queryResult = connectToMySQL("python_belt_exam").query_db(query, data)
        except:
            return None
        else:
            return queryResult
