import Usuarios_ABM  #contiene funciones de Login para usuarios registrados y ADM
import Logueo                 # variacion


def Menu():

    usuarios = Usuarios_ABM.cargar_usuarios()

    print("====================================================================")
    print("                          BIENVENIDOS!")
    print("====================================================================")
    print( )
    print("            Si QUERES ingresar con tu USUARIO  - ingresa 1")
    print("            Si QUERES crear tu USUARIO         - ingresa 2")
    print( )
    print("                   (SALIR del Sistema - ingresa 3)")
    print( )
    print("--------------------------------------------------------------------")
    try:
        eleccion = int(input("Ingresa una opción: "))
    except ValueError:
        print("Opción inválida. Debe ser un número.")
        return Menu()

    print("--------------------------------------------------------------------")
    if eleccion == 1:
        Logueo.procesar_login(usuarios)
        return Menu()
    elif eleccion == 2:
        Usuarios_ABM.agregar_usuario(usuarios)
        return Menu()  # Volver al menú después de crear
    elif eleccion == 3:
        print("Saliendo del sistema...")
        exit()
    else:
        print("Opción inválida.")
        return Menu()
