import os
import sys
from pathlib import Path

"""
Dashboard para la Gestión de Proyectos de Programación Orientada a Objetos (POO).
Este script permite visualizar y acceder a diferentes archivos Python organizados
en una estructura de unidades y carpetas.

"""

def mostrar_codigo(ruta_script):
    """
    Muestra el contenido de un archivo Python manejando diferentes codificaciones.

    Esta función intenta leer el archivo con diferentes codificaciones (utf-8, latin-1, cp1252)
    para asegurar la compatibilidad con diferentes formatos de texto.

    Args:
        ruta_script (str): Ruta al archivo que se quiere mostrar.

    Returns:
        None: La función imprime el contenido directamente en la consola.
    """
    # Lista de codificaciones a intentar para la lectura del archivo
    encodings = ['utf-8', 'latin-1', 'cp1252']

    # Intenta cada codificación hasta encontrar una que funcione
    for encoding in encodings:
        try:
            # Convierte la ruta a objeto Path para un mejor manejo
            ruta = Path(ruta_script)
            # Lee el contenido del archivo como bytes
            contenido = ruta.read_bytes()
            # Intenta decodificar el contenido con la codificación actual
            texto = contenido.decode(encoding)

            # Muestra el contenido del archivo con formato
            print(f"\n{'=' * 50}")
            print(f"Archivo: {ruta.parent.name}/{ruta.name}")
            print('=' * 50 + "\n")
            print(texto)
            print(f"\n{'=' * 50}\n")
            return

        except UnicodeDecodeError:
            continue  # Si falla la decodificación, intenta con la siguiente codificación
        except FileNotFoundError:
            print(f"Error: No se encontró el archivo {ruta_script}")
            return
        except Exception as e:
            print(f"Error al leer el archivo: {str(e)}")
            return

    # Si ninguna codificación funcionó, informa al usuario
    print(f"Error: No se pudo leer el archivo con ninguna codificación soportada.")


def limpiar_pantalla():
    """
    Limpia la pantalla de la consola.

    Esta función detecta el sistema operativo y utiliza el comando apropiado
    para limpiar la pantalla (cls para Windows, clear para Unix/Linux/MacOS).
    """
    os.system('cls' if os.name == 'nt' else 'clear')


def mostrar_menu():
    """
    Muestra el menú principal del dashboard y maneja la interacción con el usuario.

    Esta función es el núcleo del dashboard, mostrando las opciones disponibles
    y procesando la selección del usuario. Organiza los archivos por unidades
    y subcarpetas para una mejor navegación.

    Returns:
        None: La función maneja la interacción directamente.
    """
    # Diccionario que define la estructura del proyecto
    # Cada entrada contiene la ruta, nombre del archivo y carpeta contenedora
    # Las claves son números que representan las opciones del menú
    opciones = {
        # UNIDAD 1 - Fundamentos básicos y ejemplos iniciales
        '1': {
            'ruta': 'UNIDAD 1/EjemplosMundoReal_POO/Reserva_Biblioteca.py',
            'nombre': 'Reserva_Biblioteca.py',
            'carpeta': 'EjemplosMundoReal_POO'
        },
        '2': {
            'ruta': 'UNIDAD 1/Programacion Tradicional frente a POO/1.3.1 POO- Promedio-Semanal-Clima.py',
            'nombre': '1.3.1 POO- Promedio-Semanal-Clima.py',
            'carpeta': 'Programacion Tradicional frente a POO'
        },
        '3': {
            'ruta': 'UNIDAD 1/Programacion Tradicional frente a POO/1.3 Programacion Tradicional - Clima.py',
            'nombre': '1.3 Programacion Tradicional - Clima.py',
            'carpeta': 'Programacion Tradicional frente a POO'
        },
        '4': {
            'ruta': 'UNIDAD 1/Tipos_Datos_Identificadores/Calcular_Area.py',
            'nombre': 'Calcular_Area.py',
            'carpeta': 'Tipos_Datos_Identificadores'
        },
        '5': {
            'ruta': 'UNIDAD 1/1.2 Tecnicas de Programacion.py',
            'nombre': '1.2 Tecnicas de Programacion.py',
            'carpeta': 'UNIDAD 1'
        },

        # UNIDAD 2 - Conceptos avanzados de POO
        '6': {
            'ruta': 'UNIDAD 2/2.1 Constructores y Destructores.py',
            'nombre': '2.1 Constructores y Destructores.py',
            'carpeta': 'UNIDAD 2'
        },
        '7': {
            'ruta': 'UNIDAD 2/Clases, objetos, herencia, encapsulamiento y polimorfismo.py',
            'nombre': 'Clases, objetos, herencia, encapsulamiento y polimorfismo.py',
            'carpeta': 'UNIDAD 2'
        }
    }

    # Bucle principal del menú
    while True:
        limpiar_pantalla()  # Limpia la pantalla antes de mostrar el menú
        # Encabezado del menú
        print("\n🔷 DASHBOARD - PROGRAMACIÓN ORIENTADA A OBJETOS 🔷")

        # Muestra opciones de UNIDAD 1
        print("\nUNIDAD 1:")
        for i in range(1, 6):
            opt = opciones[str(i)]
            print(f"  {i} - [{opt['carpeta']}] {opt['nombre']}")

        # Muestra opciones de UNIDAD 2
        print("\nUNIDAD 2:")
        for i in range(6, 8):
            opt = opciones[str(i)]
            print(f"  {i} - [{opt['carpeta']}] {opt['nombre']}")

        # Opción para salir del programa
        print("\n  0 - Salir")
        print("\n" + "=" * 50)

        # Procesa la entrada del usuario
        opcion = input("\nSeleccione una opción (0-7): ").strip()

        if opcion == '0':
            # Mensaje de despedida y salida del programa
            limpiar_pantalla()
            print("\n¡Gracias por usar el Dashboard POO!")
            print("Desarrollado para gestionar proyectos de Programación Orientada a Objetos.")
            sys.exit(0)

        elif opcion in opciones:
            limpiar_pantalla()  # Limpia la pantalla antes de mostrar el archivo
            # Construye la ruta completa al archivo seleccionado
            ruta_base = Path(__file__).parent
            ruta_script = ruta_base / opciones[opcion]['ruta']
            # Muestra el contenido del archivo seleccionado
            mostrar_codigo(str(ruta_script))
            input("\nPresione Enter para volver al menú principal...")
        else:
            # Manejo de opciones inválidas
            print("\n⚠️ Opción no válida. Por favor, intente de nuevo.")
            input("\nPresione Enter para continuar...")


# Punto de entrada del programa
if __name__ == "__main__":
    mostrar_menu()  # Llama a la función que muestra el menú principal