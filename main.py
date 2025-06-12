from work_package import data_manager
from work_package import action_manager

##################################################################################
# Esta es la funcion principal de la aplicacion 
# que maneja el flujo de acciones del usuario en la misma
##################################################################################
def main():
    database=data_manager.ddbb_handler("./data/")
    usuario_logueado=None

    while True:
        opcion_seleccionada=action_manager.elegir_opcion(usuario_logueado)
        try:
            if opcion_seleccionada==99:
                break
            elif opcion_seleccionada==1:
                action_manager.registrar_usuario(database)
            elif opcion_seleccionada==2:
                action_manager.mostrar_usuarios(database)
            elif opcion_seleccionada==3:
                action_manager.registrar_cliente(database)                
            elif opcion_seleccionada==4:
                action_manager.mostrar_clientes(database)
            elif opcion_seleccionada==5:
                action_manager.mostrar_clientes(database,True)    
            elif opcion_seleccionada==11:
                usuario_logueado=action_manager.log_out(usuario_logueado)
            elif opcion_seleccionada==10:
                usuario_logueado=action_manager.log_in(database)
        except Exception as e:
            print("Ocurrio un error: ", e)
            pase=input("Presione Enter para continuar.")

###############################################################
# Inicio de la aplicacion
###############################################################
main()        