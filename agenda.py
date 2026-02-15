import json
import os
import logging
import sys

# =====================================================
# CONFIGURACIÓN DE LOGGING
# =====================================================

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


# =====================================================
# CLASE BASE: Contacto
# =====================================================
# Representa un contacto normal. Es la clase principal del sistema.

class Contacto:

    def __init__(self, nombre, telefono, email=""):
        self.nombre = nombre
        self.telefono = telefono
        self.email = email

    # Convierte el objeto en diccionario para poder guardarlo en JSON
    def to_dict(self):
        return {
            "tipo": "normal",
            "nombre": self.nombre,
            "telefono": self.telefono,
            "email": self.email
        }

    def __str__(self):
        email_mostrar = self.email if self.email else "No definido"
        return f"Nombre: {self.nombre} | Teléfono: {self.telefono} | Email: {email_mostrar}"


# =====================================================
# SUBCLASE: ContactoConDireccion
# =====================================================
# Subclase que hereda de Contacto y añade un atributo extra: dirección.
# Esto cumple el requisito de usar herencia del enunciado.

class ContactoConDireccion(Contacto):

    def __init__(self, nombre, telefono, email="", direccion=""):
        super().__init__(nombre, telefono, email)
        self.direccion = direccion

    def to_dict(self):
        data = super().to_dict()
        data["tipo"] = "direccion"
        data["direccion"] = self.direccion
        return data

    def __str__(self):
        email_mostrar = self.email if self.email else "No definido"
        direccion_mostrar = self.direccion if self.direccion else "No definida"
        return f"{self.nombre} | {self.telefono} | {email_mostrar} | Dirección: {direccion_mostrar}"


# =====================================================
# CLASE PRINCIPAL: Agenda
# =====================================================
# Gestiona la lista de contactos y todas las operaciones (CRUD)

class Agenda:

    FICHERO_JSON = os.path.join(os.path.dirname(__file__), "agenda_poo.json")

    def __init__(self):
        self.contactos = self.cargar_datos()

    # -------------------------------------------------
    # CARGAR DATOS DESDE JSON
    # -------------------------------------------------
    # Aquí también se aplica la herencia: dependiendo del tipo
    # guardado en el JSON se crea un objeto Contacto o ContactoConDireccion.

    def cargar_datos(self):

        if not os.path.exists(self.FICHERO_JSON):
            logging.warning("El fichero JSON no existe. Se creará uno nuevo.")
            return []

        try:
            with open(self.FICHERO_JSON, "r", encoding="utf-8") as f:

                datos = json.load(f)
                contactos = []

                for c in datos:

                    tipo = c.get("tipo", "normal")

                    # Reconstrucción de objetos según su tipo
                    if tipo == "direccion":
                        contactos.append(
                            ContactoConDireccion(
                                c.get("nombre", ""),
                                c.get("telefono", 0),
                                c.get("email", ""),
                                c.get("direccion", "")
                            )
                        )
                    else:
                        contactos.append(
                            Contacto(
                                c.get("nombre", ""),
                                c.get("telefono", 0),
                                c.get("email", "")
                            )
                        )

                logging.info("Datos cargados correctamente.")
                return contactos

        except Exception:
            logging.error("Error cargando JSON.", exc_info=True)
            return []

    # -------------------------------------------------
    # GUARDAR DATOS
    # -------------------------------------------------

    def guardar_datos(self):

        try:
            with open(self.FICHERO_JSON, "w", encoding="utf-8") as f:

                json.dump(
                    [c.to_dict() for c in self.contactos],
                    f,
                    indent=4,
                    ensure_ascii=False
                )

            logging.info("Datos guardados correctamente.")

        except Exception:
            logging.critical("Error crítico al guardar datos.", exc_info=True)

    # -------------------------------------------------
    # INSERTAR CONTACTO
    # -------------------------------------------------
    # >>> AQUÍ ES DONDE SE HA ADAPTADO EL MENÚ SEGÚN EL ENUNCIADO <<<
    #
    # El ejercicio pedía:
    # - Preguntar si el elemento es normal o especial
    # - Instanciar la clase correcta
    #
    # Esto se hace preguntando (n/d) y creando Contacto o ContactoConDireccion.

    def insertar(self):

        print("\n--- Añadir contacto ---")

        nombre = input("Ingrese nombre: ").strip()

        if not nombre:
            logging.warning("Intento de insertar contacto con nombre vacío.")
            print("El nombre no puede estar vacío.")
            return

        for c in self.contactos:
            if c.nombre.lower() == nombre.lower():
                logging.warning(f"Intento de insertar contacto duplicado: {nombre}")
                print("Este contacto ya existe.")
                return

        try:
            telefono = int(input("Ingrese teléfono: "))
        except ValueError:
            logging.error("Teléfono inválido.")
            print("Teléfono inválido.")
            return

        for c in self.contactos:
            if c.telefono == telefono:
                logging.warning(f"Intento de insertar teléfono duplicado: {telefono}")
                print("Este teléfono ya existe.")
                return

        email = input("Ingrese email: ").strip()

        # >>> ADAPTACIÓN DEL MENÚ PEDIDA EN EL ENUNCIADO <<<
        # Se pregunta al usuario qué tipo de contacto quiere crear
        tipo = input("¿Contacto normal o con dirección? (n/d): ").lower()

        # Dependiendo de la respuesta se instancia la clase correspondiente
        if tipo == "d":
            direccion = input("Ingrese dirección: ").strip()
            nuevo = ContactoConDireccion(nombre, telefono, email, direccion)
        else:
            nuevo = Contacto(nombre, telefono, email)

        self.contactos.append(nuevo)
        self.guardar_datos()

        logging.info(f"Contacto añadido: {nombre}")
        print("Contacto agregado correctamente.")

    # -------------------------------------------------
    # RESTO DE MÉTODOS 
    # -------------------------------------------------

    def mostrar_todos(self):

        print("\n--- Lista de contactos ---")

        if not self.contactos:
            print("Agenda vacía.")
            return

        for i, c in enumerate(self.contactos, start=1):
            print(f"{i}. {c}")

    def buscar_nombre(self):

        nombre = input("Ingrese nombre a buscar: ").strip()

        for c in self.contactos:
            if c.nombre.lower() == nombre.lower():
                print(c)
                logging.info(f"Contacto encontrado: {nombre}")
                return

        logging.warning(f"Contacto no encontrado: {nombre}")
        print("Contacto no encontrado.")

    def buscar_telefono(self):

        try:
            tlf = int(input("Ingrese teléfono a buscar: "))
        except ValueError:
            logging.error("Teléfono inválido.")
            print("Teléfono inválido.")
            return

        for c in self.contactos:
            if c.telefono == tlf:
                print(c)
                logging.info(f"Teléfono localizado: {tlf}")
                return

        logging.warning(f"Teléfono no encontrado: {tlf}")
        print("Número no encontrado.")

    def buscar_email(self):

        email = input("Ingrese email a buscar: ").strip().lower()

        for c in self.contactos:
            if c.email.lower() == email:
                print(c)
                logging.info(f"Email localizado: {email}")
                return

        logging.warning(f"Email no encontrado: {email}")
        print("Email no encontrado.")

    def modificar(self):

        nombre = input("Ingrese nombre del contacto a modificar: ").strip()

        for c in self.contactos:

            if c.nombre.lower() == nombre.lower():

                try:
                    c.telefono = int(input("Nuevo teléfono: "))
                except ValueError:
                    print("Teléfono inválido.")
                    return

                nuevo_email = input("Nuevo email: ").strip()
                if nuevo_email:
                    c.email = nuevo_email

                if isinstance(c, ContactoConDireccion):
                    nueva_direccion = input("Nueva dirección: ").strip()
                    if nueva_direccion:
                        c.direccion = nueva_direccion

                self.guardar_datos()
                logging.info(f"Contacto modificado: {nombre}")
                print("Contacto modificado correctamente.")
                return

        logging.warning(f"Contacto no encontrado para modificar: {nombre}")
        print("Contacto no encontrado.")

    def eliminar(self):

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

    def contar(self):

        total = len(self.contactos)
        print(f"Existen {total} contactos en la agenda.")

    def eliminar_agenda(self):

        confirmacion = input("¿Seguro que quieres eliminar toda la agenda? (s/n): ").lower()

        if confirmacion != "s":
            print("Operación cancelada.")
            return

        self.contactos.clear()
        self.guardar_datos()

        logging.info("Agenda eliminada completamente.")
        print("Agenda eliminada correctamente.")

    def ordenar_por_nombre(self):

        self.contactos.sort(key=lambda c: c.nombre.lower())
        self.guardar_datos()

        logging.info("Contactos ordenados por nombre.")
        print("Contactos ordenados por nombre.")


# =====================================================
# MENÚ PRINCIPAL
# =====================================================
# Menú de opciones del programa.
# La adaptación pedida por el ejercicio no está aquí,
# sino dentro del método insertar().

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
        print("9. Ordenar contactos")
        print("10. Eliminar agenda")
        print("11. Salir")

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
            agenda.ordenar_por_nombre()
        elif opcion == 10:
            agenda.eliminar_agenda()
        elif opcion == 11:
            logging.info("Aplicación cerrada por el usuario.")
            print("Saliendo del programa...")
            break
        else:
            logging.warning("Opción de menú fuera de rango.")
            print("Opción inválida.")


# =====================================================
# EJECUCIÓN
# =====================================================

if __name__ == "__main__":
    menu()
