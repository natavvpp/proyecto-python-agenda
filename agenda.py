"""
AGENDA: PROTOTIPO INICIAL

En esta primera fase vamos a implementar una agenda sencilla que nos permita gestionar contactos
utilizando una lista como estructura principal sobre la que elaborar los métodos pertinentes.

Permite:
- Insertar contactos
- Buscar contactos
- Modificar contactos
- Eliminar contactos
- Mostrar todos los contactos

También se incluye validación de datos, manejo de errores y un menú interactivo.
"""

agenda = []


def insertar_elemento(datos):
    """
    Inserta un nuevo contacto en la agenda.

    Solicita al usuario el nombre y el teléfono del contacto.
    Valida que el nombre no esté vacío y que el teléfono sea numérico.

    Parámetros:
    datos (list): Lista que almacena los contactos.

    Retorna:
    None
    """
    print("\n--- Añadir contacto ---")

    nombre = input("Ingrese nombre: ").strip()

    if nombre == "":
        print("El nombre no puede estar vacío.")
        return

    try:
        telefono = int(input("Ingrese teléfono (solo números): "))
    except ValueError:
        print("El teléfono debe ser numérico.")
        return

    contacto = {
        "nombre": nombre,
        "telefono": telefono
    }

    datos.append(contacto)
    print("Contacto agregado correctamente.")


def buscar_elemento(datos):
    """
    Busca un contacto en la agenda por nombre.

    Solicita al usuario el nombre del contacto y lo busca
    dentro de la estructura de datos.

    Parámetros:
    datos (list): Lista que contiene los contactos.

    Retorna:
    None
    """
    print("\n--- Buscar contacto ---")
    nombre = input("Ingrese el nombre a buscar: ").strip()

    for contacto in datos:
        if contacto["nombre"].lower() == nombre.lower():
            print("Contacto encontrado:")
            print(contacto)
            return

    print("Contacto no encontrado.")


def modificar_elemento(datos):
    """
    Modifica un contacto existente en la agenda.

    Solicita el nombre del contacto y permite cambiar su teléfono.
    Incluye manejo de errores para evitar datos inválidos.

    Parámetros:
    datos (list): Lista que contiene los contactos.

    Retorna:
    None
    """
    print("\n--- Modificar contacto ---")
    nombre = input("Ingrese el nombre del contacto a modificar: ").strip()

    for contacto in datos:
        if contacto["nombre"].lower() == nombre.lower():
            try:
                nuevo_telefono = int(input("Ingrese nuevo teléfono: "))
                contacto["telefono"] = nuevo_telefono
                print("Contacto modificado correctamente.")
            except ValueError:
                print("Teléfono inválido.")
            return

    print("Contacto no encontrado.")


def eliminar_elemento(datos):
    """
    Elimina un contacto de la agenda.

    Solicita el nombre del contacto y lo elimina si existe
    en la lista de contactos.

    Parámetros:
    datos (list): Lista que contiene los contactos.

    Retorna:
    None
    """
    print("\n--- Eliminar contacto ---")
    nombre = input("Ingrese el nombre del contacto a eliminar: ").strip()

    for contacto in datos:
        if contacto["nombre"].lower() == nombre.lower():
            datos.remove(contacto)
            print("Contacto eliminado.")
            return

    print("Contacto no encontrado.")


def mostrar_todos(datos):
    """
    Muestra todos los contactos almacenados en la agenda.

    Imprime cada contacto de forma clara y ordenada.

    Parámetros:
    datos (list): Lista que contiene los contactos.

    Retorna:
    None
    """
    print("\n--- Lista de contactos ---")

    if len(datos) == 0:
        print("Agenda vacía.")
        return

    for i, contacto in enumerate(datos, start=1):
        print(f"{i}. Nombre: {contacto['nombre']} | Teléfono: {contacto['telefono']}")


def menu():
    """
    Muestra el menú principal de la agenda.

    Permite al usuario seleccionar opciones para gestionar contactos.
    El menú se repite hasta que el usuario selecciona la opción salir.

    Retorna:
    None
    """
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
            print("Error: recuerde que debe ingresar un número.")
            continue

        if opcion == 1:
            insertar_elemento(agenda)
        elif opcion == 2:
            buscar_elemento(agenda)
        elif opcion == 3:
            modificar_elemento(agenda)
        elif opcion == 4:
            eliminar_elemento(agenda)
        elif opcion == 5:
            mostrar_todos(agenda)
        elif opcion == 6:
            print("Saliendo del programa...")
            break
        else:
            print("Opción inválida.")


menu()