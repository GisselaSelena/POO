import tkinter as tk
from tkinter import ttk
from tkinter import messagebox


class TaskManagerApp:
    """
    Aplicación para gestionar una lista de tareas utilizando Tkinter.
    Permite añadir, marcar como completadas y eliminar tareas.
    """

    def __init__(self, root):
        """
        Inicializa la aplicación con sus componentes GUI.

        Args:
            root: La ventana principal de Tkinter
        """
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("500x400")
        self.root.resizable(True, True)

        # Lista para almacenar las tareas (tuplas de (tarea, completada))
        self.tasks = []

        # Configuración de la interfaz
        self._setup_ui()

    def _setup_ui(self):
        """Configura todos los elementos de la interfaz de usuario."""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Área de entrada de tareas
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        # Etiqueta para el campo de entrada
        ttk.Label(input_frame, text="Nueva Tarea:").pack(side=tk.LEFT, padx=(0, 5))

        # Campo de entrada para nuevas tareas
        self.task_entry = ttk.Entry(input_frame, width=40)
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.task_entry.focus()  # Poner el foco en el campo de entrada

        # Vincular la tecla Enter al campo de entrada para añadir tareas
        self.task_entry.bind("<Return>", self.add_task)

        # Botón para añadir tareas
        ttk.Button(input_frame, text="Añadir Tarea", command=self.add_task).pack(side=tk.LEFT)

        # Frame para la lista de tareas y su barra de desplazamiento
        list_frame = ttk.Frame(main_frame)
        list_frame.pack(fill=tk.BOTH, expand=True)

        # Barra de desplazamiento para la lista de tareas
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Lista de tareas (Treeview para mejor visualización)
        columns = ("tarea", "estado")
        self.task_list = ttk.Treeview(list_frame, columns=columns, show="headings",
                                      yscrollcommand=scrollbar.set, selectmode="browse")

        # Configurar las columnas
        self.task_list.heading("tarea", text="Tarea")
        self.task_list.heading("estado", text="Estado")
        self.task_list.column("tarea", width=350)
        self.task_list.column("estado", width=100, anchor=tk.CENTER)

        self.task_list.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.config(command=self.task_list.yview)

        # Vinculación de doble clic para marcar/desmarcar tarea como completada
        self.task_list.bind("<Double-1>", self.toggle_task_status)

        # Frame para botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=(10, 0))

        # Botones para marcar como completada y eliminar tarea
        ttk.Button(button_frame, text="Marcar como Completada",
                   command=self.mark_task_completed).pack(side=tk.LEFT, padx=(0, 5))
        ttk.Button(button_frame, text="Eliminar Tarea",
                   command=self.delete_task).pack(side=tk.LEFT)

    def add_task(self, event=None):
        """
        Añade una nueva tarea a la lista.

        Args:
            event: Evento de teclado (opcional, para vinculación con Enter)
        """
        task_text = self.task_entry.get().strip()

        if task_text:  # Verificar que la tarea no esté vacía
            # Añadir a la lista interna de tareas
            self.tasks.append((task_text, False))  # (tarea, completada=False)

            # Añadir a la vista de árbol
            self.task_list.insert("", tk.END, values=(task_text, "Pendiente"))

            # Limpiar el campo de entrada
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Entrada vacía", "Por favor ingrese una tarea.")

        # Devolver el foco al campo de entrada
        self.task_entry.focus()

    def mark_task_completed(self):
        """Marca la tarea seleccionada como completada."""
        # Obtener el ítem seleccionado
        selected_item = self.task_list.selection()

        if selected_item:  # Si hay un ítem seleccionado
            item_id = selected_item[0]
            item_index = self.task_list.index(item_id)

            # Actualizar el estado en la lista interna
            task_text, is_completed = self.tasks[item_index]

            if not is_completed:  # Solo si no está completada
                self.tasks[item_index] = (task_text, True)

                # Actualizar la visualización en la lista
                self.task_list.item(item_id, values=(task_text, "Completada"))

                # Opcional: Añadir un estilo visual para tareas completadas (por ejemplo, texto tachado)
                # Esto requeriría configuración adicional de etiquetas
        else:
            messagebox.showinfo("Selección", "Por favor seleccione una tarea.")

    def toggle_task_status(self, event=None):
        """
        Alterna el estado de una tarea entre completada y pendiente con doble clic.

        Args:
            event: Evento de doble clic
        """
        # Obtener el ítem seleccionado
        selected_item = self.task_list.selection()

        if selected_item:  # Si hay un ítem seleccionado
            item_id = selected_item[0]
            item_index = self.task_list.index(item_id)

            # Obtener el estado actual y cambiarlo
            task_text, is_completed = self.tasks[item_index]
            new_status = not is_completed

            # Actualizar en la lista interna
            self.tasks[item_index] = (task_text, new_status)

            # Actualizar la visualización en la lista
            status_text = "Completada" if new_status else "Pendiente"
            self.task_list.item(item_id, values=(task_text, status_text))

    def delete_task(self):
        """Elimina la tarea seleccionada de la lista."""
        # Obtener el ítem seleccionado
        selected_item = self.task_list.selection()

        if selected_item:  # Si hay un ítem seleccionado
            item_id = selected_item[0]
            item_index = self.task_list.index(item_id)

            # Eliminar de la lista interna
            del self.tasks[item_index]

            # Eliminar de la vista de árbol
            self.task_list.delete(item_id)
        else:
            messagebox.showinfo("Selección", "Por favor seleccione una tarea.")


# Punto de entrada de la aplicación
if __name__ == "__main__":
    root = tk.Tk()
    app = TaskManagerApp(root)
    root.mainloop()