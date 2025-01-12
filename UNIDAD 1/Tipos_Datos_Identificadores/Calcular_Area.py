# Programa para calcular el área de diferentes figuras geométricas.
# El usuario puede elegir entre círculo, cuadrado o rectángulo.
# Se utilizan funciones para calcular el área de cada figura y se
# permite al usuario realizar múltiples cálculos hasta que decida salir.

import math  # Importamos la biblioteca math para utilizar la constante pi


def calcular_area_circulo(radio: float) -> float:
    """Calcula el área de un círculo dado su radio."""
    return math.pi * (radio ** 2)  # Fórmula del área: π * r^2


def calcular_area_cuadrado(lado: float) -> float:
    """Calcula el área de un cuadrado dado el tamaño de su lado."""
    return lado ** 2  # Fórmula del área: lado^2


def calcular_area_rectangulo(base: float, altura: float) -> float:
    """Calcula el área de un rectángulo dado su base y altura."""
    return base * altura  # Fórmula del área: base * altura


def main():
    # Variable para controlar el bucle que permite al usuario realizar múltiples cálculos
    continuar = True

    while continuar:
        # Menú de opciones para que el usuario seleccione la figura
        print("Seleccione la figura para calcular el área:")
        print("1. Círculo")
        print("2. Cuadrado")
        print("3. Rectángulo")
        print("4. Salir")

        # Solicitar la opción del usuario
        opcion = input("Ingrese el número de la opción deseada: ")

        if opcion == '1':
            # Calcular área de un círculo
            radio = float(input("Ingrese el radio del círculo: "))  # Solicitar el radio
            area = calcular_area_circulo(radio)  # Llamar a la función para calcular el área
            print(f"El área del círculo es: {area:.2f}")  # Mostrar el resultado

        elif opcion == '2':
            # Calcular área de un cuadrado
            lado = float(input("Ingrese el lado del cuadrado: "))  # Solicitar el lado
            area = calcular_area_cuadrado(lado)  # Llamar a la función para calcular el área
            print(f"El área del cuadrado es: {area:.2f}")  # Mostrar el resultado

        elif opcion == '3':
            # Calcular área de un rectángulo
            base = float(input("Ingrese la base del rectángulo: "))  # Solicitar la base
            altura = float(input("Ingrese la altura del rectángulo: "))  # Solicitar la altura
            area = calcular_area_rectangulo(base, altura)  # Llamar a la función para calcular el área
            print(f"El área del rectángulo es: {area:.2f}")  # Mostrar el resultado

        elif opcion == '4':
            # Salir del programa
            continuar = False  # Cambiar la variable para salir del bucle
            print("Saliendo del programa. ¡Hasta luego!")

        else:
            # Manejar opción no válida
            print("Opción no válida. Por favor, intente de nuevo.")


# Verificar si el script se está ejecutando directamente
if __name__ == "__main__":
    main()  # Llamar a la función principal para iniciar el programa