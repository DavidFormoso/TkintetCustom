import tkinter.messagebox as messagebox
from pathlib import Path
from PIL import Image
import customtkinter as ctk
from model.usuario_model import GestorUsuarios, Usuario
from view.main_view import MainView, AddUserView

class AppController:
    def __init__(self, master):
        self.master = master
        self.modelo = GestorUsuarios()
        self.view = MainView(master)

        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.ASSETS_PATH = self.BASE_DIR / "assets"
        self.avatar_images = {}

        self.view.configurar_callback_nuevo_usuario(self.abrir_ventana_anadir)
        self.view.configurar_callback_salir(self.master.destroy)

        self.refrescar_lista_usuarios()
        if self.modelo.listar():
            self.seleccionar_usuario(0)

    def refrescar_lista_usuarios(self):
        usuarios = self.modelo.listar()
        self.view.actualizar_lista_usuarios(usuarios, self.seleccionar_usuario)

    def seleccionar_usuario(self, indice):
        usuario = self.modelo.obtener(indice)
        avatar_image = self.cargar_avatar(usuario.avatar)
        self.view.mostrar_detalles_usuario(usuario, avatar_image)

    def cargar_avatar(self, nombre_archivo):
        if not nombre_archivo:
            return None
        if nombre_archivo in self.avatar_images:
            return self.avatar_images[nombre_archivo]
        ruta = self.ASSETS_PATH / nombre_archivo
        try:
            imagen = Image.open(ruta)
        except FileNotFoundError:
            return None
        avatar_image = ctk.CTkImage(light_image=imagen, dark_image=imagen, size=(120, 120))
        self.avatar_images[nombre_archivo] = avatar_image
        return avatar_image

    def abrir_ventana_anadir(self):
        add_view = AddUserView(self.master)
        add_view.boton_guardar.configure(command=lambda: self.anadir_usuario(add_view))

    def anadir_usuario(self, add_view):
        datos = add_view.get_data()
        nombre = datos["nombre"]
        edad_texto = datos["edad"]
        genero = datos["genero"]
        avatar = datos["avatar"]

        if not nombre or not edad_texto or not genero:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return
        try:
            edad = int(edad_texto)
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número entero.")
            return

        usuario = Usuario(nombre, edad, genero, avatar)
        self.modelo.añadir(usuario)
        add_view.window.destroy()
        self.refrescar_lista_usuarios()
