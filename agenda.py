import json
import os
import logging
import sys

# =========================
# CONFIGURACIÓN DE LOGGING
# =========================
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H:%M:%S",
    filename="agenda.log",
    filemode="a"
)

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.WARNING)
console_handler.setFormatter(logging.Formatter("%(levelname)s: %(message)s"))
logging.getLogger().addHandler(console_handler)

# =========================
# Clase Contacto
# =========================
class Contacto:
    def __init__(self, nombre, telefono, email=""):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

    def __str__(self):
        email_mostrar = self.email if self.email else "No definido" # Trabajamos con un campo opcional
        return f"Nombre: {self.nombre} | Teléfono: {self.telefono} | Email: {email_mostrar}"

# =========================
# Clase Agenda
# =========================
class Agenda:
    FICHERO_JSON = os.path.join(os.path.dirname(__file__), "agenda_poo.json")

    #No se pasan los contactos al constructor porque la clase Agenda se encarga de cargarlos desde el fichero JSON.
    # Así se mantiene la encapsulación y la agenda se inicializa automáticamente con sus datos.
    def __init__(self):
        self.contactos = self.cargar_datos()

    # Cargar datos del JSON
    def cargar_datos(self):
        if not os.path.exists(self.FICHERO_JSON):
            logging.warning("El fichero agenda.json no existe. Se creará uno nuevo.")
            return []

        try:
            with open(self.FICHERO_JSON, "r", encoding="utf-8") as f:
                datos = json.load(f)
                contactos = []
                for c in datos:
                    nombre = c.get("nombre", "")
                    telefono = c.get("telefono", 0)
                    email = c.get("email", "")
                    contactos.append(Contacto(nombre, telefono, email))
                logging.info("Datos cargados correctamente desde JSON.")
                return contactos
        except Exception as e:
            logging.error("Error cargando JSON.", exc_info=True)
            return []

    # Guardar datos al JSON
    def guardar_datos(self):
        try:
            with open(self.FICHERO_JSON, "w", encoding="utf-8") as f:
                json.dump(
                    [{"nombre": c.nombre, "telefono": c.telefono, "email": c.email} for c in self.contactos],
                    f,
                    indent=4,
                    ensure_ascii=False
                )
            logging.info("Datos guardados correctamente en JSON.")
        except Exception as e:
            logging.critical("Error crítico al guardar datos en JSON.", exc_info=True)

    # Insertar nuevo contacto
    def insertar(self):
        print("\n--- Añadir contacto ---")
        nombre = input("Ingrese nombre: ").strip()
        if not nombre:
            logging.warning("Intento de insertar contacto con nombre vacío.")
            print("El nombre no puede estar vacío.")
            return

        # Evitamos duplicados en el nombre
        for c in self.contactos:
            if c.nombre.lower() == nombre.lower():
                logging.warning(f"Intento de insertar contacto duplicado: {nombre}")
                print("Este contacto ya existe.")
                return

        try:
            telefono = int(input("Ingrese teléfono: "))

        except ValueError:
            logging.error("Teléfono inválido al insertar contacto.")
            print("Teléfono inválido.")
            return

        # Evitamos duplicados en el nº de tlf
        for c in self.contactos:
            if c.telefono == telefono:
                logging.warning(f"Intento de insertar teléfono duplicado: {telefono}")
                print("Este teléfono ya existe.")
                return

        email = input("Ingrese email: ").strip()
        if not email:
            logging.warning("Email vacío al insertar contacto.")
            print("Se recomienda añadir un email.")
            email = ""

        self.contactos.append(Contacto(nombre, telefono, email))
        self.guardar_datos()
        logging.info(f"Contacto añadido: {nombre}")
        print("Contacto agregado correctamente.")

    # Mostrar todos los contactos
    def mostrar_todos(self):
        print("\n--- Lista de contactos ---")
        if not self.contactos:
            print("Agenda vacía.")
            return
        for i, c in enumerate(self.contactos, start=1):
            print(f"{i}. {c}")

    # Buscar contacto por nombre
    def buscar_nombre(self):
        print("\n--- Buscar contacto por nombre ---")
        nombre = input("Ingrese nombre a buscar: ").strip()
        for c in self.contactos:
            if c.nombre.lower() == nombre.lower():
                logging.info(f"Contacto encontrado: {nombre}")
                print(c)
                return
        logging.warning(f"Contacto no encontrado: {nombre}")
        print("Contacto no encontrado.")

    # Buscar contacto por teléfono
    def buscar_telefono(self):
        print("\n--- Buscar contacto por teléfono ---")
        try:
            tlf = int(input("Ingrese teléfono a buscar: ").strip())
        except ValueError:
            logging.error("Teléfono inválido al buscar.")
            print("Teléfono inválido.")
            return
        for c in self.contactos:
            if c.telefono == tlf:
                logging.info(f"Teléfono localizado: {tlf}")
                print(c)
                return
        logging.warning(f"Teléfono no encontrado: {tlf}")
        print("Número no encontrado.")

    # Buscar contacto por email
    def buscar_email(self):
        print("\n--- Buscar contacto por email ---")
        email = input("Ingrese email a buscar: ").strip().lower()
        for c in self.contactos:
            if c.email.lower() == email:
                logging.info(f"Email localizado: {email}")
                print(c)
                return
        logging.warning(f"Email no encontrado: {email}")
        print("Email no encontrado.")

    # Modificar contacto (teléfono y email)
    def modificar(self):
        print("\n--- Modificar contacto ---")
        nombre = input("Ingrese nombre del contacto a modificar: ").strip()
        for c in self.contactos:
            if c.nombre.lower() == nombre.lower():
                try:
                    c.telefono = int(input("Ingrese nuevo teléfono: "))
                except ValueError:
                    logging.error("Teléfono inválido al modificar.")
                    print("Teléfono inválido.")
                    return
                nuevo_email = input("Ingrese nuevo email: ").strip()
                if nuevo_email:
                    c.email = nuevo_email
                try:
                    self.guardar_datos()
                    logging.info(f"Contacto modificado: {nombre}")
                    print("Contacto modificado correctamente.")
                except Exception as e:
                    logging.error("Error guardando contacto modificado.", exc_info=True)
                    print("Error guardando contacto.")
                return
        logging.warning(f"Intento de modificar contacto inexistente: {nombre}")
        print("Contacto no encontrado.")

    # Eliminar contacto
    def eliminar(self):
        print("\n--- Eliminar contacto ---")
        nombre = input("Ingrese nombre del contacto a eliminar: ").strip()
        for c in self.contactos:
            if c.nombre.lower() == nombre.lower():
                self.contactos.remove(c)
                try:
                    self.guardar_datos()
                    logging.info(f"Contacto eliminado: {nombre}")
                    print("Contacto eliminado correctamente.")
                except Exception as e:
                    logging.error("Error eliminando contacto.", exc_info=True)
                    print("Error eliminando contacto.")
                return
        logging.warning(f"Intento de eliminar contacto inexistente: {nombre}")
        print("Contacto no encontrado.")

    # Contar contactos
    def contar(self):
        total = len(self.contactos)
        print(f"Existen {total} contactos en la agenda.")

# =========================
# Menú principal
# =========================
def menu():
    agenda = Agenda()

    while True:
        print("\n===== AGENDA =====")
        print("1. Añadir contacto")
        print("2. Buscar por nombre")
        print("3. Buscar por teléfono")
        print("4. Buscar por email")
        print("5. Modificar contacto")
        print("6. Eliminar contacto")
        print("7. Mostrar todos")
        print("8. Contar contactos")
        print("9. Salir")

        try:
            opcion = int(input("Seleccione una opción: "))
        except ValueError:
            logging.error("Opción de menú no numérica.")
            print("Debe ingresar un número.")
            continue

        if opcion == 1:
            agenda.insertar()
        elif opcion == 2:
            agenda.buscar_nombre()
        elif opcion == 3:
            agenda.buscar_telefono()
        elif opcion == 4:
            agenda.buscar_email()
        elif opcion == 5:
            agenda.modificar()
        elif opcion == 6:
            agenda.eliminar()
        elif opcion == 7:
            agenda.mostrar_todos()
        elif opcion == 8:
            agenda.contar()
        elif opcion == 9:
            logging.info("Aplicación cerrada por el usuario.")
            print("Saliendo del programa...")
            break
        else:
            logging.warning("Opción de menú fuera de rango.")
            print("Opción inválida.")

# =========================
# Ejecución
# =========================
if __name__ == "__main__":
    menu()
