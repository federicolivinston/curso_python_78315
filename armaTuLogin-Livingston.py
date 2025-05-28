import os
#################################################
#Objeto Usuario: contiene los datos de un usuario
#################################################
class Usuario:
    def __init__(self, user, name, password):
        self.user=user
        self.name=name
        self.password=password
    
    def __str__(self):
        return f"{self.user:<10}|  {self.name:<70}|  {self.password}"
        
    def get_name(self):
        return self.name

    def verify_password(self, password):
        return self.password==password
################################################################################
# Base usuarios contiene la lista de objetos usuario registrados, 
# se inicializa con un usuario para poder realizar el login inicial al sistema
################################################################################
base_usuarios = {
    "admin": Usuario("admin", "Usuario Admin", "admin1234")
}

# Esta variable se utiliza para controlar si hay un usuario logueado o no 
# y mostrar las opciones del menu
glb_usuario_logueado=False

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
def logOut():
    global glb_usuario_logueado
    opcion=input("Desea salir de la aplicacion? (y/n)")
    if opcion!="y":
        return 
    glb_usuario_logueado=False
       
# Esta funcion solicita usuario y pwd, verifica los datos y loguea al usuario
def logIn(lista_usuarios):
    global glb_usuario_logueado

    limpiar_pantalla()
    user=input("Ingrese su Usuario: ").lower()
    password=input("Ingrese su Clave: ")
    try:
        valor=lista_usuarios[user].verify_password(password)
        if not valor:
            print("Usuario o Clave incorrentos, intentelo nuevamente.")
            input("Presione Enter para continuar.")
            return
    except Exception as e:
        print("Usuario o Clave incorrentos, intentelo nuevamente.")
        input("Presione Enter para continuar.")
        return
    glb_usuario_logueado=True

# Esta funcion solicita el ingreso de los datos del usuario, 
# realiza las validaciones correspondientes y lo da de alta en la base de usuarios
def registrar_usuario(lista_usuarios):

    #solicita y valida el usuario (debe ser unico contener solo letras y entre 5 y 8 caracteres)
    limpiar_pantalla()
    while True:
        user=input("Ingrese el Usuario: ").lower()
        if user in base_usuarios:
            limpiar_pantalla()
            print(f"El Usuario: {user} ya existe, por favor ingrese uno que no exista.")
        elif not (len(user) >= 5 and len(user) <= 8 and user.isalpha()):
            limpiar_pantalla()
            print(f"El Usuario debe contener entre 5 y 8 letras.")
        else:
            break    

    # solicita y valida El nombre del usuario (debe tener entre 3 y 70 caracteres)
    limpiar_pantalla()
    while True:
        name=input("Ingrese el Nombre y Apellido: ")    
        if len(name) < 3 or len(name) > 70:
            limpiar_pantalla()
            print(f"El Nombre y Apellido deben contener entre 3 y 70 letras.")
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
    lista_usuarios[user] = Usuario(user,name,password)
    limpiar_pantalla()
    print(f"Se ha registrado el usuario correctamente")
    print(f"Datos registrados:")
    print()
    print(f"{'Usuario':<10}|  {'Nombre y Apellido':<70}|  {'Clave'}")
    print(f"{lista_usuarios[user]}")
    input("Presione Enter para continuar.")

# Esta funcion recorre la lista de usuarios y 
# muestra la lista de usuarios por pantalla con todos sus datos
def mostrar_usuarios(lista_usuarios):
    limpiar_pantalla()
    print()
    print("Listado de Usuarios activos:")
    print()
    print(f"{'Usuario':<10}|  {'Nombre y Apellido':<70}|  {'Clave'}")
    print("-" * 90)  # Línea divisoria
    for usuario in lista_usuarios.values():
        print(usuario)
    print()
    print()    
    input("Presione Enter para continuar.")


# Esta funcion maneja el menu y la seleccion de opciones del mismo
def elegir_opcion(usuario_logueado):
    limpiar_pantalla()
    print("Menu de opciones:")
    if usuario_logueado:
        print("1. Registrar Usuario.")
        print("2. Mostrar Usuarios.")
        print("3. LogOut.")
        opciones=[1,2,3]
    else:
        print("4. LogIn.")
        print("99. Salir de la aplicacion.")
        opciones=[4,99]
    

    try:
        seleccion = int(input("Ingrese una opcion: "))
        if (seleccion in opciones):
            return seleccion
        else:
            return 0
    except:
        return 0
    
##################################################################################
# Esta es la funcion principal de la aplicacion 
# que maneja el flujo de acciones del usuario en la misma
##################################################################################
def main(lista_usuarios):
    global glb_usuario_logueado

    while True:
        opcion_seleccionada=elegir_opcion(glb_usuario_logueado)

        if opcion_seleccionada==99:
            break
        elif opcion_seleccionada==1:
            registrar_usuario(lista_usuarios)
        elif opcion_seleccionada==2:
            mostrar_usuarios(lista_usuarios)
        elif opcion_seleccionada==3:
            logOut()
        elif opcion_seleccionada==4:
            logIn(lista_usuarios)

###############################################################
# Inicio de la aplicacion
###############################################################
main(base_usuarios)