import json
from typing import List, Optional
import os


class Producto:
    def __init__(self, id_producto: str, nombre: str, cantidad: int, precio: float):
        self._id = id_producto
        self._nombre = nombre
        self._cantidad = cantidad
        self._precio = precio

    def to_dict(self) -> dict:
        """Convierte el producto a un diccionario para almacenamiento."""
        return {
            'id': self._id,
            'nombre': self._nombre,
            'cantidad': self._cantidad,
            'precio': self._precio
        }

    @classmethod
    def from_dict(cls, data: dict) -> 'Producto':
        """Crea una instancia de Producto desde un diccionario."""
        return cls(
            id_producto=data['id'],
            nombre=data['nombre'],
            cantidad=data['cantidad'],
            precio=data['precio']
        )

    # Los métodos getter y setter se mantienen igual
    def get_id(self) -> str:
        return self._id

    def get_nombre(self) -> str:
        return self._nombre

    def get_cantidad(self) -> int:
        return self._cantidad

    def get_precio(self) -> float:
        return self._precio

    def set_nombre(self, nombre: str) -> None:
        self._nombre = nombre

    def set_cantidad(self, cantidad: int) -> None:
        self._cantidad = cantidad

    def set_precio(self, precio: float) -> None:
        self._precio = precio


class Inventario:
    ARCHIVO_INVENTARIO = "inventario.json"

    def __init__(self):
        self._productos: List[Producto] = []
        self.cargar_inventario()

    def guardar_inventario(self) -> bool:
        """
        Guarda el inventario actual en un archivo JSON.
        Retorna True si la operación fue exitosa, False en caso contrario.
        """
        try:
            datos = [producto.to_dict() for producto in self._productos]
            with open(self.ARCHIVO_INVENTARIO, 'w', encoding='utf-8') as archivo:
                json.dump(datos, archivo, indent=2)
            return True
        except (PermissionError, OSError) as e:
            print(f"Error al guardar el inventario: {str(e)}")
            return False

    def cargar_inventario(self) -> None:
        """
        Carga el inventario desde el archivo JSON.
        Si el archivo no existe, crea un inventario vacío.
        """
        try:
            if os.path.exists(self.ARCHIVO_INVENTARIO):
                with open(self.ARCHIVO_INVENTARIO, 'r', encoding='utf-8') as archivo:
                    datos = json.load(archivo)
                    self._productos = [Producto.from_dict(item) for item in datos]
            else:
                self._productos = []
                # Crear el archivo vacío
                self.guardar_inventario()
        except json.JSONDecodeError:
            print("Error: El archivo de inventario está corrupto. Creando nuevo inventario.")
            self._productos = []
            self.guardar_inventario()
        except Exception as e:
            print(f"Error al cargar el inventario: {str(e)}")
            self._productos = []

    def anadir_producto(self, producto: Producto) -> bool:
        """
        Añade un nuevo producto al inventario y actualiza el archivo.
        Retorna True si la operación fue exitosa, False en caso contrario.
        """
        if not any(p.get_id() == producto.get_id() for p in self._productos):
            self._productos.append(producto)
            if self.guardar_inventario():
                return True
        return False

    def eliminar_producto(self, id_producto: str) -> bool:
        """
        Elimina un producto del inventario y actualiza el archivo.
        Retorna True si la operación fue exitosa, False en caso contrario.
        """
        longitud_anterior = len(self._productos)
        self._productos = [p for p in self._productos if p.get_id() != id_producto]
        if len(self._productos) < longitud_anterior:
            return self.guardar_inventario()
        return False

    def actualizar_producto(self, id_producto: str, cantidad: Optional[int] = None,
                            precio: Optional[float] = None) -> bool:
        """
        Actualiza un producto en el inventario y en el archivo.
        Retorna True si la operación fue exitosa, False en caso contrario.
        """
        for p in self._productos:
            if p.get_id() == id_producto:
                if cantidad is not None:
                    p.set_cantidad(cantidad)
                if precio is not None:
                    p.set_precio(precio)
                return self.guardar_inventario()
        return False

    def buscar_productos(self, nombre: str) -> List[Producto]:
        """Busca productos por nombre (puede haber nombres similares)."""
        return [p for p in self._productos if nombre.lower() in p.get_nombre().lower()]

    def mostrar_productos(self) -> None:
        """Muestra todos los productos en el inventario."""
        if not self._productos:
            print("El inventario está vacío.")
            return
        for p in self._productos:
            print(f"ID: {p.get_id()}, Nombre: {p.get_nombre()}, "
                  f"Cantidad: {p.get_cantidad()}, Precio: {p.get_precio()}")

    def vender_producto(self, id_producto: str, cantidad: int) -> float:
        """
        Vende un producto y actualiza el inventario.
        Retorna el total de la venta si es exitosa, 0 en caso contrario.
        """
        for p in self._productos:
            if p.get_id() == id_producto:
                if p.get_cantidad() >= cantidad:
                    p.set_cantidad(p.get_cantidad() - cantidad)
                    if self.guardar_inventario():
                        return p.get_precio() * cantidad
                    else:
                        print("Error: No se pudo actualizar el inventario después de la venta.")
                        return 0
                else:
                    print("Error: Cantidad insuficiente en el inventario.")
                    return 0
        print("Error: Producto no encontrado.")
        return 0


class Caja:
    def __init__(self):
        self._dinero = 0.0

    def agregar_dinero(self, cantidad: float) -> None:
        self._dinero += cantidad

    def mostrar_dinero(self) -> None:
        print(f"Dinero en caja: {self._dinero:.2f}")


def validar_entrada_numerica(prompt: str, tipo: type) -> Optional[type]:
    """
    Valida la entrada numérica del usuario.
    Retorna None si la entrada está vacía o no es válida.
    """
    try:
        entrada = input(prompt)
        if entrada.strip() == "":
            return None
        return tipo(entrada)
    except ValueError:
        print(f"Error: Por favor ingrese un valor {tipo.__name__} válido.")
        return None


def menu():
    """Función principal que maneja el menú interactivo."""
    try:
        inventario = Inventario()
        caja = Caja()

        while True:
            print("\n=== Sistema de Gestión de Inventario ===")
            print("1. Añadir nuevo producto")
            print("2. Eliminar producto por ID")
            print("3. Actualizar cantidad o precio de un producto")
            print("4. Buscar productos por nombre")
            print("5. Mostrar todos los productos")
            print("6. Realizar una venta")
            print("7. Mostrar dinero en caja")
            print("8. Salir")

            opcion = input("\nSeleccione una opción: ")

            if opcion == '1':
                id_producto = input("ID del producto: ")
                nombre = input("Nombre del producto: ")
                cantidad = validar_entrada_numerica("Cantidad del producto: ", int)
                precio = validar_entrada_numerica("Precio del producto: ", float)

                if cantidad is not None and precio is not None:
                    producto = Producto(id_producto, nombre, cantidad, precio)
                    if inventario.anadir_producto(producto):
                        print("✓ Producto añadido y guardado exitosamente.")
                    else:
                        print("✗ Error: El ID del producto ya existe o no se pudo guardar.")

            elif opcion == '2':
                id_producto = input("ID del producto a eliminar: ")
                if inventario.eliminar_producto(id_producto):
                    print("✓ Producto eliminado y cambios guardados exitosamente.")
                else:
                    print("✗ Error: No se encontró el producto o no se pudo guardar el cambio.")

            elif opcion == '3':
                id_producto = input("ID del producto a actualizar: ")
                cantidad = validar_entrada_numerica(
                    "Nueva cantidad (Enter para no cambiar): ", int)
                precio = validar_entrada_numerica(
                    "Nuevo precio (Enter para no cambiar): ", float)

                if inventario.actualizar_producto(id_producto, cantidad, precio):
                    print("✓ Producto actualizado y guardado exitosamente.")
                else:
                    print("✗ Error: No se encontró el producto o no se pudo guardar.")

            elif opcion == '4':
                nombre = input("Nombre del producto a buscar: ")
                productos = inventario.buscar_productos(nombre)
                if productos:
                    print("\nProductos encontrados:")
                    for p in productos:
                        print(f"ID: {p.get_id()}, Nombre: {p.get_nombre()}, "
                              f"Cantidad: {p.get_cantidad()}, Precio: {p.get_precio()}")
                else:
                    print("No se encontraron productos con ese nombre.")

            elif opcion == '5':
                print("\nProductos en el inventario:")
                inventario.mostrar_productos()

            elif opcion == '6':
                id_producto = input("ID del producto a vender: ")
                cantidad = validar_entrada_numerica("Cantidad a vender: ", int)

                if cantidad is not None:
                    total_venta = inventario.vender_producto(id_producto, cantidad)
                    if total_venta > 0:
                        caja.agregar_dinero(total_venta)
                        print(f"✓ Venta realizada exitosamente. Total: {total_venta:.2f}")

            elif opcion == '7':
                caja.mostrar_dinero()

            elif opcion == '8':
                print("Guardando cambios y saliendo del programa...")
                if inventario.guardar_inventario():
                    print("✓ Cambios guardados exitosamente.")
                break

            else:
                print("Opción no válida. Por favor, intente de nuevo.")

    except Exception as e:
        print(f"Error inesperado: {str(e)}")
        print("El programa se cerrará después de intentar guardar el inventario...")
        inventario.guardar_inventario()


if __name__ == "__main__":
    menu()