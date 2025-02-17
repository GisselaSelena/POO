class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        # Constructor que inicializa los atributos del producto
        self._id = id_producto  # ID único del producto
        self._nombre = nombre  # Nombre del producto
        self._cantidad = cantidad  # Cantidad disponible del producto
        self._precio = precio  # Precio del producto

    # Métodos getter para acceder a los atributos
    def get_id(self):
        return self._id

    def get_nombre(self):
        return self._nombre

    def get_cantidad(self):
        return self._cantidad

    def get_precio(self):
        return self._precio

    # Métodos setter para modificar los atributos
    def set_nombre(self, nombre):
        self._nombre = nombre

    def set_cantidad(self, cantidad):
        self._cantidad = cantidad

    def set_precio(self, precio):
        self._precio = precio


class Inventario:
    def __init__(self):
        self._productos = []  # Lista para almacenar los productos

    def anadir_producto(self, producto):
        # Añadir un nuevo producto asegurándose de que el ID sea único
        if not any(p.get_id() == producto.get_id() for p in self._productos):
            self._productos.append(producto)
            return True
        return False

    def eliminar_producto(self, id_producto):
        # Eliminar un producto por su ID
        self._productos = [p for p in self._productos if p.get_id() != id_producto]

    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        # Actualizar la cantidad o el precio de un producto por su ID
        for p in self._productos:
            if p.get_id() == id_producto:
                if cantidad is not None:
                    p.set_cantidad(cantidad)
                if precio is not None:
                    p.set_precio(precio)
                return True
        return False

    def buscar_productos(self, nombre):
        # Buscar productos por nombre (puede haber nombres similares)
        return [p for p in self._productos if nombre.lower() in p.get_nombre().lower()]

    def mostrar_productos(self):
        # Mostrar todos los productos en el inventario
        for p in self._productos:
            print(f"ID: {p.get_id()}, Nombre: {p.get_nombre()}, Cantidad: {p.get_cantidad()}, Precio: {p.get_precio()}")

    def vender_producto(self, id_producto, cantidad):
        # Vender un producto y actualizar la cantidad en el inventario
        for p in self._productos:
            if p.get_id() == id_producto:
                if p.get_cantidad() >= cantidad:
                    p.set_cantidad(p.get_cantidad() - cantidad)
                    return p.get_precio() * cantidad  # Retorna el total de la venta
                else:
                    print("Error: Cantidad insuficiente en el inventario.")
                    return 0
        print("Error: Producto no encontrado.")
        return 0


class Caja:
    def __init__(self):
        self._dinero = 0.0  # Inicializar el dinero en caja

    def agregar_dinero(self, cantidad):
        # Agregar dinero a la caja
        self._dinero += cantidad

    def mostrar_dinero(self):
        # Mostrar el dinero en caja
        print(f"Dinero en caja: {self._dinero}")


def menu():
    inventario = Inventario()  # Crear una instancia de Inventario
    caja = Caja()  # Crear una instancia de Caja
    while True:
        # Menú interactivo en la consola
        print("\n--- Menú de Inventario ---")
        print("1. Añadir nuevo producto")
        print("2. Eliminar producto por ID")
        print("3. Actualizar cantidad o precio de un producto por ID")
        print("4. Buscar producto(s) por nombre")
        print("5. Mostrar todos los productos en el inventario")
        print("6. Realizar una venta")
        print("7. Mostrar dinero en caja")
        print("8. Salir")
        opcion = input("Selecciona una opción: ")

        if opcion == '1':
            # Añadir nuevo producto
            id_producto = input("ID del producto: ")
            nombre = input("Nombre del producto: ")
            cantidad = int(input("Cantidad del producto: "))
            precio = float(input("Precio del producto: "))
            producto = Producto(id_producto, nombre, cantidad, precio)
            if inventario.anadir_producto(producto):
                print("Producto añadido con éxito.")
            else:
                print("Error: El ID del producto ya existe.")
        elif opcion == '2':

            # Eliminar producto por ID
            id_producto = input("ID del producto a eliminar: ")
            inventario.eliminar_producto(id_producto)
            print("Producto eliminado con éxito.")
        elif opcion == '3':
            # Actualizar cantidad o precio de un producto por ID
            id_producto = input("ID del producto a actualizar: ")
            cantidad = input("Nueva cantidad (dejar en blanco para no actualizar): ")
            precio = input("Nuevo precio (dejar en blanco para no actualizar): ")
            cantidad = int(cantidad) if cantidad else None  # Convertir a int o None
            precio = float(precio) if precio else None  # Convertir a float o None
            if inventario.actualizar_producto(id_producto, cantidad, precio):
                print("Producto actualizado con éxito.")
            else:
                print("Error: No se encontró el producto con el ID proporcionado.")
        elif opcion == '4':
            # Buscar producto(s) por nombre
            nombre = input("Nombre del producto a buscar: ")
            productos = inventario.buscar_productos(nombre)
            if productos:
                print("Productos encontrados:")
                for p in productos:
                    print(
                        f"ID: {p.get_id()}, Nombre: {p.get_nombre()}, Cantidad: {p.get_cantidad()}, Precio: {p.get_precio()}")
            else:
                print("No se encontraron productos con ese nombre.")
        elif opcion == '5':
            # Mostrar todos los productos en el inventario
            print("Productos en el inventario:")
            inventario.mostrar_productos()
        elif opcion == '6':
            # Realizar una venta
            id_producto = input("ID del producto a vender: ")
            cantidad = int(input("Cantidad a vender: "))
            total_venta = inventario.vender_producto(id_producto, cantidad)
            if total_venta > 0:
                caja.agregar_dinero(total_venta)  # Agregar el total de la venta a la caja
                print(f"Venta realizada con éxito. Total: {total_venta}")
        elif opcion == '7':
            # Mostrar dinero en caja
            caja.mostrar_dinero()
        elif opcion == '8':
            # Salir del programa
            print("Saliendo del programa.")
            break
        else:
            print("Opción no válida. Por favor, intenta de nuevo.")


if __name__ == "__main__":
    menu()  # Ejecutar el menú al iniciar el programa