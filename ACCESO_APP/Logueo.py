
import pickle
from datetime import datetime
from usuario import Usuario
import os
import Menu_Administrador


RUTA_USUARIOS = os.path.join(os.path.dirname(__file__), 'usuarios.ispc')
RUTA_ACCESOS = os.path.join(os.path.dirname(__file__), 'accesos.ispc')
RUTA_LOGS = os.path.join(os.path.dirname(__file__), 'logs.txt')

class Acceso:
    def __init__(self, id, fechaIngreso, fechaSalida, usuarioLogueado):
        self.id = id
        self.fechaIngreso = fechaIngreso
        self.fechaSalida = fechaSalida
        self.usuarioLogueado = usuarioLogueado

# ------------- Gestion de Accesos ------------------------------

def registrar_acceso(usuario):
    accesos = cargar_accesos()
    id = len(accesos) + 1
    fechaIngreso = datetime.now()
    fechaSalida = None
    accesos.append(Acceso(id, fechaIngreso, fechaSalida, usuario.nombre_usuario))
    guardar_accesos(accesos)

def cargar_accesos():
    try:
        with open(RUTA_ACCESOS, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

def guardar_accesos(accesos):
    with open(RUTA_ACCESOS, 'wb') as file:
        pickle.dump(accesos, file)

def registrar_logueo_fallido(nombre_usuario, password):
    with open(RUTA_LOGS, 'a') as file:
        file.write(f"{datetime.now()} - nombre de usuario: {nombre_usuario}, Password: {password}\n")

"""def mostrar_accesos():
    accesos = cargar_accesos()
    if not accesos:
        print("No hay accesos registrados.")
        return
    print("\nLista de Accesos Registrados:")
    print("-------------------------------------------------------")
    for acceso in accesos:
        print(f"ID: {acceso.id} ")
        print(f"Usuario: {acceso.usuarioLogueado}")
        print(f"Fecha de Ingreso: {acceso.fechaIngreso}")
        print(f"Fecha de Salida: {acceso.fechaSalida if acceso.fechaSalida else '---'}")
        print("-------------------------------------------------------")"""


# ----------------------- Gestion de Usuarios -------------------
def cargar_usuarios():
    try:
        with open(RUTA_USUARIOS, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []


def guardar_usuarios(usuarios):
    with open(RUTA_USUARIOS, 'wb') as file:
        pickle.dump(usuarios, file)


def resetear_contrasena(nombre_usuario):
    usuarios = cargar_usuarios()
    usuario = next((u for u in usuarios if u.nombre_usuario == nombre_usuario), None)

    if not usuario:
        print("Usuario no encontrado.")
        return

    email_ingresado = input("Ingrese el email asociado a su cuenta: ").strip().lower()

    if not hasattr(usuario, 'email'):
        print("Este usuario no tiene un email registrado. No se puede validar la identidad.")
        return

    if usuario.email.lower() != email_ingresado:
        print("El email no coincide con el registrado. No se puede cambiar la contraseña.")
        return

    nueva_password = input("Ingrese la nueva contraseña: ")
    confirmar_password = input("Confirme la nueva contraseña: ")

    if nueva_password != confirmar_password:
        print("Las contraseñas no coinciden. No se realizó ningún cambio.")
        return

    usuario.password = nueva_password
    guardar_usuarios(usuarios)
    print("La contraseña ha sido actualizada exitosamente.")


def recuperar_usuario(usuarios):
    email = input("Ingrese su email registrado: ").strip().lower()
    #usuarios = cargar_usuarios()

    usuario = next((u for u in usuarios if hasattr(u, 'email') and u.email.lower() == email), None)

    if usuario:
        print(f"Su nombre de usuario es: {usuario.nombre_usuario}")
    else:
        print("No se encontró un usuario con ese email.")



def procesar_login(usuarios):
    #usuarios = cargar_usuarios()
    print(f"Usuarios cargados: {[u.nombre_usuario for u in usuarios]}")
    max_intentos = 4
    usuario = None

    # Validar nombre de usuario (hasta 4 intentos)
    for intento in range(max_intentos):
        nombre_usuario = input("Ingrese nombre de usuario: ")

        usuario = next((u for u in usuarios if u.nombre_usuario == nombre_usuario), None)

        if usuario:
            break  # Usuario encontrado, continuar con el login
        else:
            print("El nombre de usuario no existe.")
            if intento < max_intentos - 1:
                print(f"Intentos restantes: {max_intentos - intento - 1}")
            else:
                print("Se han superado los intentos para ingresar un nombre de usuario.")
                recuperar = input("¿Desea recuperar su nombre de usuario? (s/n): ").strip().lower()
                if recuperar == 's':
                    recuperar_usuario(usuarios) 
                else:
                    print("Operación cancelada.")
                return  # Salimos del login

    # Validar password (hasta 4 intentos)
    intentos_pass = 0
    autenticado = False

    while intentos_pass < max_intentos:
        password = input("Ingrese password: ")

        if usuario.password == password:
            print("Ingreso exitoso.")
            registrar_acceso(usuario)
            autenticado = True
            break
        else:
            print("Password incorrecta.")
            registrar_logueo_fallido(usuario.nombre_usuario, password)
            intentos_pass += 1

    if autenticado:
        # Evaluamos el rol del usuario
        if usuario.rol.lower() == "alumno":
            print("\nBienvenido al módulo Alumno.")
        elif usuario.rol.lower() == "docente":
            print("\nBienvenido al módulo Docente.")
        elif usuario.rol.lower() == "administrador" or usuario.rol.lower() == "superadmin":
            print("\nBienvenido al módulo Administrador.")
            print( )
            Menu_Administrador.mostrar_menu_Administrador(usuarios)
            return
        else:
            print(f"\nRol desconocido: {usuario.rol}")

        # Menú posterior
        while True:
            print("\n1. Volver al Menú Principal")
            print("2. Salir")
            sub_opcion = input("Seleccione una opción: ")
            if sub_opcion == '1':
                return
            elif sub_opcion == '2':
                exit()
    else:
        print("Se han superado los intentos para ingresar la contraseña.")
        opcion_reset = input("¿Desea resetear su contraseña? (s/n): ").strip().lower()
        if opcion_reset == 's':
            resetear_contrasena(usuario.nombre_usuario)
        else:
            print("Operación cancelada.")





