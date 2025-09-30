import Usuarios_ABM
import Menu_Principal

def mostrar_menu_Administrador(usuarios):
    while True:

        print("\nQue necesitas hacer?")
        print( )
        print("            Si QUERES modificar un ROL     - ingresa 1")
        print("            Si QUERES ver USUARIO creados  - ingresa 2")
        print("            Si QUERES eliminar un USUARIO  - ingresa 3")
        print("            Volver al Menú Principal       - ingresa 4")
        print("            Salir del Sistema              - ingresa 5")
        print( )
        print("--------------------------------------------------------------------")

        try:
            eleccion_Admin = int(input("Ingrese una opción: "))
        except ValueError:
            print("Opción inválida. Debe ingresar un número.")
            continue

        if eleccion_Admin == 1:
            Usuarios_ABM.modificar_rol_usuario(usuarios)

        elif eleccion_Admin == 2:
            Usuarios_ABM.mostrar_usuarios(usuarios)

        elif eleccion_Admin == 3:
            Usuarios_ABM.eliminar_usuario(usuarios)

        elif eleccion_Admin == 4:
            print("Volviendo al menú principal...")
            Menu_Principal.Menu()
            return  # vuelve al menú principal

        elif eleccion_Admin == 5:
            print("Saliendo del sistema...")
            exit()

        else:
            print("Opción inválida. Intente nuevamente.")
