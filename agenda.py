import json
import logging
import os
import sys

# ==============================
# CONFIGURACIÓN DE LOGGING
# ==============================

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - Módulo: %(module)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="agenda.log",
    filemode="a"
)

# Handler adicional para mostrar WARNING+ en consola
console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logging.getLogger().addHandler(console_handler)

# ==============================
# CONSTANTES
# ==============================
FICHERO_JSON = os.path.join(os.path.dirname(__file__), "agenda.json")


# ==============================
# FUNCIONES DE FICHEROS JSON
# ==============================

def cargar_datos():
    """
    Carga los contactos desde un fichero JSON.
    Si el fichero no existe, devuelve una lista vacía.
    """
    if not os.path.exists(FICHERO_JSON):
        logging.warning("El fichero agenda.json no existe. Se creará uno nuevo.")
        return []

    try:
        with open(FICHERO_JSON, "r", encoding="utf-8") as fichero:
            datos = json.load(fichero)
            logging.info("Datos cargados correctamente desde JSON.")
            return datos
    except Exception as e:
        logging.error("Error al cargar el fichero JSON.", exc_info=True)
        return []


def guardar_datos(datos):
    """
    Guarda la lista de contactos en un fichero JSON.
    """
    try:
        with open(FICHERO_JSON, "w", encoding="utf-8") as fichero:
            json.dump(datos, fichero, indent=4, ensure_ascii=False)
            logging.info("Datos guardados correctamente en JSON.")
    except Exception as e:
        logging.critical("Error crítico al guardar datos en JSON.", exc_info=True)

# ==============================
# FUNCIONES PRINCIPALES
# ==============================

def insertar_elemento(datos):
    """
    Inserta un nuevo contacto en la agenda.
    """
    print("\n--- Añadir contacto ---")
    nombre = input("Ingrese nombre: ").strip()

    if nombre == "":
        logging.warning("Intento de insertar contacto con nombre vacío.")
        print("El nombre no puede estar vacío.")
        return

    try:
        telefono = int(input("Ingrese teléfono (solo números): "))
    except ValueError:
        logging.error("Teléfono inválido al insertar contacto.")
        print("El teléfono debe ser numérico.")
        return

    contacto = {"nombre": nombre, "telefono": telefono}
    datos.append(contacto)
    guardar_datos(datos)

    logging.info(f"Contacto añadido: {nombre}")
    print("Contacto agregado correctamente.")


def buscar_elemento(datos):
    """
    Busca un contacto por nombre.
    """
    print("\n--- Buscar contacto ---")
    nombre = input("Ingrese el nombre a buscar: ").strip()

    for contacto in datos:
        if contacto["nombre"].lower() == nombre.lower():
            logging.info(f"Contacto encontrado: {nombre}")
            print(contacto)
            return

    logging.warning(f"Contacto no encontrado: {nombre}")
    print("Contacto no encontrado.")


def modificar_elemento(datos):
    """
    Modifica el teléfono de un contacto existente.
    """
    print("\n--- Modificar contacto ---")
    nombre = input("Ingrese el nombre del contacto a modificar: ").strip()

    for contacto in datos:
        if contacto["nombre"].lower() == nombre.lower():
            try:
                nuevo_telefono = int(input("Ingrese nuevo teléfono: "))
                contacto["telefono"] = nuevo_telefono
                guardar_datos(datos)
                logging.info(f"Contacto modificado: {nombre}")
                print("Contacto modificado correctamente.")
            except ValueError:
                logging.error("Error al modificar teléfono.", exc_info=True)
                print("Teléfono inválido.")
            return

    logging.warning(f"Intento de modificar contacto inexistente: {nombre}")
    print("Contacto no encontrado.")


def eliminar_elemento(datos):
    """
    Elimina un contacto de la agenda.
    """
    print("\n--- Eliminar contacto ---")
    nombre = input("Ingrese el nombre del contacto a eliminar: ").strip()

    for contacto in datos:
        if contacto["nombre"].lower() == nombre.lower():
            datos.remove(contacto)
            guardar_datos(datos)
            logging.info(f"Contacto eliminado: {nombre}")
            print("Contacto eliminado.")
            return

    logging.warning(f"Intento de eliminar contacto inexistente: {nombre}")
    print("Contacto no encontrado.")


def mostrar_todos(datos):
    """
    Muestra todos los contactos de la agenda.
    """
    print("\n--- Lista de contactos ---")

    if not datos:
        print("Agenda vacía.")
        return

    for i, contacto in enumerate(datos, start=1):
        print(f"{i}. Nombre: {contacto['nombre']} | Teléfono: {contacto['telefono']}")

# ==============================
# MENÚ PRINCIPAL
# ==============================

def menu():
    """
    Menú interactivo de la agenda.
    """
    datos = cargar_datos()

    while True:
        print("\n===== AGENDA =====")
        print("1. Añadir contacto")
        print("2. Buscar contacto")
        print("3. Modificar contacto")
        print("4. Eliminar contacto")
        print("5. Mostrar todos")
        print("6. Salir")

        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            logging.error("Opción de menú no numérica.")
            print("Debe ingresar un número.")
            continue

        if opcion == 1:
            insertar_elemento(datos)
        elif opcion == 2:
            buscar_elemento(datos)
        elif opcion == 3:
            modificar_elemento(datos)
        elif opcion == 4:
            eliminar_elemento(datos)
        elif opcion == 5:
            mostrar_todos(datos)
        elif opcion == 6:
            logging.info("Aplicación cerrada por el usuario.")
            print("Saliendo del programa...")
            break
        else:
            logging.warning("Opción de menú fuera de rango.")
            print("Opción inválida.")

# ==============================
# EJECUCIÓN
# ==============================

menu()
