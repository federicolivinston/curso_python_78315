import json
import os
from .ddbb_models import crear_objeto

#################################################################################################
# Este modulo maneja el acceso a los archivos json que constituyen la base de datos persistente
# contiene una clase ddbb_handler que trata de emular los metodos de una ddbb con los metodos:
# get_table_element: trae un solo elemento filtrado por algun dato (ej: user con id=aaaaaa)
# get_table_elements trae todos los elementos que correspondan a un filtro 
#   (ej: customers con status activo) si no tiene filtro trae todos
# add_table_element: recibe un diccionario con los datos y lo agrega al json correspondiente 
#   si no existe
#################################################################################################

class ddbb_handler:

    # lesta de tablas existentes
    db_list = {
        "users": "users.json",
        "customers":"customers.json"
    }

    # al crear la base se le debe indicar el path fisico de la base
    def __init__(self,db_path):
        self.db_path = db_path
        if not os.path.isdir(self.db_path):
            raise Exception("No es posible conectarse a la Base de Datos.")

    # recibe un nombre de tabla y verifica que exista si existe retorna
    # el nombre del json asociado
    def _get_table(self, table):
        if table in self.db_list:
            return os.path.join(self.db_path, self.db_list[table])
        else:
            raise Exception(f"No existe la tabla: {table}")
    
    # recibe un nombre de tabla, llama a la funcion para recuperar el archivo, 
    # verifica que el json exista, lo lee y retorna un objeto con todos 
    # los datos de la tabla
    def _get_table_data(self,table):
        file_path = self._get_table(table)

        if not os.path.isfile(file_path):
            raise Exception(f"No es posible acceder a la tabla: {table}")
        
        with open(file_path, 'r', encoding='utf-8') as data_table:
            try:
                return json.load(data_table)
            except json.JSONDecodeError:
                raise Exception(f"Error al leer los datos de la tabla: {table}")

    # recibe una tabla y un diccionario de filtros, pide los datos de la tabla y 
    # filtra el primer elemento que cumpla con los mismos, si no encuentra ninguno 
    # devuelve None
    def get_table_element(self, table, filters):

        if not isinstance(filters, dict):
            raise ValueError("El parámetro 'filters' debe ser un diccionario.")
        
        data = self._get_table_data(table)

        for element in data:
            if all(element.get(key) == value for key, value in filters.items()):
                return crear_objeto(table, element)

        return None
    
    # recibe una tabla y un diccionario de filtros, pide los datos de la tabla y 
    # filtra todos los elementos que cumplan con los mismos, si no encuentra ninguno 
    # devuelve None y si el diccionario de filtros viene vacio retorna todos los elementos
    def get_table_elements(self, table, filters):

        if not isinstance(filters, dict):
            raise ValueError("El parámetro 'filters' debe ser un diccionario.")

        data = self._get_table_data(table)

        if not filters:
            return [crear_objeto(table, element) for element in data]
        
        resultados = []

        for element in data:
            if all(element.get(key) == value for key, value in filters.items()):
                element = crear_objeto(table, element)
                resultados.append(element)

        return resultados

    # recibe una tabla y un diccionario con los datos de un elemento a agrgar a la tabla, 
    # verifica que el elemento no este en la tabla por el campo unique, si no existe lo agrega a la tabla   
    def add_table_element(self, table, data_dict):

        new_element = crear_objeto(table, data_dict)  # instancia
        unique_value = getattr(new_element, "unique_index", None)
        new_data_dict = new_element.to_dict()

        if not unique_value:
            return self.__insert_raw(table, new_data_dict)

        existing_data = self._get_table_data(table)
        for item in existing_data:
            if item.get(unique_value) == unique_value:
                return False

        return self.__insert_raw(table, new_data_dict)

    # recibe una tabla y un diccionario con datos, lee la tabla, agrega el elemento 
    # con los datos del diccionario y actualiza el archivo con el nuevo json
    def __insert_raw(self, table, obj_dict):
        data = self._get_table_data(table)
        data.append(obj_dict)
        file_path = self._get_table(table)
        with open(file_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, ensure_ascii=False, indent=4)
        return True
