import os

######################################################################################
# este modulo maneja las acciones del flujo de la app, contiene las acciones 
# principales de logIn, logOut, traer listados de datos y pedir los datos para
# dar de alta usuarios o clientes
######################################################################################

# Esta variable se utiliza para controlar si hay un usuario logueado o no 
# y mostrar las opciones del menu ademas de la bienvenida
glb_usuario_logueado=None

############################################################################
# Funciones auxiliares
############################################################################

# Esta funcion solo limpia la pantalla
def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

# Esta funcion valida que una cadena de caracteres tenga al menos una letra y un numero
def validar_letra_y_numero(cadena):
    tiene_letra = any(c.isalpha() for c in cadena)
    tiene_numero = any(c.isdigit() for c in cadena)
    return tiene_letra and tiene_numero

######################################################################################
# Funciones primarias para realizar acciones
######################################################################################

# Esta funcion desloguea al usuario
def log_out(usuario_logueado):
    opcion=input("Desea salir de la aplicacion? (y/n)")
    if opcion!="y":
        return usuario_logueado
    return None
       
# Esta funcion solicita usuario y pwd, verifica los datos y loguea al usuario
def log_in(database):

    limpiar_pantalla()
    user=input("Ingrese su Usuario: ").lower()
    password=input("Ingrese su Clave: ")
    try:
        usuario=database.get_table_element("users", {"user": user, "password":password})
        if usuario is None:
            print("Usuario o Clave incorrentos, intentelo nuevamente.")
            input("Presione Enter para continuar.")
            return None
    except Exception as e:
        print("Usuario o Clave incorrentos, intentelo nuevamente.")
        input("Presione Enter para continuar.")
        return None
    return usuario

# Esta funcion maneja el menu y la seleccion de opciones del mismo
def elegir_opcion(usuario_logueado):
    limpiar_pantalla()
    if usuario_logueado is not None:
        print(f"Bienvenido:",usuario_logueado.get_name())
        print()
    print("Menu de opciones:")
    if usuario_logueado is not None:
        print("1. Registrar Usuario.")
        print("2. Mostrar Usuarios.")
        print("3. Registrar Cliente.")
        print("4. Mostrar Clientes.")
        print("5. Mostrar Clientes Activos.")
        print("11. LogOut.")
        opciones=[1,2,3,4,5,11]
    else:
        print("10. LogIn.")
        print("99. Salir de la aplicacion.")
        opciones=[10,99]
    

    try:
        seleccion = int(input("Ingrese una opcion: "))
        if (seleccion in opciones):
            return seleccion
        else:
            return 0
    except:
        return 0
    
# Esta funcion recorre la lista de usuarios y 
# muestra la lista de usuarios por pantalla con todos sus datos
def mostrar_usuarios(database):
    limpiar_pantalla()
    print()
    print("Listado de Usuarios activos:")
    print()
    print(f"{'Usuario':<10}|  {'Nombre y Apellido':<50}|  {'Clave'}")
    print("-" * 90)  # Línea divisoria
    lista_usuarios=database.get_table_elements("users",{})
    for usuario in lista_usuarios:
        print(usuario)
    print()
    print()    
    input("Presione Enter para continuar.")


# Esta funcion recorre la lista de usuarios y 
# muestra la lista de usuarios por pantalla con todos sus datos
def mostrar_clientes(database,solo_activos=False):
    limpiar_pantalla()
    print()
    if solo_activos:
        print("Listado de Clientes activos:")
        filters={"status":"activo"}
    else:
        print("Listado completo de Clientes:")
        filters={}
    print()
    print(f"{'Cliente':<10}|  {'Nombre y Apellido':<50}|  {'direccion':<50}|  {'Estado'}")
    print("-" * 90)  # Línea divisoria
    lista_clientes=database.get_table_elements("customers",filters)
    for cliente in lista_clientes:
        print(cliente)
    print()
    print()    
    input("Presione Enter para continuar.")

# Esta funcion solicita el ingreso de los datos del usuario, 
# realiza las validaciones correspondientes y lo da de alta en la base de usuarios
def registrar_usuario(database):

    #solicita y valida el usuario (debe ser unico contener solo letras y entre 5 y 8 caracteres)
    limpiar_pantalla()
    while True:
        user=input("Ingrese el Usuario: ").lower()
        usuario_existente=database.get_table_element("users",{"user":user})
        if usuario_existente is not None:
            limpiar_pantalla()
            print(f"El Usuario: {user} ya existe, por favor ingrese uno que no exista.")
        elif not (len(user) >= 5 and len(user) <= 8 and user.isalpha()):
            limpiar_pantalla()
            print(f"El Usuario debe contener entre 5 y 8 letras.")
        else:
            break    

    # solicita y valida El nombre del usuario (debe tener entre 3 y 50 caracteres)
    limpiar_pantalla()
    while True:
        name=input("Ingrese el Nombre y Apellido: ")    
        if len(name) < 3 or len(name) > 50:
            limpiar_pantalla()
            print(f"El Nombre y Apellido deben contener entre 3 y 50 letras.")
        else:
            break 

    # solicita y valida la clave del usuario 
    # (debe tener entre 6 y 10 caracteres y debe contener letras y numeros)
    limpiar_pantalla()
    while True:
        password=input("Ingrese la Clave: ") 
        if len(password) < 6 or len(password) > 10:
            limpiar_pantalla()
            print(f"La Clave debe contener entre 6 y 10 caracteres.")
        elif not validar_letra_y_numero(password):
            limpiar_pantalla()
            print(f"La Clave debe contener al menos una letra y un numero.")    
        else:
            break
    
    # si los datos estan ok se agrega el usuario nuevo a la lista 
    # y se indica el exito de la operacion
    new_user = {
        "user": user,
        "name":name,
        "password":password    
    }

    respuesta=database.add_table_element("users", new_user)

    limpiar_pantalla()
    if respuesta:
        print(f"Se ha registrado el usuario correctamente")
    else:
        print(f"Hubo algun problema al intentar crear el usuario.")
    input("Presione Enter para continuar.")

# Esta funcion solicita el ingreso de los datos del cliente, 
# realiza las validaciones correspondientes y lo da de alta en la base de clientes
def registrar_cliente(database):

    #solicita y valida el dni cliente (debe ser unico contener entre 7 y 8 caracteres numeros)
    limpiar_pantalla()
    while True:
        dni=input("Ingrese el DNI (solo los numeros): ")
        usuario_existente=database.get_table_element("customers",{"dni":dni})
        if usuario_existente is not None:
            limpiar_pantalla()
            print(f"El Cliente: {dni} ya existe, por favor ingrese uno que no exista.")
        elif not (len(dni) >= 7 and len(dni) <= 8 and dni.isdigit()):
            limpiar_pantalla()
            print(f"El DNI debe contener entre 7 y 8 numeros.")
        else:
            break    

    # solicita y valida El nombre del cliente (debe tener entre 3 y 50 caracteres)
    limpiar_pantalla()
    while True:
        name=input("Ingrese el Nombre y Apellido: ")    
        if len(name) < 3 or len(name) > 70:
            limpiar_pantalla()
            print(f"El Nombre y Apellido deben contener entre 3 y 70 letras.")
        else:
            break 

    # solicita y valida la direccion del cliente (debe tener entre 3 y 50 caracteres)
    limpiar_pantalla()
    while True:
        address=input("Ingrese la direccion: ")    
        if len(address) < 3 or len(address) > 50:
            limpiar_pantalla()
            print(f"La direccion debe contener entre 3 y 50 caracteres.")
        else:
            break 
    
    # si los datos estan ok se agrega el usuario nuevo a la lista 
    # y se indica el exito de la operacion
    new_customer = {
        "name":name,
        "dni":dni,
        "address":address,
        "status": "activo"
    }

    respuesta=database.add_table_element("customers", new_customer)

    limpiar_pantalla()
    if respuesta:
        print(f"Se ha registrado el cliente correctamente")
    else:
        print(f"Hubo algun problema al intentar crear el cliente.")
    input("Presione Enter para continuar.")    