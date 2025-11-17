import customtkinter as ctk

class MainView:
    def __init__(self, master):
        self.master = master

        self.master.grid_rowconfigure(0, weight=1)
        self.master.grid_columnconfigure(0, weight=1)

        self.frame_principal = ctk.CTkFrame(self.master)
        self.frame_principal.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.frame_principal.grid_rowconfigure(0, weight=1)
        self.frame_principal.grid_columnconfigure(0, weight=1)
        self.frame_principal.grid_columnconfigure(1, weight=2)

        self.frame_lista = ctk.CTkScrollableFrame(self.frame_principal, width=250)
        self.frame_lista.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        self.frame_detalles = ctk.CTkFrame(self.frame_principal)
        self.frame_detalles.grid(row=0, column=1, sticky="nsew", padx=10, pady=10)

        self.label_nombre = ctk.CTkLabel(self.frame_detalles, text="", font=ctk.CTkFont(size=18))
        self.label_nombre.pack(pady=5, anchor="w")

        self.label_edad = ctk.CTkLabel(self.frame_detalles, text="")
        self.label_edad.pack(pady=5, anchor="w")

        self.label_genero = ctk.CTkLabel(self.frame_detalles, text="")
        self.label_genero.pack(pady=5, anchor="w")

        self.label_avatar = ctk.CTkLabel(self.frame_detalles, text="")
        self.label_avatar.pack(pady=10, anchor="w")

    def actualizar_lista_usuarios(self, usuarios, callback):
        for widget in self.frame_lista.winfo_children():
            widget.destroy()
        for i, usuario in enumerate(usuarios):
            b = ctk.CTkButton(self.frame_lista, text=usuario.nombre, command=lambda idx=i: callback(idx))
            b.pack(fill="x", pady=5, padx=5)

    def mostrar_detalles_usuario(self, usuario):
        self.label_nombre.configure(text=f"Nombre: {usuario.nombre}")
        self.label_edad.configure(text=f"Edad: {usuario.edad}")
        self.label_genero.configure(text=f"Género: {usuario.genero}")
        self.label_avatar.configure(text=f"Avatar: {usuario.avatar}")
