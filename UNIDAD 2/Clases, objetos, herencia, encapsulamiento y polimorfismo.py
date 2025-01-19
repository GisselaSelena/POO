# Clase base: Vehiculo
class Vehiculo:
    def __init__(self, marca, modelo, year):
        """
        Inicializa un objeto de la clase Vehiculo.

        :param marca: Marca del vehículo.
        :param modelo: Modelo del vehículo.
        :param year: Año de fabricación del vehículo.
        """
        self.marca = marca  # Atributo público que almacena la marca del vehículo
        self.modelo = modelo  # Atributo público que almacena el modelo del vehículo
        self.year = year  # Atributo público que almacena el año del vehículo

    def descripcion(self):
        """
        Devuelve una descripción del vehículo.

        :return: Cadena con la descripción del vehículo.
        """
        return f"{self.year} {self.marca} {self.modelo}"  # Descripción básica del vehículo


# Clase derivada: Coche
class Coche(Vehiculo):
    def __init__(self, marca, modelo, year, puertas):
        """
        Inicializa un objeto de la clase Coche.

        :param marca: Marca del coche.
        :param modelo: Modelo del coche.
        :param year: Año de fabricación del coche.
        :param puertas: Número de puertas del coche.
        """
        super().__init__(marca, modelo, year)  # Llama al constructor de la clase base
        self.__puertas = puertas  # Atributo privado que almacena el número de puertas

    def descripcion(self):
        """
        Devuelve una descripción del coche, sobrescribiendo el método de la clase base.

        :return: Cadena con la descripción del coche.
        """
        return f"{super().descripcion()} con {self.__puertas} puertas"  # Descripción del coche

    def get_puertas(self):
        """
        Método para acceder al atributo privado __puertas.

        :return: Número de puertas del coche.
        """
        return self.__puertas  # Devuelve el número de puertas

    def set_puertas(self, puertas):
        """
        Método para modificar el atributo privado __puertas.

        :param puertas: Nuevo número de puertas del coche.
        """
        if puertas > 0:
            self.__puertas = puertas  # Modifica el número de puertas si es válido
        else:
            print("El número de puertas debe ser positivo.")  # Mensaje de error


# Clase derivada: Motocicleta
class Motocicleta(Vehiculo):
    def __init__(self, marca, modelo, year, tipo):
        """
        Inicializa un objeto de la clase Motocicleta.

        :param marca: Marca de la motocicleta.
        :param modelo: Modelo de la motocicleta.
        :param year: Año de fabricación de la motocicleta.
        :param tipo: Tipo de motocicleta (ej. deportiva, cruiser).
        """
        super().__init__(marca, modelo,year)  # Llama al constructor de la clase base
        self.tipo = tipo  # Atributo público que almacena el tipo de motocicleta

    def descripcion(self):
        """
        Devuelve una descripción de la motocicleta, sobrescribiendo el método de la clase base.

        :return: Cadena con la descripción de la motocicleta.
        """
        return f"{super().descripcion()} de tipo {self.tipo}"  # Descripción de la motocicleta


# Función para mostrar la descripción de un vehículo
def mostrar_descripcion(vehiculo):
    """
    Función que utiliza polimorfismo para mostrar la descripción de un vehículo.

    :param vehiculo: Objeto de tipo Vehiculo (o sus derivados).
    """
    print(vehiculo.descripcion())  # Llama al método descripcion del objeto


# Creación de instancias de las clases
coche1 = Coche("Toyota", "Corolla", 2020, 4)  # Instancia de la clase Coche
motocicleta1 = Motocicleta("Yamaha", "MT-07", 2021, "Deportiva")  # Instancia de la clase Motocicleta

# Uso de los métodos
print("Descripción del coche:")
mostrar_descripcion(coche1)  # Muestra la descripción del coche

print("\nDescripción de la motocicleta:")
mostrar_descripcion(motocicleta1)  # Muestra la descripción de la motocicleta

# Acceso y modificación del atributo privado
print(f"\nNúmero de puertas del coche: {coche1.get_puertas()}")
coche1.set_puertas(5)  # Cambiamos el número de puertas
print(f"Número de puertas del coche después de modificar: {coche1.get_puertas()}")

