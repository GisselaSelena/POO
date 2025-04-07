import tkinter as tk
from tkinter import ttk, messagebox
import os


class TodoApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Gestor de Tareas")
        self.root.geometry("500x450")
        self.root.resizable(True, True)

        # Configuración del tema y estilo
        self.configure_styles()

        # Variables
        self.tasks = []
        self.completed_tasks = []

        # Crear widgets
        self.create_widgets()

        # Configurar atajos de teclado
        self.setup_keyboard_shortcuts()

    def configure_styles(self):
        """Configurar estilos para los widgets"""
        style = ttk.Style()

        # Configurar colores según el sistema operativo
        if os.name == 'nt':  # Windows
            style.theme_use('vista')
        else:
            style.theme_use('clam')

        # Estilo para tareas pendientes y completadas
        style.configure("Pending.TLabel", foreground="black")
        style.configure("Completed.TLabel", foreground="gray", font=("TkDefaultFont", 9, "overstrike"))

        # Estilos de botones
        style.configure("Add.TButton", background="#4CAF50")
        style.configure("Complete.TButton", background="#2196F3")
        style.configure("Delete.TButton", background="#F44336")

        # En algunos sistemas, el cambio de color de texto en botones ttk requiere mapeo
        style.map("Add.TButton", foreground=[('!disabled', 'white')])
        style.map("Complete.TButton", foreground=[('!disabled', 'white')])
        style.map("Delete.TButton", foreground=[('!disabled', 'white')])

    def create_widgets(self):
        """Crear todos los widgets de la interfaz"""
        # Frame principal
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # Título
        title_label = ttk.Label(main_frame, text="Gestor de Tareas", font=("TkDefaultFont", 16, "bold"))
        title_label.pack(pady=10)

        # Frame para entrada y botón de añadir
        input_frame = ttk.Frame(main_frame)
        input_frame.pack(fill=tk.X, pady=5)

        # Etiqueta de entrada
        input_label = ttk.Label(input_frame, text="Nueva tarea:")
        input_label.pack(side=tk.LEFT, padx=(0, 5))

        # Campo de entrada
        self.task_entry = ttk.Entry(input_frame, width=40)
        self.task_entry.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=(0, 5))
        self.task_entry.focus()

        # Botón para añadir tarea
        add_button = ttk.Button(input_frame, text="Añadir", command=self.add_task, style="Add.TButton")
        add_button.pack(side=tk.LEFT)

        # Frame para la lista de tareas
        tasks_frame = ttk.LabelFrame(main_frame, text="Lista de Tareas")
        tasks_frame.pack(fill=tk.BOTH, expand=True, pady=10)

        # Scrollbar para la lista
        scrollbar = ttk.Scrollbar(tasks_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Lista de tareas
        self.task_listbox = tk.Listbox(tasks_frame, height=12, selectmode=tk.SINGLE)
        self.task_listbox.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)

        # Configurar scrollbar
        self.task_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=self.task_listbox.yview)

        # Frame para botones de acción
        button_frame = ttk.Frame(main_frame)
        button_frame.pack(fill=tk.X, pady=5)

        # Botón para marcar como completada
        complete_button = ttk.Button(button_frame, text="Completar (C)",
                                     command=self.complete_task, style="Complete.TButton")
        complete_button.pack(side=tk.LEFT, padx=(0, 5), fill=tk.X, expand=True)

        # Botón para eliminar tarea
        delete_button = ttk.Button(button_frame, text="Eliminar (D)",
                                   command=self.delete_task, style="Delete.TButton")
        delete_button.pack(side=tk.LEFT, fill=tk.X, expand=True)

        # Frame para atajos de teclado
        shortcut_frame = ttk.LabelFrame(main_frame, text="Atajos de Teclado")
        shortcut_frame.pack(fill=tk.X, pady=5)

        # Información de atajos
        shortcuts_text = """
        • Enter: Añadir nueva tarea
        • C: Marcar tarea como completada
        • D: Eliminar tarea seleccionada
        • Esc: Cerrar aplicación
        """
        shortcuts_label = ttk.Label(shortcut_frame, text=shortcuts_text, justify=tk.LEFT)
        shortcuts_label.pack(padx=5, pady=5)

    def setup_keyboard_shortcuts(self):
        """Configurar atajos de teclado"""
        # Enter para añadir tarea
        self.task_entry.bind("<Return>", lambda event: self.add_task())

        # C para completar tarea
        self.root.bind("<c>", lambda event: self.complete_task())
        self.root.bind("<C>", lambda event: self.complete_task())

        # D o Delete para eliminar tarea
        self.root.bind("<d>", lambda event: self.delete_task())
        self.root.bind("<D>", lambda event: self.delete_task())
        self.root.bind("<Delete>", lambda event: self.delete_task())

        # Escape para cerrar la aplicación
        self.root.bind("<Escape>", lambda event: self.root.destroy())

    def add_task(self):
        """Añadir una nueva tarea a la lista"""
        task = self.task_entry.get().strip()
        if task:
            self.tasks.append(task)
            self.update_listbox()
            self.task_entry.delete(0, tk.END)
        else:
            messagebox.showwarning("Advertencia", "Por favor, ingrese una tarea.")

    def complete_task(self):
        """Marcar tarea seleccionada como completada"""
        try:
            index = self.task_listbox.curselection()[0]
            task = self.task_listbox.get(index)

            # Verificar si la tarea ya está completada
            if task.startswith("✓ "):
                return

            # Marcar como completada
            self.completed_tasks.append(self.tasks[index])
            self.update_listbox()

        except IndexError:
            messagebox.showinfo("Información", "Por favor, seleccione una tarea para completar.")

    def delete_task(self):
        """Eliminar tarea seleccionada"""
        try:
            index = self.task_listbox.curselection()[0]
            task = self.task_listbox.get(index)

            # Determinar si la tarea está completada
            is_completed = task.startswith("✓ ")

            # Eliminar de la lista correspondiente
            if is_completed:
                # Extraer el texto real de la tarea (sin el prefijo)
                task_text = task[2:].strip()
                if task_text in self.completed_tasks:
                    self.completed_tasks.remove(task_text)
            else:
                self.tasks.remove(task)

            self.update_listbox()

        except IndexError:
            messagebox.showinfo("Información", "Por favor, seleccione una tarea para eliminar.")

    def update_listbox(self):
        """Actualizar la visualización de la lista de tareas"""
        self.task_listbox.delete(0, tk.END)

        # Añadir tareas pendientes
        for task in self.tasks:
            if task not in self.completed_tasks:
                self.task_listbox.insert(tk.END, task)

        # Añadir tareas completadas
        for task in self.completed_tasks:
            if task in self.tasks:
                self.task_listbox.insert(tk.END, f"✓ {task}")
                # Configurar estilo visual para tareas completadas
                index = self.task_listbox.size() - 1
                self.task_listbox.itemconfig(index, fg="gray")


def main():
    root = tk.Tk()
    app = TodoApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()