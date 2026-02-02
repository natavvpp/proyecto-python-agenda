import json
import os
import logging
import sys

## EJERCICIOS RESUELTOS EN EL EXAMEN: EJ.1(LÍNEA 31) Y EJ.3(LÍNEA 261)

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
        email_mostrar = self.email if self.email else "No definido"  # Campo opcional
        return f"Nombre: {self.nombre} | Teléfono: {self.telefono} | Email: {email_mostrar}"


# EXAMEN - Ejercicio 1 - Subclase ContactoProfesion -> Hereda de la clase Contacto
class ContactoConProfesion(Contacto):
    def __init__(self, nombre, telefono, email="", direccion="", profesion=""):
        super().__init__(nombre, telefono, email)
        self.profesion = profesion

    def __str__(self):
        email_mostrar = self.email if self.email else "No definido"
        profesion_mostrar = self.profesion if self.profesion else "No definida"
        return f"{self.nombre} | {self.telefono} | {email_mostrar} | Profesion: {profesion_mostrar}"




# =========================
# Clase Agenda
# =========================
class Agenda:
    FICHERO_JSON = os.path.join(os.path.dirname(__file__), "agenda_poo.json")

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
                    profesion = c.get("profesion", "")
                    contactos.append(ContactoConProfesion(nombre, telefono, email, profesion))
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
                    [{"nombre": c.nombre, "telefono": c.telefono, "email": c.email,
                      "profesion": getattr(c, "profesion", "")}
                     for c in self.contactos],
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

        profesion = input("Ingrese profesión del contacto a agendar: ").strip()
        if not profesion:
            profesion = ""

        self.contactos.append(ContactoConProfesion(nombre, telefono, email, profesion))
        self.guardar_datos()
        logging.info(f"Contacto añadido: {nombre}")
        print("Contacto agregado correctamente.")

        """
            Sin herencia: 

            self.contactos.append(Contacto(nombre, telefono, email))
            self.guardar_datos()
            logging.info(f"Contacto añadido: {nombre}")
            print("Contacto agregado correctamente.") 
        """

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

    # Modificar contacto (teléfono, email y profesion
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
                nueva_profesion = input("Ingrese nueva profesion: ").strip()
                if nueva_profesion:
                    c.profesion = nueva_profesion
                self.guardar_datos()
                logging.info(f"Contacto modificado: {nombre}")
                print("Contacto modificado correctamente.")
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
                self.guardar_datos()
                logging.info(f"Contacto eliminado: {nombre}")
                print("Contacto eliminado correctamente.")
                return
        logging.warning(f"Intento de eliminar contacto inexistente: {nombre}")
        print("Contacto no encontrado.")

    # Contar contactos
    def contar(self):
        total = len(self.contactos)
        print(f"Existen {total} contactos en la agenda.")

    # Eliminar agenda
    def eliminar_agenda(self):
        confirmacion = input("¿Seguro que quieres eliminar toda la agenda? (s/n): ").lower()

        if confirmacion != "s":
            print("Operación cancelada.")
            return

        self.contactos.clear()
        self.guardar_datos()
        logging.info("Agenda eliminada completamente.")
        print("Agenda eliminada correctamente.")

    # EXAMEN - Ejercicio 3 - Metodo ordenacion y resumen
    def ordenacion_resumen(self):
        # Ordenamos contactos por nombre
        self.contactos.sort(key=lambda c: c.nombre.lower())
        self.guardar_datos()
        logging.info("Contactos ordenados por nombre A-Z.")
        print("Contactos ordenados por nombre (A–Z).")

        # Mostramos los elementos (contactos) ordenados alfabéticamente(A-Z)
        self.mostrar_todos()

        # Mostramos el total de elementos contenidos por el objeto de tipo Agenda
        print("")
        total = len(self.contactos)
        print(f"Existen {total} contactos en la agenda.")

        # Creamos y mostramos un elemento calculado (¿Cuántos contactos no tienen email agregado?)
        print("")
        contactosSinEmail = 0;
        for c in self.contactos:
            if c.email.lower() == "":
                contactosSinEmail += 1

        print(f"Existen {contactosSinEmail} contactos sin email agregado en la agenda")




# =========================
# Menú principal
# =========================
def menuExamen():
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
        print("8. Mostrar reporte (método EXAMEN)")
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
            agenda.ordenacion_resumen()
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
    menuExamen()
