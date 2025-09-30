import pickle
import re
from datetime import datetime
from usuario import Usuario
import os

RUTA_USUARIOS = os.path.join(os.path.dirname(__file__), 'usuarios.ispc')

#define las clases

class Acceso:
    def __init__(self, id, fechaIngreso, fechaSalida, usuarioLogueado):
        self.id = id
        self.fechaIngreso = fechaIngreso
        self.fechaSalida = fechaSalida
        self.usuarioLogueado = usuarioLogueado
        
# funciones para ABM
# ------------- Gestion de Usuarios ---------------------
def cargar_usuarios():
    try:
        with open(RUTA_USUARIOS, 'rb') as file:
            return pickle.load(file)
    except FileNotFoundError:
        return []

def guardar_usuarios(usuarios):
    with open(RUTA_USUARIOS, 'wb') as file:
        pickle.dump(usuarios, file)


def modificar_rol_usuario(usuarios):
    nombre_usuario = input("Ingrese el nombre de usuario del usuario a modificar: ")
    for usuario in usuarios:
        if usuario.nombre_usuario == nombre_usuario:
            #usuario.password = input("Ingrese nuevo password: ")
            #usuario.email = input("Ingrese nuevo email: ")
            usuario.rol = input("Ingrese nuevo rol Docente/Admin: ")
            guardar_usuarios(usuarios)
            print("Usuario modificado exitosamente.")
            return
    print("Usuario no encontrado.")

def eliminar_usuario(usuarios):
    nombre_usuario = input("Ingrese el nombre de usuario o email del usuario a eliminar: ")
    for usuario in usuarios:
        if usuario.nombre_usuario == nombre_usuario or usuario.email == nombre_usuario:
            if usuario.rol.lower() == "superadmin":
               print("No se puede eliminar ese usuario")
               return
            usuarios.remove(usuario)
            guardar_usuarios(usuarios)
            print("Usuario eliminado exitosamente.")
            return
    print("Usuario no encontrado.")

def buscar_usuario(usuarios):
    nombre_usuario = input("Ingrese el nombre de usuario o email del usuario a buscar: ")
    for usuario in usuarios:
        if usuario.nombre_usuario == nombre_usuario or usuario.email == nombre_usuario:
            print(f"ID: {usuario.id}, nombre de usuario: {usuario.nombre_usuario}, Email: {usuario.email}, Rol: {usuario.rol}")
            return
    print("Usuario no encontrado.")

def mostrar_usuarios(usuarios):
    for usuario in usuarios:
        print(f"ID: {usuario.id}, nombre de usuario: {usuario.nombre_usuario}, Email: {usuario.email}, Pass: {usuario.password}, Rol: {usuario.rol}")  
  
#fincion para evaluar si respeta formato de email
def es_email_valido(email):
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)
#evalua si cumple las condiciones requeridas para la pass
def es_password_valida(password):
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"\d", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

# Función principal para agregar un nuevo usuario
def agregar_usuario(usuarios):
    #usuarios = cargar_usuarios()
    id = len(usuarios) + 1

    # Validar email primero
    while True:
        email = input("Ingrese email: ").strip()
        if not es_email_valido(email):
            print("Formato de email inválido. Intente nuevamente.")
            continue
        if any(u.email == email for u in usuarios):
            print("Ese email ya está registrado. Intente con otro.")
            continue
        break

    # Luego validar nombre de usuario
    while True:
        nombre_usuario = input("Ingrese nombre de usuario: ").strip()
        if not nombre_usuario:
            print("El nombre de usuario no puede estar vacío.")
            continue
        if any(u.nombre_usuario == nombre_usuario for u in usuarios):
            print("Ese nombre de usuario ya está en uso. Intente con otro.")
            continue
        break

    # Por último validar la contraseña
    while True:
        password = input("Ingrese password: ")
        if not es_password_valida(password):
            print("La contraseña debe tener al menos 8 caracteres, incluir una mayúscula, una minúscula, un número y un carácter especial.")
            continue
        break

    nuevo_usuario = Usuario(id, nombre_usuario, password, email,"Alumno")
    usuarios.append(nuevo_usuario)
    guardar_usuarios(usuarios)
    print("Usuario agregado exitosamente.")

