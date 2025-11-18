import customtkinter as ctk
import tkinter as tk


class MainView:
    def __init__(self, master):
        self.master = master

        self.menubar = tk.Menu(self.master)
        self.menu_archivo = tk.Menu(self.menubar, tearoff=0)
        self.menu_ayuda = tk.Menu(self.menubar, tearoff=0)
        self.menubar.add_cascade(label="Archivo", menu=self.menu_archivo)
        self.menubar.add_cascade(label="Ayuda", menu=self.menu_ayuda)
        self.master.config(menu=self.menubar)

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_rowconfigure(1, weight=0)
        self.master.grid_columnconfigure(0, weight=1)

        self.frame_contenido = ctk.CTkFrame(self.master)
        self.frame_contenido.grid(row=0, column=0, sticky="nsew", padx=20, pady=(10, 5))

        self.frame_contenido.grid_columnconfigure(0, weight=1)
        self.frame_contenido.grid_columnconfigure(1, weight=1)
        self.frame_contenido.grid_rowconfigure(0, weight=1)

        self.frame_usuarios = ctk.CTkFrame(self.frame_contenido, corner_radius=10)
        self.frame_usuarios.grid(row=0, column=0, sticky="nsew", padx=(0, 10), pady=5)

        self.frame_detalles = ctk.CTkFrame(self.frame_contenido, corner_radius=10)
        self.frame_detalles.grid(row=0, column=1, sticky="nsew", padx=(10, 0), pady=5)

        self.label_titulo_usuarios = ctk.CTkLabel(
            self.frame_usuarios,
            text="Usuarios",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label_titulo_usuarios.pack(pady=(15, 5))

        self.contenedor_lista = ctk.CTkFrame(self.frame_usuarios, corner_radius=15)
        self.contenedor_lista.pack(expand=True, fill="both", padx=15, pady=(5, 15))

        self.contenedor_lista.grid_rowconfigure(0, weight=1)
        self.contenedor_lista.grid_columnconfigure(0, weight=1)

        self.frame_lista = ctk.CTkScrollableFrame(self.contenedor_lista)
        self.frame_lista.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.label_titulo_detalles = ctk.CTkLabel(
            self.frame_detalles,
            text="Detalles del Usuario",
            font=ctk.CTkFont(size=20, weight="bold")
        )
        self.label_titulo_detalles.pack(pady=(15, 5))

        self.contenedor_detalles = ctk.CTkFrame(self.frame_detalles, corner_radius=15)
        self.contenedor_detalles.pack(expand=True, fill="both", padx=15, pady=(5, 15))

        self.contenedor_detalles.grid_columnconfigure(0, weight=1)
        self.contenedor_detalles.grid_rowconfigure(0, weight=1)
        self.contenedor_detalles.grid_rowconfigure(1, weight=1)

        self.frame_avatar = ctk.CTkFrame(self.contenedor_detalles, fg_color="transparent")
        self.frame_avatar.grid(row=0, column=0, sticky="n", pady=(20, 10))

        self.avatar_label = ctk.CTkLabel(self.frame_avatar, text="")
        self.avatar_label.pack()

        self.frame_textos = ctk.CTkFrame(self.contenedor_detalles, fg_color="transparent")
        self.frame_textos.grid(row=1, column=0, sticky="nw", padx=40, pady=(10, 20))

        self.label_nombre = ctk.CTkLabel(self.frame_textos, text="", anchor="w")
        self.label_nombre.pack(anchor="w", pady=5)

        self.label_edad = ctk.CTkLabel(self.frame_textos, text="", anchor="w")
        self.label_edad.pack(anchor="w", pady=5)

        self.label_genero = ctk.CTkLabel(self.frame_textos, text="", anchor="w")
        self.label_genero.pack(anchor="w", pady=5)

        self.frame_inferior = ctk.CTkFrame(self.master)
        self.frame_inferior.grid(row=1, column=0, sticky="ew", padx=20, pady=(0, 10))

        self.frame_inferior.grid_columnconfigure(0, weight=1)
        self.frame_inferior.grid_columnconfigure(1, weight=0)
        self.frame_inferior.grid_columnconfigure(2, weight=1)

        self.boton_nuevo = ctk.CTkButton(self.frame_inferior, text="Añadir Usuario")
        self.boton_nuevo.grid(row=0, column=0, sticky="w", padx=(0, 10), pady=5)

        self.boton_salir = ctk.CTkButton(self.frame_inferior, text="Salir")
        self.boton_salir.grid(row=0, column=2, sticky="e", padx=(10, 0), pady=5)

        self._avatar_image = None

    def configurar_callback_nuevo_usuario(self, callback):
        self.boton_nuevo.configure(command=callback)

    def configurar_callback_salir(self, callback):
        self.boton_salir.configure(command=callback)

    def configurar_menu_archivo(self, on_cargar, on_guardar, on_salir):
        self.menu_archivo.delete(0, "end")
        self.menu_archivo.add_command(label="Cargar", command=on_cargar)
        self.menu_archivo.add_command(label="Guardar", command=on_guardar)
        self.menu_archivo.add_separator()
        self.menu_archivo.add_command(label="Salir", command=on_salir)

    def actualizar_lista_usuarios(self, usuarios, callback):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()
        for i, usuario in enumerate(usuarios):
            b = ctk.CTkButton(self.frame_lista, text=usuario.nombre, command=lambda idx=i: callback(idx))
            b.pack(fill="x", pady=5, padx=10)

    def mostrar_detalles_usuario(self, usuario, avatar_image=None):
        self.label_nombre.configure(text=f"Nombre: {usuario.nombre}")
        self.label_edad.configure(text=f"Edad: {usuario.edad}")
        self.label_genero.configure(text=f"Género: {usuario.genero}")
        if avatar_image is not None:
            self._avatar_image = avatar_image
            self.avatar_label.configure(image=self._avatar_image, text="")
        else:
            self._avatar_image = None
            self.avatar_label.configure(image=None, text="")


class AddUserView:
    def __init__(self, master):
        self.window = ctk.CTkToplevel(master)
        self.window.title("Añadir Nuevo Usuario")
        self.window.geometry("340x520")
        self.window.resizable(False, False)
        self.window.grab_set()

        self.window.grid_columnconfigure(0, weight=1)

        row = 0

        self.label_nombre = ctk.CTkLabel(self.window, text="Nombre:")
        self.label_nombre.grid(row=row, column=0, pady=(15, 0), padx=25, sticky="w")
        row += 1

        self.entry_nombre = ctk.CTkEntry(self.window)
        self.entry_nombre.grid(row=row, column=0, pady=(0, 10), padx=25, sticky="ew")
        row += 1

        self.label_edad = ctk.CTkLabel(self.window, text="Edad:")
        self.label_edad.grid(row=row, column=0, pady=(5, 0), padx=25, sticky="w")
        row += 1

        self.entry_edad = ctk.CTkEntry(self.window)
        self.entry_edad.grid(row=row, column=0, pady=(0, 10), padx=25, sticky="ew")
        row += 1

        self.label_genero = ctk.CTkLabel(self.window, text="Género:")
        self.label_genero.grid(row=row, column=0, pady=(10, 0), padx=25, sticky="w")
        row += 1

        self.var_genero = ctk.StringVar(value="Masculino")

        self.radio_genero_m = ctk.CTkRadioButton(self.window, text="Masculino", variable=self.var_genero, value="Masculino")
        self.radio_genero_m.grid(row=row, column=0, padx=35, sticky="w")
        row += 1

        self.radio_genero_f = ctk.CTkRadioButton(self.window, text="Femenino", variable=self.var_genero, value="Femenino")
        self.radio_genero_f.grid(row=row, column=0, padx=35, sticky="w")
        row += 1

        self.radio_genero_o = ctk.CTkRadioButton(self.window, text="Otro", variable=self.var_genero, value="Otro")
        self.radio_genero_o.grid(row=row, column=0, padx=35, sticky="w")
        row += 1

        self.label_avatar = ctk.CTkLabel(self.window, text="Avatar:")
        self.label_avatar.grid(row=row, column=0, pady=(15, 0), padx=25, sticky="w")
        row += 1

        self.var_avatar = ctk.StringVar(value="mujer1.png")

        self.radio_avatar1 = ctk.CTkRadioButton(self.window, text="Mujer 1", variable=self.var_avatar, value="mujer1.png")
        self.radio_avatar1.grid(row=row, column=0, padx=35, sticky="w")
        row += 1

        self.radio_avatar2 = ctk.CTkRadioButton(self.window, text="Hombre", variable=self.var_avatar, value="hombre.png")
        self.radio_avatar2.grid(row=row, column=0, padx=35, sticky="w")
        row += 1

        self.radio_avatar3 = ctk.CTkRadioButton(self.window, text="Mujer 2", variable=self.var_avatar, value="mujer2.png")
        self.radio_avatar3.grid(row=row, column=0, padx=35, sticky="w")
        row += 1

        self.window.grid_rowconfigure(row, weight=1)
        row += 1

        self.boton_guardar = ctk.CTkButton(self.window, text="Guardar", width=160)
        self.boton_guardar.grid(row=row, column=0, pady=(0, 8), padx=80, sticky="ew")
        row += 1

        self.boton_cancelar = ctk.CTkButton(self.window, text="Cancelar", width=160)
        self.boton_cancelar.grid(row=row, column=0, pady=(0, 15), padx=80, sticky="ew")

    def get_data(self):
        return {
            "nombre": self.entry_nombre.get().strip(),
            "edad": self.entry_edad.get().strip(),
            "genero": self.var_genero.get().strip(),
            "avatar": self.var_avatar.get().strip()
        }
