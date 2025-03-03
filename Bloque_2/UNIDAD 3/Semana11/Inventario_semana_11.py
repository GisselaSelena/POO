import json  # Importamos el módulo json para manejar la serialización y deserialización de datos.


# Clase que representa un producto en el inventario.
class Producto:
    def __init__(self, id_producto, nombre, cantidad, precio):
        self.id_producto = id_producto  # ID único del producto
        self.nombre = nombre  # Nombre del producto
        self.cantidad = cantidad  # Cantidad disponible del producto
        self.precio = precio  # Precio del producto

    # Métodos para obtener los atributos del producto.
    def obtener_id(self):
        return self.id_producto

    def obtener_nombre(self):
        return self.nombre

    def obtener_cantidad(self):
        return self.cantidad

    def obtener_precio(self):
        return self.precio

    # Métodos para establecer los atributos del producto.
    def establecer_cantidad(self, cantidad):
        self.cantidad = cantidad

    def establecer_precio(self, precio):
        self.precio = precio

    # Método para convertir el objeto Producto a un diccionario.
    def to_dict(self):
        return {
            'id_producto': self.id_producto,
            'nombre': self.nombre,
            'cantidad': self.cantidad,
            'precio': self.precio
        }


# Clase que representa el inventario de productos.
class Inventario:
    def __init__(self):
        self.productos = {}  # Diccionario para almacenar productos, donde la clave es el ID del producto
        self.total_ventas = 0  # Total de ventas realizadas
        self.codigo_venta = 1  # Código de venta autogenerado

    # Método para añadir un nuevo producto al inventario.
    def añadir_producto(self, producto):
        if producto.obtener_id() in self.productos:
            print("El producto ya existe en el inventario.")
        else:
            self.productos[producto.obtener_id()] = producto  # Añadimos el producto al diccionario
            print("Producto añadido al inventario.")

    # Método para eliminar un producto del inventario por su ID.
    def eliminar_producto(self, id_producto):
        if id_producto in self.productos:
            del self.productos[id_producto]  # Eliminamos el producto del diccionario
            print("Producto eliminado del inventario.")
        else:
            print("Producto no encontrado.")

    # Método para actualizar la cantidad o el precio de un producto.
    def actualizar_producto(self, id_producto, cantidad=None, precio=None):
        if id_producto in self.productos:
            if cantidad is not None:
                self.productos[id_producto].establecer_cantidad(cantidad)  # Actualizamos la cantidad
            if precio is not None:
                self.productos[id_producto].establecer_precio(precio)  # Actualizamos el precio
            print("Producto actualizado.")
        else:
            print("Producto no encontrado.")

    # Método para buscar productos por nombre.
    def buscar_producto(self, nombre):
        encontrados = [producto for producto in self.productos.values() if
                       nombre.lower() in producto.obtener_nombre().lower()]
        if encontrados:
            for producto in encontrados:
                # Mostramos los detalles de los productos encontrados.
                print(
                    f"ID: {producto.obtener_id()}, Nombre: {producto.obtener_nombre()}, Cantidad: {producto.obtener_cantidad()}, Precio: {producto.obtener_precio()}")
        else:
            print("No se encontraron productos con ese nombre.")

    # Método para mostrar todos los productos en el inventario.
    def mostrar_productos(self):
        if not self.productos:
            print("El inventario está vacío.")
        else:
            for producto in self.productos.values():
                # Mostramos los detalles de cada producto en el inventario.
                print(
                    f"ID: {producto.obtener_id()}, Nombre: {producto.obtener_nombre()}, Cantidad: {producto.obtener_cantidad()}, Precio: {producto.obtener_precio()}")

    # Método para registrar una venta de un producto.
    def registrar_venta(self, id_producto, cantidad_vendida):
        if id_producto in self.productos and self.productos[id_producto].obtener_cantidad() >= cantidad_vendida:
            total_venta = cantidad_vendida * self.productos[
                id_producto].obtener_precio()  # Calculamos el total de la venta
            self.productos[id_producto].establecer_cantidad(self.productos[
                                                                id_producto].obtener_cantidad() - cantidad_vendida)  # Actualizamos la cantidad en el inventario
            self.total_ventas += total_venta  # Actualizamos el total de ventas
            codigo = self.codigo_venta  # Guardamos el código de la venta
            self.codigo_venta += 1  # Incrementamos el código de venta para la próxima transacción
            print(
                f"Venta registrada: Código {codigo}, Producto: {self.productos[id_producto].obtener_nombre()}, Cantidad: {cantidad_vendida}, Total: {total_venta}")
        else:
            print("No hay suficiente stock para realizar la venta.")

    # Método para procesar una devolución de un producto.
    def procesar_devolucion(self, codigo_venta, id_producto, cantidad_devuelta):
        if id_producto in self.productos:
            self.productos[id_producto].establecer_cantidad(self.productos[
                                                                id_producto].obtener_cantidad() + cantidad_devuelta)  # Aumentamos la cantidad en el inventario
            total_devolucion = cantidad_devuelta * self.productos[
                id_producto].obtener_precio()  # Calculamos el total de la devolución
            self.total_ventas -= total_devolucion  # Actualizamos el total de ventas
            print(
                f"Devolución procesada: Código {codigo_venta}, Producto: {self.productos[id_producto].obtener_nombre()}, Cantidad: {cantidad_devuelta}, Total: {total_devolucion}")
        else:
            print("El producto no existe en el inventario.")

    # Método para guardar el inventario en un archivo JSON.
    def guardar_inventario(self, archivo):
        with open(archivo, 'w') as f:
            json.dump({id: producto.to_dict() for id, producto in self.productos.items()},
                      f)  # Serializamos el diccionario de productos a formato JSON
        print("Inventario guardado en el archivo.")

    # Método para cargar el inventario desde un archivo JSON.
    def cargar_inventario(self, archivo):
        try:
            with open(archivo, 'r') as f:
                data = json.load(f)  # Deserializamos el contenido del archivo JSON a un diccionario de productos
                self.productos = {id: Producto(**producto) for id, producto in
                                  data.items()}  # Creamos objetos Producto a partir del diccionario
            print("Inventario cargado desde el archivo.")
        except FileNotFoundError:
            print("El archivo no existe.")
        except json.JSONDecodeError:
            print("Error al leer el archivo.")


# Función que muestra un menú interactivo para gestionar el inventario.
def menu():
    inventario = Inventario()  # Creamos una instancia de la clase Inventario.
    inventario.cargar_inventario('inventario.json')  # Cargamos el inventario desde un archivo JSON.

    while True:  # Bucle infinito para mostrar el menú hasta que el usuario decida salir.
        print("\nMenú de Inventario:")
        print("1. Añadir producto")
        print("2. Eliminar producto")
        print("3. Actualizar producto")
        print("4. Buscar producto")
        print("5. Mostrar todos los productos")
        print("6. Registrar venta")
        print("7. Procesar devolución")
        print("8. Guardar inventario")
        print("9. Salir")

        opcion = input("Seleccione una opción: ")  # Pedimos al usuario que seleccione una opción.

        if opcion == '1':
            # Añadir un nuevo producto.
            id_producto = input("ID del producto: ")
            nombre = input("Nombre del producto: ")
            cantidad = int(input("Cantidad: "))
            precio = float(input("Precio: "))
            producto = Producto(id_producto, nombre, cantidad, precio)  # Creamos un nuevo objeto Producto.
            inventario.añadir_producto(producto)  # Añadimos el producto al inventario.

        elif opcion == '2':
            # Eliminar un producto.
            id_producto = input("ID del producto a eliminar: ")
            inventario.eliminar_producto(id_producto)  # Llamamos al método para eliminar el producto.

        elif opcion == '3':
            # Actualizar un producto existente.
            id_producto = input("ID del producto a actualizar: ")
            cantidad = input("Nueva cantidad (dejar en blanco si no se desea cambiar): ")
            precio = input("Nuevo precio (dejar en blanco si no se desea cambiar): ")

            # Convertimos los valores a los tipos adecuados si no están vacíos.
            if cantidad:
                cantidad = int(cantidad)
            else:
                cantidad = None

            if precio:
                precio = float(precio)
            else:
                precio = None

            inventario.actualizar_producto(id_producto, cantidad, precio)  # Actualizamos el producto.

        elif opcion == '4':
            # Buscar un producto por nombre.
            nombre = input("Nombre del producto a buscar: ")
            inventario.buscar_producto(nombre)  # Llamamos al método para buscar el producto.

        elif opcion == '5':
            # Mostrar todos los productos en el inventario.
            inventario.mostrar_productos()  # Llamamos al método para mostrar los productos.

        elif opcion == '6':
            # Registrar una venta.
            id_producto = input("ID del producto a vender: ")
            cantidad_vendida = int(input("Cantidad a vender: "))
            inventario.registrar_venta(id_producto, cantidad_vendida)  # Llamamos al método para registrar la venta.

        elif opcion == '7':
            # Procesar una devolución.
            codigo_venta = input("Código de la venta a devolver: ")
            id_producto = input("ID del producto a devolver: ")
            cantidad_devuelta = int(input("Cantidad a devolver: "))
            inventario.procesar_devolucion(codigo_venta, id_producto,
                                           cantidad_devuelta)  # Llamamos al método para procesar la devolución.

        elif opcion == '8':
            # Guardar el inventario en un archivo.
            inventario.guardar_inventario('inventario.json')  # Llamamos al método para guardar el inventario.

        elif opcion == '9':
            # Salir del programa.
            print("Saliendo del programa.")
            break  # Salimos del bucle y terminamos el programa.

        else:
            print("Opción no válida. Intente de nuevo.")  # Mensaje de error si la opción no es válida.


# Punto de entrada del programa.
if __name__ == "__main__":
    menu()  # Llamamos a la función menu para iniciar el programa.