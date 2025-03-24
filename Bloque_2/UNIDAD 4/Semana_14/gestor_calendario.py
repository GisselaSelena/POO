import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry  # Módulo para DatePicker
import datetime
import json  # Módulo para trabajar con archivos JSON


class AplicacionGestionEventos:
    """
    Aplicación para gestionar eventos o tareas programadas utilizando Tkinter.
    Permite añadir, visualizar y eliminar eventos.
    """

    def __init__(self, root):
        """
        Inicializa la aplicación.

        Args:
            root: La ventana principal de Tkinter.
        """
        self.root = root
        self.root.title("Gestor de Eventos")
        self.root.geometry("800x500")
        self.root.resizable(True, True)

        # Configuración de estilo
        self.style = ttk.Style()
        self.style.configure("Treeview", font=('Arial', 10))
        self.style.configure("Treeview.Heading", font=('Arial', 10, 'bold'))

        # Creación de frames para organizar la interfaz
        self.crear_frames()

        # Creación de los componentes de la interfaz
        self.crear_componentes_visualizacion()
        self.crear_componentes_entrada()
        self.crear_componentes_acciones()

        # Inicializar con la fecha y hora actuales
        self.inicializar_valores_predeterminados()

    def crear_frames(self):
        """Crea los frames para organizar la interfaz."""
        # Frame para la lista de eventos
        self.frame_lista = ttk.LabelFrame(self.root, text="Lista de Eventos")
        self.frame_lista.pack(fill="both", expand=True, padx=10, pady=10)

        # Frame para la entrada de datos
        self.frame_entrada = ttk.LabelFrame(self.root, text="Nuevo Evento")
        self.frame_entrada.pack(fill="both", expand=False, padx=10, pady=10)

        # Frame para los botones de acción
        self.frame_acciones = ttk.Frame(self.root)
        self.frame_acciones.pack(fill="x", expand=False, padx=10, pady=10)

    def crear_componentes_visualizacion(self):
        """Crea los componentes para visualizar los eventos."""
        # Treeview para mostrar la lista de eventos
        self.tree = ttk.Treeview(self.frame_lista, columns=("ID", "Fecha", "Hora", "Descripción"), show="headings")

        # Configurar columnas
        self.tree.heading("ID", text="ID")
        self.tree.heading("Fecha", text="Fecha")
        self.tree.heading("Hora", text="Hora")
        self.tree.heading("Descripción", text="Descripción")

        # Configurar anchos de columnas
        self.tree.column("ID", width=50, anchor="center")
        self.tree.column("Fecha", width=100, anchor="center")
        self.tree.column("Hora", width=100, anchor="center")
        self.tree.column("Descripción", width=400)

        # Añadir barras de desplazamiento
        scrollbar_y = ttk.Scrollbar(self.frame_lista, orient="vertical", command=self.tree.yview)
        scrollbar_x = ttk.Scrollbar(self.frame_lista, orient="horizontal", command=self.tree.xview)
        self.tree.configure(yscrollcommand=scrollbar_y.set, xscrollcommand=scrollbar_x.set)

        # Empaquetar componentes
        scrollbar_y.pack(side="right", fill="y")
        scrollbar_x.pack(side="bottom", fill="x")
        self.tree.pack(fill="both", expand=True)

    def crear_componentes_entrada(self):
        """Crea los componentes para la entrada de datos de nuevos eventos."""
        # Crear un grid dentro del frame de entrada
        for i in range(3):
            self.frame_entrada.columnconfigure(i, weight=1)

        # Etiquetas y campos para fecha
        self.lbl_fecha = ttk.Label(self.frame_entrada, text="Fecha:")
        self.lbl_fecha.grid(row=0, column=0, padx=5, pady=5, sticky="e")

        # DatePicker para selección de fecha
        self.entry_fecha = DateEntry(self.frame_entrada, width=15, background='darkblue',
                                     foreground='white', borderwidth=2, date_pattern='dd/mm/yyyy')
        self.entry_fecha.grid(row=0, column=1, padx=5, pady=5, sticky="w")

        # Etiquetas y campos para hora
        self.lbl_hora = ttk.Label(self.frame_entrada, text="Hora:")
        self.lbl_hora.grid(row=0, column=2, padx=5, pady=5, sticky="e")

        # Frame para hora (horas y minutos)
        self.frame_hora = ttk.Frame(self.frame_entrada)
        self.frame_hora.grid(row=0, column=3, padx=5, pady=5, sticky="w")

        # Spinbox para horas
        self.spin_horas = ttk.Spinbox(self.frame_hora, from_=0, to=23, width=3, format="%02.0f")
        self.spin_horas.pack(side="left")

        ttk.Label(self.frame_hora, text=":").pack(side="left")

        # Spinbox para minutos
        self.spin_minutos = ttk.Spinbox(self.frame_hora, from_=0, to=59, width=3, format="%02.0f")
        self.spin_minutos.pack(side="left")

        # Etiquetas y campos para descripción
        self.lbl_descripcion = ttk.Label(self.frame_entrada, text="Descripción:")
        self.lbl_descripcion.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.entry_descripcion = ttk.Entry(self.frame_entrada, width=60)
        self.entry_descripcion.grid(row=1, column=1, columnspan=3, padx=5, pady=5, sticky="we")

    def crear_componentes_acciones(self):
        """Crea los botones de acción."""
        # Botón para agregar evento
        self.btn_agregar = ttk.Button(self.frame_acciones, text="Agregar Evento", command=self.agregar_evento)
        self.btn_agregar.pack(side="left", padx=5, pady=5)

        # Botón para eliminar evento seleccionado
        self.btn_eliminar = ttk.Button(self.frame_acciones, text="Eliminar Evento Seleccionado",
                                       command=self.eliminar_evento)
        self.btn_eliminar.pack(side="left", padx=5, pady=5)

        # Botón para salir
        self.btn_salir = ttk.Button(self.frame_acciones, text="Salir", command=self.root.destroy)
        self.btn_salir.pack(side="right", padx=5, pady=5)

    def inicializar_valores_predeterminados(self):
        """Inicializa los campos con valores predeterminados."""
        # Establecer hora actual
        now = datetime.datetime.now()
        self.spin_horas.set(f"{now.hour:02d}")
        self.spin_minutos.set(f"{now.minute:02d}")

        # Limpiar descripción
        self.entry_descripcion.delete(0, tk.END)

        # Contador para los IDs de los eventos
        self.contador_id = 1

    def agregar_evento(self):
        """Agrega un nuevo evento a la lista y lo guarda en un archivo JSON."""
        # Obtener valores de los campos
        fecha = self.entry_fecha.get_date().strftime("%d/%m/%Y")
        hora = f"{self.spin_horas.get()}:{self.spin_minutos.get()}"
        descripcion = self.entry_descripcion.get().strip()

        # Validar que la descripción no esté vacía
        if not descripcion:
            messagebox.showerror("Error", "La descripción no puede estar vacía.")
            return

        # Insertar evento en el TreeView
        self.tree.insert("", "end", values=(self.contador_id, fecha, hora, descripcion))

        # Guardar evento en un archivo JSON
        self.guardar_evento_json(self.contador_id, fecha, hora, descripcion)

        # Incrementar contador de ID
        self.contador_id += 1

        # Limpiar campo de descripción
        self.entry_descripcion.delete(0, tk.END)

        # Mostrar mensaje de confirmación
        messagebox.showinfo("Éxito", "Evento agregado correctamente.")

    def guardar_evento_json(self, id_evento, fecha, hora, descripcion):
        """Guarda el evento en un archivo JSON."""
        evento = {
            "id": id_evento,
            "fecha": fecha,
            "hora": hora,
            "descripcion": descripcion
        }

        # Intentar abrir el archivo JSON existente y cargar los eventos
        try:
            with open("eventos.json", "r") as archivo:
                eventos = json.load(archivo)
        except (FileNotFoundError, json.JSONDecodeError):
            eventos = []  # Si el archivo no existe o está vacío, inicializar lista vacía

        # Añadir el nuevo evento a la lista
        eventos.append(evento)

        # Guardar la lista actualizada de eventos en el archivo JSON
        with open("eventos.json", "w") as archivo:
            json.dump(eventos, archivo, indent=4)

    def eliminar_evento(self):
        """Elimina el evento seleccionado de la lista."""
        # Obtener ítem seleccionado
        seleccionado = self.tree.selection()

        if not seleccionado:
            messagebox.showerror("Error", "No hay ningún evento seleccionado.")
            return

        # Solicitar confirmación
        if messagebox.askyesno("Confirmar eliminación", "¿Está seguro que desea eliminar el evento seleccionado?"):
            # Eliminar evento seleccionado
            for item in seleccionado:
                self.tree.delete(item)

            messagebox.showinfo("Éxito", "Evento eliminado correctamente.")


def main():
    """Función principal que inicia la aplicación."""
    root = tk.Tk()
    app = AplicacionGestionEventos(root)
    root.mainloop()


if __name__ == "__main__":
    main()