import json
import os


class Libro:
    """
    Clase que representa un libro en la biblioteca digital.
    Utiliza tuplas para almacenar autor y título ya que son inmutables.
    """

    def __init__(self, titulo, autor, categoria, isbn):
        self.datos = (titulo, autor)  # Tupla inmutable para título y autor
        self.categoria = categoria
        self.isbn = isbn
        self.disponible = True

    @property
    def titulo(self):
        return self.datos[0]

    @property
    def autor(self):
        return self.datos[1]

    def __str__(self):
        estado = "Disponible" if self.disponible else "Prestado"
        return f"Libro: {self.titulo} | Autor: {self.autor} | Categoría: {self.categoria} | ISBN: {self.isbn} | Estado: {estado}"


class Usuario:
    """
    Clase que representa a un usuario de la biblioteca digital.
    Mantiene un registro de los libros actualmente prestados al usuario.
    """

    def __init__(self, nombre, id_usuario):
        self.nombre = nombre
        self.id_usuario = id_usuario
        self.libros_prestados = []  # Lista para almacenar los libros prestados

    def prestar_libro(self, libro):
        """Añade un libro a la lista de libros prestados del usuario."""
        self.libros_prestados.append(libro)

    def devolver_libro(self, isbn):
        """Elimina un libro de la lista de libros prestados del usuario."""
        for i, libro in enumerate(self.libros_prestados):
            if libro.isbn == isbn:
                return self.libros_prestados.pop(i)
        return None

    def listar_libros_prestados(self):
        """Devuelve una lista de los libros prestados al usuario."""
        return self.libros_prestados

    def __str__(self):
        return f"Usuario: {self.nombre} | ID: {self.id_usuario} | Libros prestados: {len(self.libros_prestados)}"


class Biblioteca:
    """
    Clase principal que gestiona la biblioteca digital.
    Utiliza estructuras de datos eficientes: diccionarios para libros y conjunto para IDs de usuario.
    Implementa persistencia de datos con archivos JSON.
    """

    def __init__(self, cargar_datos=True):
        self.libros = {}  # Diccionario con ISBN como clave y objeto Libro como valor
        self.usuarios = {}  # Diccionario con ID como clave y objeto Usuario como valor
        self.ids_usuario = set()  # Conjunto para asegurar IDs de usuario únicos

        # Archivos para persistencia de datos
        self.archivo_libros = "libros.json"
        self.archivo_usuarios = "usuarios.json"

        # Cargar datos si existen y se solicita
        if cargar_datos:
            self.cargar_datos()

    def agregar_libro(self, libro):
        """Añade un nuevo libro a la biblioteca."""
        if libro.isbn in self.libros:
            return False
        self.libros[libro.isbn] = libro
        return True

    def quitar_libro(self, isbn):
        """Elimina un libro de la biblioteca por su ISBN."""
        if isbn in self.libros and self.libros[isbn].disponible:
            del self.libros[isbn]
            return True
        return False

    def registrar_usuario(self, usuario):
        """Registra un nuevo usuario en la biblioteca."""
        if usuario.id_usuario in self.ids_usuario:
            return False
        self.ids_usuario.add(usuario.id_usuario)
        self.usuarios[usuario.id_usuario] = usuario
        return True

    def dar_baja_usuario(self, id_usuario):
        """Da de baja a un usuario existente."""
        if id_usuario in self.ids_usuario:
            # Verificar que el usuario no tenga libros prestados
            if len(self.usuarios[id_usuario].libros_prestados) == 0:
                self.ids_usuario.remove(id_usuario)
                del self.usuarios[id_usuario]
                return True
        return False

    def prestar_libro(self, isbn, id_usuario):
        """Presta un libro a un usuario."""
        if isbn in self.libros and id_usuario in self.ids_usuario:
            libro = self.libros[isbn]
            if libro.disponible:
                libro.disponible = False
                self.usuarios[id_usuario].prestar_libro(libro)
                return True
        return False

    def devolver_libro(self, isbn, id_usuario):
        """Procesa la devolución de un libro."""
        if id_usuario in self.ids_usuario:
            libro_devuelto = self.usuarios[id_usuario].devolver_libro(isbn)
            if libro_devuelto:
                libro_devuelto.disponible = True
                return True
        return False

    def buscar_por_titulo(self, titulo):
        """Busca libros por título."""
        return [libro for libro in self.libros.values() if titulo.lower() in libro.titulo.lower()]

    def buscar_por_autor(self, autor):
        """Busca libros por autor."""
        return [libro for libro in self.libros.values() if autor.lower() in libro.autor.lower()]

    def buscar_por_categoria(self, categoria):
        """Busca libros por categoría."""
        return [libro for libro in self.libros.values() if categoria.lower() == libro.categoria.lower()]

    def listar_libros_usuario(self, id_usuario):
        """Lista los libros prestados a un usuario específico."""
        if id_usuario in self.ids_usuario:
            return self.usuarios[id_usuario].listar_libros_prestados()
        return []

    def listar_todos_libros(self):
        """Lista todos los libros de la biblioteca."""
        return list(self.libros.values())

    def listar_todos_usuarios(self):
        """Lista todos los usuarios registrados."""
        return list(self.usuarios.values())

    def guardar_datos(self):
        """Guarda los datos de la biblioteca en archivos JSON."""
        # Guardar libros
        libros_data = {}
        for isbn, libro in self.libros.items():
            libros_data[isbn] = {
                "titulo": libro.titulo,
                "autor": libro.autor,
                "categoria": libro.categoria,
                "isbn": libro.isbn,
                "disponible": libro.disponible
            }

        try:
            with open(self.archivo_libros, 'w') as f:
                json.dump(libros_data, f, indent=4)
        except Exception as e:
            print(f"Error al guardar libros: {e}")

        # Guardar usuarios
        usuarios_data = {}
        for id_usuario, usuario in self.usuarios.items():
            libros_prestados_ids = [libro.isbn for libro in usuario.libros_prestados]
            usuarios_data[id_usuario] = {
                "nombre": usuario.nombre,
                "id_usuario": usuario.id_usuario,
                "libros_prestados": libros_prestados_ids
            }

        try:
            with open(self.archivo_usuarios, 'w') as f:
                json.dump(usuarios_data, f, indent=4)
        except Exception as e:
            print(f"Error al guardar usuarios: {e}")

        print("✓ Datos guardados correctamente.")

    def cargar_datos(self):
        """Carga los datos de la biblioteca desde archivos JSON."""
        # Cargar libros
        if os.path.exists(self.archivo_libros):
            with open(self.archivo_libros, 'r', encoding='utf-8') as f:
                libros_data = json.load(f)

            for isbn, libro_data in libros_data.items():
                libro = Libro(
                    libro_data["titulo"],
                    libro_data["autor"],
                    libro_data["categoria"],
                    libro_data["isbn"]
                )
                libro.disponible = libro_data["disponible"]
                self.libros[isbn] = libro

        # Cargar usuarios
        if os.path.exists(self.archivo_usuarios):
            with open(self.archivo_usuarios, 'r', encoding='utf-8') as f:
                usuarios_data = json.load(f)

            for id_usuario, usuario_data in usuarios_data.items():
                usuario = Usuario(
                    usuario_data["nombre"],
                    usuario_data["id_usuario"]
                )
                self.usuarios[id_usuario] = usuario
                self.ids_usuario.add(id_usuario)

                # Asignar libros prestados
                for isbn in usuario_data["libros_prestados"]:
                    if isbn in self.libros:
                        usuario.libros_prestados.append(self.libros[isbn])
                        self.libros[isbn].disponible = False


def menu_principal():
    """Muestra el menú principal del sistema de biblioteca digital."""
    print("\n===== SISTEMA DE GESTIÓN DE BIBLIOTECA DIGITAL =====")
    print("1. Gestión de Libros")
    print("2. Gestión de Usuarios")
    print("3. Préstamos y Devoluciones")
    print("4. Búsquedas")
    print("5. Guardar y Salir")
    return input("Seleccione una opción (1-5): ")


def menu_libros():
    """Muestra el menú de gestión de libros."""
    print("\n===== GESTIÓN DE LIBROS =====")
    print("1. Añadir libro")
    print("2. Quitar libro")
    print("3. Listar todos los libros")
    print("4. Volver al menú principal")
    return input("Seleccione una opción (1-4): ")


def menu_usuarios():
    """Muestra el menú de gestión de usuarios."""
    print("\n===== GESTIÓN DE USUARIOS =====")
    print("1. Registrar usuario")
    print("2. Dar de baja usuario")
    print("3. Listar todos los usuarios")
    print("4. Volver al menú principal")
    return input("Seleccione una opción (1-4): ")


def menu_prestamos():
    """Muestra el menú de préstamos y devoluciones."""
    print("\n===== PRÉSTAMOS Y DEVOLUCIONES =====")
    print("1. Prestar libro")
    print("2. Devolver libro")
    print("3. Listar libros prestados a usuario")
    print("4. Volver al menú principal")
    return input("Seleccione una opción (1-4): ")


def menu_busquedas():
    """Muestra el menú de búsquedas."""
    print("\n===== BÚSQUEDAS =====")
    print("1. Buscar por título")
    print("2. Buscar por autor")
    print("3. Buscar por categoría")
    print("4. Volver al menú principal")
    return input("Seleccione una opción (1-4): ")


def ejecutar_sistema():
    """Función principal que ejecuta el sistema de biblioteca digital interactivo."""
    biblioteca = Biblioteca(cargar_datos=True)

    # Datos de ejemplo si no hay datos cargados
    if not biblioteca.libros and not biblioteca.usuarios:
        print("Sistema inicializado con datos de ejemplo.")
        biblioteca.agregar_libro(Libro("Cien años de soledad", "Gabriel García Márquez", "Novela", "9780307476463"))
        biblioteca.agregar_libro(Libro("El Alquimista", "Paulo Coelho", "Ficción", "9780062315007"))
        biblioteca.agregar_libro(Libro("Don Quijote de la Mancha", "Miguel de Cervantes", "Clásico", "9788420412146"))
        biblioteca.registrar_usuario(Usuario("Ana García", "U001"))
        biblioteca.guardar_datos()
    else:
        print(f"✓ Datos cargados: {len(biblioteca.libros)} libros y {len(biblioteca.usuarios)} usuarios.")

    while True:
        opcion = menu_principal()

        if opcion == "1":  # Gestión de Libros
            while True:
                opcion_libros = menu_libros()

                if opcion_libros == "1":  # Añadir libro
                    titulo = input("Título: ")
                    autor = input("Autor: ")
                    categoria = input("Categoría: ")
                    isbn = input("ISBN: ")
                    libro = Libro(titulo, autor, categoria, isbn)
                    if biblioteca.agregar_libro(libro):
                        print(f"✓ Libro '{titulo}' añadido correctamente.")
                        biblioteca.guardar_datos()
                    else:
                        print(f"✗ Error: Ya existe un libro con ISBN {isbn}.")

                elif opcion_libros == "2":  # Quitar libro
                    isbn = input("ISBN del libro a quitar: ")
                    if biblioteca.quitar_libro(isbn):
                        print("✓ Libro eliminado correctamente.")
                        biblioteca.guardar_datos()
                    else:
                        print("✗ Error: El libro no existe o está prestado actualmente.")

                elif opcion_libros == "3":  # Listar todos los libros
                    print("\n===== CATÁLOGO DE LIBROS =====")
                    libros = biblioteca.listar_todos_libros()
                    if libros:
                        for libro in libros:
                            print(libro)
                    else:
                        print("No hay libros en la biblioteca.")

                elif opcion_libros == "4":  # Volver al menú principal
                    break

                else:
                    print("Opción no válida. Intente de nuevo.")

        elif opcion == "2":  # Gestión de Usuarios
            while True:
                opcion_usuarios = menu_usuarios()

                if opcion_usuarios == "1":  # Registrar usuario
                    nombre = input("Nombre: ")
                    id_usuario = input("ID de usuario: ")
                    usuario = Usuario(nombre, id_usuario)
                    if biblioteca.registrar_usuario(usuario):
                        print(f"✓ Usuario '{nombre}' registrado correctamente.")
                        biblioteca.guardar_datos()
                    else:
                        print(f"✗ Error: Ya existe un usuario con ID {id_usuario}.")

                elif opcion_usuarios == "2":  # Dar de baja usuario
                    id_usuario = input("ID del usuario a dar de baja: ")
                    if biblioteca.dar_baja_usuario(id_usuario):
                        print("✓ Usuario dado de baja correctamente.")
                        biblioteca.guardar_datos()
                    else:
                        print("✗ Error: El usuario no existe o tiene libros prestados.")

                elif opcion_usuarios == "3":  # Listar todos los usuarios
                    print("\n===== USUARIOS REGISTRADOS =====")
                    usuarios = biblioteca.listar_todos_usuarios()
                    if usuarios:
                        for usuario in usuarios:
                            print(usuario)
                    else:
                        print("No hay usuarios registrados.")

                elif opcion_usuarios == "4":  # Volver al menú principal
                    break

                else:
                    print("Opción no válida. Intente de nuevo.")

        elif opcion == "3":  # Préstamos y Devoluciones
            while True:
                opcion_prestamos = menu_prestamos()

                if opcion_prestamos == "1":  # Prestar libro
                    isbn = input("ISBN del libro a prestar: ")
                    id_usuario = input("ID del usuario: ")
                    if biblioteca.prestar_libro(isbn, id_usuario):
                        print("✓ Libro prestado correctamente.")
                        biblioteca.guardar_datos()
                    else:
                        print("✗ Error: Libro o usuario no encontrado, o el libro no está disponible.")

                elif opcion_prestamos == "2":  # Devolver libro
                    isbn = input("ISBN del libro a devolver: ")
                    id_usuario = input("ID del usuario: ")
                    if biblioteca.devolver_libro(isbn, id_usuario):
                        print("✓ Libro devuelto correctamente.")
                        biblioteca.guardar_datos()
                    else:
                        print("✗ Error: El usuario no tiene este libro prestado.")

                elif opcion_prestamos == "3":  # Listar libros prestados a usuario
                    id_usuario = input("ID del usuario: ")
                    print(f"\n===== LIBROS PRESTADOS AL USUARIO {id_usuario} =====")
                    libros = biblioteca.listar_libros_usuario(id_usuario)
                    if libros:
                        for libro in libros:
                            print(libro)
                    else:
                        print(f"El usuario {id_usuario} no tiene libros prestados o no existe.")

                elif opcion_prestamos == "4":  # Volver al menú principal
                    break

                else:
                    print("Opción no válida. Intente de nuevo.")

        elif opcion == "4":  # Búsquedas
            while True:
                opcion_busquedas = menu_busquedas()

                if opcion_busquedas == "1":  # Buscar por título
                    titulo = input("Título a buscar: ")
                    print(f"\n===== RESULTADOS DE BÚSQUEDA: TÍTULO '{titulo}' =====")
                    resultados = biblioteca.buscar_por_titulo(titulo)
                    if resultados:
                        for libro in resultados:
                            print(libro)
                    else:
                        print("No se encontraron libros con ese título.")

                elif opcion_busquedas == "2":  # Buscar por autor
                    autor = input("Autor a buscar: ")
                    print(f"\n===== RESULTADOS DE BÚSQUEDA: AUTOR '{autor}' =====")
                    resultados = biblioteca.buscar_por_autor(autor)
                    if resultados:
                        for libro in resultados:
                            print(libro)
                    else:
                        print("No se encontraron libros de ese autor.")

                elif opcion_busquedas == "3":  # Buscar por categoría
                    categoria = input("Categoría a buscar: ")
                    print(f"\n===== RESULTADOS DE BÚSQUEDA: CATEGORÍA '{categoria}' =====")
                    resultados = biblioteca.buscar_por_categoria(categoria)
                    if resultados:
                        for libro in resultados:
                            print(libro)
                    else:
                        print("No se encontraron libros en esa categoría.")

                elif opcion_busquedas == "4":  # Volver al menú principal
                    break

                else:
                    print("Opción no válida. Intente de nuevo.")

        elif opcion == "5":  # Salir
            biblioteca.guardar_datos()
            print("¡Gracias por usar el Sistema de Gestión de Biblioteca Digital!")
            break

        else:
            print("Opción no válida. Intente de nuevo.")


if __name__ == "__main__":
    ejecutar_sistema()