class Conexion:
    def __init__(self, direccion):
        """
        Constructor que inicializa la conexión a una dirección específica.

        :param direccion: Dirección de la conexión (por ejemplo, una URL o IP).
        """
        self.direccion = direccion
        self.conectado = True  # Simula que la conexión está abierta
        print(f"Conexión establecida a {self.direccion}.")

    def enviar_datos(self, datos):
        """
        Método para simular el envío de datos a través de la conexión.

        :param datos: Datos que se desean enviar.
        """
        if self.conectado:
            print(f"Enviando datos a {self.direccion}: {datos}")
        else:
            print("No se puede enviar datos, la conexión está cerrada.")

    def cerrar(self):
        """
        Método para cerrar la conexión.
        """
        if self.conectado:
            self.conectado = False
            print(f"Conexión a {self.direccion} cerrada.")
        else:
            print("La conexión ya está cerrada.")

    def __del__(self):
        """
        Destructor que cierra la conexión si está abierta.

        Este método se llama automáticamente cuando el objeto es destruido,
        ya sea porque se sale del alcance o se llama a 'del'.
        """
        if self.conectado:
            self.cerrar()  # Cierra la conexión
            print(f"Destructor: Conexión a {self.direccion} liberada.")


# Crear y eliminar una instancia de Conexion para observar el comportamiento
mi_conexion = Conexion("192.168.1.1")
mi_conexion.enviar_datos("Hola, servidor!")
del mi_conexion  # Esto debería desencadenar el destructor