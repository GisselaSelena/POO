class Autor:
    def __init__(self, nombre, nacionalidad):
        """
        Inicializa un nuevo autor con nombre y nacionalidad.
        :param nombre: Nombre del autor.
        :param nacionalidad: Nacionalidad del autor.
        """
        self.nombre = nombre
        self.nacionalidad = nacionalidad

    def __str__(self):
        """
        Devuelve una representación en cadena del autor.
        """
        return f"{self.nombre} ({self.nacionalidad})"


class Libro:
    def __init__(self, titulo, autor, isbn):
        """
        Inicializa un nuevo libro con título, autor e ISBN.
        :param titulo: Título del libro.
        :param autor: Objeto Autor del libro.
        :param isbn: ISBN del libro.
        """
        self.titulo = titulo
        self.autor = autor
        self.isbn = isbn
        self.disponible = True  # Indica si el libro está disponible para prestar

    def prestar(self):
        """
        Marca el libro como prestado.
        :return: True si se pudo prestar, False si ya está prestado.
        """
        if self.disponible:
            self.disponible = False
            return True
        return False

    def devolver(self):
        """
        Marca el libro como disponible.
        """
        self.disponible = True

    def __str__(self):
        """
        Devuelve una representación en cadena del libro.
        """
        estado = "Disponible" if self.disponible else "Prestado"
        return f"Título: {self.titulo}, Autor: {self.autor}, ISBN: {self.isbn}, Estado: {estado}"


class Biblioteca:
    def __init__(self):
        """
        Inicializa una nueva biblioteca con una lista de libros.
        """
        self.libros = []  # Lista de libros en la biblioteca

    def agregar_libro(self, libro):
        """
        Agrega un libro a la biblioteca.
        :param libro: Objeto Libro que se desea agregar.
        """
        self.libros.append(libro)

    def mostrar_libros(self):
        """
        Muestra todos los libros disponibles en la biblioteca.
        """
        for libro in self.libros:
            print(libro)


# Ejemplo de uso del sistema de gestión de obras literarias
if __name__ == "__main__":
    # Crear autores
    autor1 = Autor("Gabriel García Márquez", "Colombia")
    autor2 = Autor("Jorge Luis Borges", "Argentina")

    # Crear una biblioteca
    biblioteca = Biblioteca()

    # Agregar libros a la biblioteca
    libro1 = Libro("Cien años de soledad", autor1, "123456789")
    libro2 = Libro("Ficciones", autor2, "987654321")
    biblioteca.agregar_libro(libro1)
    biblioteca.agregar_libro(libro2)

    # Mostrar libros disponibles
    print("Libros en la biblioteca:")
    biblioteca.mostrar_libros()

    # Prestar un libro
    print(f"\nIntentando prestar '{libro1.titulo}':")
    if libro1.prestar():
        print(f"El libro '{libro1.titulo}' ha sido prestado.")
    else:
        print(f"El libro '{libro1.titulo}' no está disponible.")

    # Mostrar libros después del préstamo
    print("\nLibros en la biblioteca después del préstamo:")
    biblioteca.mostrar_libros()

    # Devolver el libro
    libro1.devolver()
    print(f"\nEl libro '{libro1.titulo}' ha sido devuelto.")

    # Mostrar libros después de la devolución
    print("\nLibros en la biblioteca después de la devolución:")
    biblioteca.mostrar_libros()