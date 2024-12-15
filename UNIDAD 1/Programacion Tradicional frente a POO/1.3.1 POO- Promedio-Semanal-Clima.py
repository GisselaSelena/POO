class ClimaDiario:
    """Clase que representa la información diaria del clima.

    Esta clase encapsula las temperaturas diarias y proporciona métodos
    para ingresar datos y calcular el promedio. Utiliza el concepto de
    encapsulamiento para proteger los datos.
    """

    def __init__(self):
        """Inicializa una nueva instancia de ClimaDiario con una lista vacía de temperaturas."""
        self.temperaturas = []  # Lista para almacenar las temperaturas diarias

    def ingresar_temperatura(self):
        """Método para ingresar la temperatura del día.

        Solicita al usuario que ingrese una temperatura y la almacena en la lista.
        Este método incluye manejo de errores para asegurar que la entrada sea válida.
        """
        while True:  # Bucle para asegurar que se ingrese un valor válido
            try:
                # Solicitar al usuario que ingrese la temperatura
                temp = float(input("Ingrese la temperatura del día: "))
                self.temperaturas.append(temp)  # Agregar la temperatura a la lista
                break  # Salir del bucle si la entrada es válida
            except ValueError:
                # Manejo de errores si la entrada no es un número
                print("Por favor, ingrese un número válido.")

    def calcular_promedio(self):
        """Método para calcular el promedio de las temperaturas.

        Retorna el promedio de las temperaturas almacenadas.
        Si no hay temperaturas, retorna 0.
        """
        if not self.temperaturas:  # Verificar si la lista está vacía
            return 0  # Retornar 0 si no hay temperaturas
        return sum(self.temperaturas) / len(self.temperaturas)  # Calcular y retornar el promedio


def main():
    """Función principal que coordina la entrada de datos y el cálculo del promedio."""
    print("Bienvenido al programa de promedio semanal del clima.")
    clima = ClimaDiario()  # Crear una instancia de la clase ClimaDiario

    for dia in range(7):  # Iterar sobre 7 días de la semana
        print(f"Ingreso de temperatura para el día {dia + 1}:")
        clima.ingresar_temperatura()  # Llamar al método para ingresar la temperatura

    promedio = clima.calcular_promedio()  # Calcular el promedio de las temperaturas
    # Mostrar el resultado al usuario
    print(f"El promedio semanal de las temperaturas es: {promedio:.2f}°C")


if __name__ == "__main__":
    main()  # Ejecutar la función principal