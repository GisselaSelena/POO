import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import uuid


class GestorTareas:
    """
    Aplicación GUI para gestionar tareas.
    Permite al usuario agregar, visualizar y eliminar tareas.
    """

    def __init__(self, root):
        """
        Inicializa la aplicación GUI.

        Args:
            root: La ventana principal de Tkinter.
        """
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("700x500")
        self.root.resizable(True, True)

        # Configuración del estilo
        self.style = ttk.Style()
        self.style.theme_use("clam")  # Usar un tema moderno

        # Variables para almacenar la entrada del usuario
        self.titulo_var = tk.StringVar()
        self.descripcion_var = tk.StringVar()

        # Crear y configurar el marco principal
        self.crear_widgets()

        # Lista para almacenar las tareas (para futuras funcionalidades)
        self.tareas = []

    def crear_widgets(self):
        """Crea y configura todos los widgets de la interfaz."""

        # Marco para los formularios
        form_frame = ttk.LabelFrame(self.root, text="Nueva Tarea")
        form_frame.pack(fill="x", expand="no", padx=20, pady=10)

        # Etiqueta y campo para el título de la tarea
        ttk.Label(form_frame, text="Título:").grid(row=0, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(form_frame, textvariable=self.titulo_var, width=50).grid(row=0, column=1, padx=5, pady=5)

        # Etiqueta y campo para la descripción de la tarea
        ttk.Label(form_frame, text="Descripción:").grid(row=1, column=0, padx=5, pady=5, sticky=tk.W)
        ttk.Entry(form_frame, textvariable=self.descripcion_var, width=50).grid(row=1, column=1, padx=5, pady=5)

        # Marco para los botones
        button_frame = ttk.Frame(form_frame)
        button_frame.grid(row=2, column=0, columnspan=2, pady=10)

        # Botón para agregar tarea
        ttk.Button(
            button_frame,
            text="Agregar Tarea",
            command=self.agregar_tarea
        ).pack(side=tk.LEFT, padx=5)

        # Botón para limpiar campos
        ttk.Button(
            button_frame,
            text="Limpiar Campos",
            command=self.limpiar_campos
        ).pack(side=tk.LEFT, padx=5)

        # Marco para la tabla de tareas
        table_frame = ttk.LabelFrame(self.root, text="Mis Tareas")
        table_frame.pack(fill="both", expand=True, padx=20, pady=10)

        # Crear tabla de tareas (Treeview)
        self.tabla_tareas = ttk.Treeview(
            table_frame,
            columns=("id", "titulo", "descripcion"),
            show="headings"
        )

        # Configurar las columnas
        self.tabla_tareas.heading("id", text="ID")
        self.tabla_tareas.heading("titulo", text="Título")
        self.tabla_tareas.heading("descripcion", text="Descripción")

        # Ajustar el ancho de las columnas
        self.tabla_tareas.column("id", width=50)
        self.tabla_tareas.column("titulo", width=200)
        self.tabla_tareas.column("descripcion", width=400)

        # Agregar scrollbar vertical
        scrollbar = ttk.Scrollbar(table_frame, orient=tk.VERTICAL, command=self.tabla_tareas.yview)
        self.tabla_tareas.configure(yscroll=scrollbar.set)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        self.tabla_tareas.pack(fill="both", expand=True)

        # Marco para los botones de gestión de tareas
        manage_frame = ttk.Frame(self.root)
        manage_frame.pack(fill="x", padx=20, pady=10)

        # Botón para eliminar tarea seleccionada
        ttk.Button(
            manage_frame,
            text="Eliminar Tarea Seleccionada",
            command=self.eliminar_tarea
        ).pack(side=tk.LEFT, padx=5)

    def agregar_tarea(self):
        """Agrega una nueva tarea a la tabla."""
        titulo = self.titulo_var.get().strip()
        descripcion = self.descripcion_var.get().strip()

        # Validar que el título no esté vacío
        if not titulo:
            messagebox.showerror("Error", "El título de la tarea no puede estar vacío.")
            return

        # Generar un ID único para la tarea
        id_tarea = str(uuid.uuid4())[:8]

        # Insertar la tarea en la tabla
        self.tabla_tareas.insert("", tk.END, values=(id_tarea, titulo, descripcion))

        # Guardar la tarea en la lista (para futuras funcionalidades)
        self.tareas.append({
            "id": id_tarea,
            "titulo": titulo,
            "descripcion": descripcion
        })

        # Limpiar los campos de entrada
        self.limpiar_campos()
        messagebox.showinfo("Éxito", "Tarea agregada correctamente.")

    def limpiar_campos(self):
        """Limpia los campos de entrada."""
        self.titulo_var.set("")
        self.descripcion_var.set("")

    def eliminar_tarea(self):
        """Elimina la tarea seleccionada de la tabla."""
        # Obtener el ítem seleccionado
        seleccionado = self.tabla_tareas.selection()

        if not seleccionado:
            messagebox.showwarning("Advertencia", "Por favor, selecciona una tarea para eliminar.")
            return

        # Confirmar la eliminación
        if messagebox.askyesno("Confirmar", "¿Estás seguro de eliminar esta tarea?"):
            # Eliminar de la tabla
            for item in seleccionado:
                item_id = self.tabla_tareas.item(item, "values")[0]
                self.tabla_tareas.delete(item)

                # Eliminar de la lista de tareas (búsqueda por ID)
                self.tareas = [tarea for tarea in self.tareas if tarea["id"] != item_id]

            messagebox.showinfo("Éxito", "Tarea(s) eliminada(s) correctamente.")


def main():
    """Función principal para iniciar la aplicación."""
    root = tk.Tk()
    app = GestorTareas(root)
    root.mainloop()


if __name__ == "__main__":
    main()