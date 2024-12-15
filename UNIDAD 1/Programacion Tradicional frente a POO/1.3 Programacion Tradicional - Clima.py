def ingresar_temperaturas():
    """Función para ingresar las temperaturas diarias de la semana.

    Retorna una lista con las temperaturas ingresadas.
    """
    temperaturas = []  # Lista para almacenar las temperaturas
    for dia in range(7):  # Iterar sobre 7 días de la semana
        while True:  # Bucle para asegurar que se ingrese un valor válido
            try:
                # Solicitar al usuario que ingrese la temperatura
                temp = float(input(f"Ingrese la temperatura del día {dia + 1}: "))
                temperaturas.append(temp)  # Agregar la temperatura a la lista
                break  # Salir del bucle si la entrada es válida
            except ValueError:
                # Manejo de errores si la entrada no es un número
                print("Por favor, ingrese un número válido.")
    return temperaturas  # Retornar la lista de temperaturas


def calcular_promedio(temperaturas):
    """Función para calcular el promedio de las temperaturas.

    Parámetros:
    temperaturas (list): Lista de temperaturas diarias.

    Retorna el promedio de las temperaturas.
    """
    return sum(temperaturas) / len(temperaturas)  # Calcular y retornar el promedio


def main():
    """Función principal que coordina la entrada de datos y el cálculo del promedio."""
    print("Bienvenido al programa de promedio semanal del clima.")
    temperaturas = ingresar_temperaturas()  # Llamar a la función para ingresar temperaturas
    promedio = calcular_promedio(temperaturas)  # Calcular el promedio
    # Mostrar el resultado al usuario
    print(f"El promedio semanal de las temperaturas es: {promedio:.2f}°C")


if __name__ == "__main__":
    main()  # Ejecutar la función principal