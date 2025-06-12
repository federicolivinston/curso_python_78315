import secrets
import string

#################################################################################################
# Este modulo contiene los modelos de datos de User y Customer
#################################################################################################

# User contiene el modelo de user
# atributos: 
# user: nombre de usuario (unico en la base)
# name: nombre de la persona dueña del usuario
# password: contraseña de acceso a la app
# id: identificador en teoria unico pero es no se implemento
# ademas implementa los metodos default de init, y str y se agregaron los metodos:
# to_dict: tranforma el objeto en diccionario
# generate_id: genera una cadena de 6 caracteres random a usar como identificador unico (faltaria validar esto ultimo)
# todos los geters

class User:

    unique_index = "user"

    def __init__(self, user, name, password, id=None):
        if id is None:
            self.__id = self._generate_id()
        else:
            self.__id = id
        self.__user=user
        self.__name=name
        self.__password=password
    
    def __str__(self):
        return f"{self.__user:<10}|  {self.__name:<50}|  {self.__password}"

    # metodos auxiliares
    def to_dict(self):
        return {
            "id": self.__id,
            "user": self.__user,
            "name": self.__name,
            "password": self.__password
        }
        
    def _generate_id(self):
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for _ in range(8))    
    
    # getters
    def get_id(self):
        return self.__id

    def get_user(self):
        return self.__user

    def get_name(self):
        return self.__name

    def get_password(self):
        return self.__password


    
# User contiene el modelo de customer (clientes)
# atributos: 
# dni: documento de identificacion del cliente (unico en la base)
# name: nombre de la persona dueña del usuario
# address: direccion fisica del cliente
# statua: indica si el cliente esta activo o no
# id: identificador en teoria unico pero es no se implemento
# ademas implementa los metodos default de init, y str y se agregaron los metodos:
# to_dict: tranforma el objeto en diccionario
# generate_id: genera una cadena de 6 caracteres random a usar como identificador unico (faltaria validar esto ultimo)
# todos los geters

class Customer:

    unique_index = "dni"

    def __init__(self, name, dni, address, status, id=None):
        self.__id = id if id is not None else self._generate_id()
        self.__name = name
        self.__dni = dni
        self.__address = address
        self.__status = status

    def __str__(self):
        return f"{self.__dni:<10}|  {self.__name:<50}|  {self.__address:<50}|  {self.__status:<10}"

    # metodos auxiliares
    def _generate_id(self):
        chars = string.ascii_letters + string.digits
        return ''.join(secrets.choice(chars) for _ in range(8))

    def to_dict(self):
        return {
            "id": self.__id,
            "name": self.__name,
            "dni": self.__dni,
            "address": self.__address,
            "status": self.__status
        }

    # getters
    def get_id(self):
        return self.__id

    def get_name(self):
        return self.__name

    def get_dni(self):
        return self.__dni

    def get_address(self):
        return self.__address

    def get_status(self):
        return self.__status


def crear_objeto(class_name, data):
    clases = {
        "users": User,
        "customers": Customer
    }

    clase = clases.get(class_name)
    if clase is None:
        raise ValueError(f"No existe la clase con nombre '{class_name}'")

    return clase(**data)