# Clase base que representa un vehículo (ABSTRACCIÓN)
class Vehiculo:
    def __init__(self, marca, modelo, año, precio_dia):
        self.marca = marca
        self.modelo = modelo
        self.año = año
        self.precio_dia = precio_dia

    def mostrar_info(self):
        print(f"Marca: {self.marca}, Modelo: {self.modelo}, Año: {self.año}, Precio por día: {self.precio_dia}")

    def calcular_precio_alquiler(self, dias):
        return self.precio_dia * dias


# Clase que representa un coche, hereda de Vehiculo (HERENCIA)
class Coche(Vehiculo):
    def __init__(self, marca, modelo, año, precio_dia, puertas):
        super().__init__(marca, modelo, año, precio_dia)  # Llamada al constructor de la clase base
        self.__puertas = puertas  # Atributo privado (ENCAPSULACIÓN)

    def mostrar_info(self):
        super().mostrar_info()  # Llama al método de la clase base
        print(f"·Puertas: {self.__puertas}")

    def calcular_precio_alquiler(self, dias):
        return super().calcular_precio_alquiler(dias) * 1.1  # Aplica un 10% extra para coches


# Clase que representa una moto, hereda de Vehiculo (HERENCIA)
class Moto(Vehiculo):
    def __init__(self, marca, modelo, año, precio_dia, tipo):
        super().__init__(marca, modelo, año, precio_dia)  # Llamada al constructor de la clase base
        self.__tipo = tipo  # Atributo privado (ENCAPSULACIÓN)

    def mostrar_info(self):
        super().mostrar_info()  # Llama al método de la clase base
        print(f"·Tipo: {self.__tipo}")

    def calcular_precio_alquiler(self, dias):
        return super().calcular_precio_alquiler(dias) * 0.9  # Aplica un 10% de descuento para motos


# Función para mostrar información de todos los vehículos
def mostrar_vehiculos(vehiculos):
    for vehiculo in vehiculos:
        vehiculo.mostrar_info()  # POLIMORFISMO: se llama al método de cada objeto


# Creación de instancias de Coche y Moto
coche1 = Coche("Toyota", "Corolla", 2020, 50, 4)
moto1 = Moto("Yamaha", "MT-07", 2021, 30, "Deportiva")

# Lista de vehículos
vehiculos = [coche1, moto1]

# Mostrar información de los vehículos
mostrar_vehiculos(vehiculos)

# Calcular y mostrar el precio de alquiler
dias = 5
for vehiculo in vehiculos:
    precio = vehiculo.calcular_precio_alquiler(dias)
    print(f"Precio de alquiler por {dias} días: {precio}")