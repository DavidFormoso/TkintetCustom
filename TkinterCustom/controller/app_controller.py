import threading
import tkinter.messagebox as messagebox
from pathlib import Path
from PIL import Image
import customtkinter as ctk

from model.usuario_model import GestorUsuarios, Usuario
from view.main_view import MainView, AddUserView, EditUserView


class AppController:
    def __init__(self, master):
        self.master = master
        self.modelo = GestorUsuarios()
        self.view = MainView(master)

        self.BASE_DIR = Path(__file__).resolve().parent.parent
        self.ASSETS_PATH = self.BASE_DIR / "assets"
        self.CSV_PATH = self.BASE_DIR / "usuarios.csv"

        self.indices_visibles = list(range(len(self.modelo.listar())))
        self.usuario_actual = 0 if self.indices_visibles else None

        self.auto_guardar_activo = False
        self._auto_guardar_stop = threading.Event()
        self._auto_guardar_thread = None

        self.view.configurar_callback_nuevo_usuario(self.abrir_ventana_anadir)
        self.view.configurar_callback_eliminar(self.eliminar_usuario)
        self.view.configurar_menu_archivo(
            on_cargar=lambda: self.cargar_usuarios(mostrar_mensajes=True),
            on_guardar=self.guardar_usuarios,
            on_salir=self.salir,
        )
        self.view.configurar_callbacks_filtro(self.actualizar_vista_lista_y_estado)
        self.view.configurar_callback_salir(self.salir)
        self.view.configurar_callback_autoguardar(self.toggle_auto_guardado)
        self.view.set_estado_autoguardar(False)

        self.actualizar_vista_lista_y_estado()

    def aplicar_filtros(self):
        texto = self.view.get_texto_busqueda().strip().lower()
        genero = self.view.get_filtro_genero()

        nuevos_indices = []
        for i, u in enumerate(self.modelo.listar()):
            if texto and texto not in u.nombre.lower():
                continue
            if genero != "Todos" and u.genero != genero:
                continue
            nuevos_indices.append(i)

        self.indices_visibles = nuevos_indices

    def actualizar_vista_lista_y_estado(self):
        self.aplicar_filtros()
        usuarios = [self.modelo.listar()[i] for i in self.indices_visibles]
        self.view.actualizar_lista_usuarios(
            usuarios,
            on_seleccionar=self._on_seleccionar_visual,
            on_editar=self._on_editar_visual,
        )

        total = len(self.modelo.listar())
        visibles = len(self.indices_visibles)
        self.view.actualizar_estado(f"Usuarios visibles: {visibles}/{total}")

        if visibles > 0:
            self._on_seleccionar_visual(0)
        else:
            vacio = Usuario("-", "-", "-", "")
            self.view.mostrar_detalles_usuario(vacio, None)

    def _on_seleccionar_visual(self, idx_vista):
        if not self.indices_visibles:
            return
        real_idx = self.indices_visibles[idx_vista]
        self.usuario_actual = real_idx
        usuario = self.modelo.obtener(real_idx)
        avatar = self.cargar_avatar(usuario.avatar)
        self.view.mostrar_detalles_usuario(usuario, avatar)

    def _on_editar_visual(self, idx_vista):
        if not self.indices_visibles:
            return
        real_idx = self.indices_visibles[idx_vista]
        self.abrir_ventana_editar(real_idx)

    def cargar_avatar(self, nombre_archivo):
        if not nombre_archivo:
            return None
        ruta = self.ASSETS_PATH / nombre_archivo
        try:
            imagen = Image.open(ruta)
        except FileNotFoundError:
            return None
        return ctk.CTkImage(light_image=imagen, dark_image=imagen, size=(120, 120))

    def abrir_ventana_anadir(self):
        add_view = AddUserView(self.master)
        add_view.boton_guardar.configure(command=lambda: self.anadir_usuario(add_view))
        add_view.boton_cancelar.configure(command=add_view.window.destroy)

    def anadir_usuario(self, add_view):
        datos = add_view.get_data()
        nombre = datos["nombre"]
        edad_txt = datos["edad"]
        genero = datos["genero"]
        avatar = datos["avatar"]

        if not nombre or not edad_txt or not genero:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            edad = int(edad_txt)
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número entero.")
            return

        nuevo = Usuario(nombre, edad, genero, avatar)
        self.modelo.añadir(nuevo)
        add_view.window.destroy()
        self.actualizar_vista_lista_y_estado()
        self.view.actualizar_estado("Usuario añadido correctamente.")

    def abrir_ventana_editar(self, indice):
        usuario = self.modelo.obtener(indice)
        edit_view = EditUserView(self.master, usuario)
        edit_view.boton_guardar.configure(
            command=lambda: self.guardar_cambios_usuario(edit_view, indice)
        )
        edit_view.boton_cancelar.configure(command=edit_view.window.destroy)

    def guardar_cambios_usuario(self, edit_view, indice):
        datos = edit_view.get_data()
        nombre = datos["nombre"]
        edad_txt = datos["edad"]
        genero = datos["genero"]
        avatar = datos["avatar"]

        if not nombre or not edad_txt or not genero:
            messagebox.showerror("Error", "Todos los campos son obligatorios.")
            return

        try:
            edad = int(edad_txt)
        except ValueError:
            messagebox.showerror("Error", "La edad debe ser un número entero.")
            return

        usuario = self.modelo.obtener(indice)
        usuario.nombre = nombre
        usuario.edad = edad
        usuario.genero = genero
        usuario.avatar = avatar

        edit_view.window.destroy()
        self.actualizar_vista_lista_y_estado()
        self.view.actualizar_estado("Usuario editado correctamente.")

    def eliminar_usuario(self):
        if self.usuario_actual is None or not self.modelo.listar():
            messagebox.showwarning("Atención", "No hay usuarios para eliminar.")
            return

        if not messagebox.askyesno("Confirmar", "¿Eliminar el usuario seleccionado?"):
            return

        self.modelo.eliminar(self.usuario_actual)
        self.usuario_actual = 0 if self.modelo.listar() else None
        self.actualizar_vista_lista_y_estado()
        self.view.actualizar_estado("Usuario eliminado correctamente.")

    def guardar_usuarios(self):
        try:
            self.modelo.guardar_csv(self.CSV_PATH)
            self.view.actualizar_estado("Usuarios guardados en CSV.")
            messagebox.showinfo("Guardar", "Usuarios guardados correctamente.")
        except Exception as e:
            self.view.actualizar_estado("Error al guardar usuarios.")
            messagebox.showerror("Error", f"No se pudieron guardar los usuarios.\n{e}")

    def cargar_usuarios(self, mostrar_mensajes=True):
        ok = self.modelo.cargar_csv(self.CSV_PATH)
        self.indices_visibles = list(range(len(self.modelo.listar())))
        self.usuario_actual = 0 if self.indices_visibles else None
        self.actualizar_vista_lista_y_estado()

        if not mostrar_mensajes:
            return

        if ok:
            self.view.actualizar_estado("Usuarios cargados desde CSV.")
            messagebox.showinfo("Cargar", "Usuarios cargados correctamente.")
        else:
            self.view.actualizar_estado("No se encontraron usuarios válidos; se cargan por defecto.")
            messagebox.showwarning(
                "Cargar",
                "No se pudo cargar ningún usuario válido.\n"
                "Se han cargado los usuarios por defecto.",
            )

    def toggle_auto_guardado(self):
        if not self.auto_guardar_activo:
            self.auto_guardar_activo = True
            self._auto_guardar_stop.clear()
            self._auto_guardar_thread = threading.Thread(
                target=self._auto_guardar_loop, daemon=True
            )
            self._auto_guardar_thread.start()
            self.view.set_estado_autoguardar(True)
            self.view.actualizar_estado("Auto-guardado cada 10s: ACTIVADO.")
        else:
            self.auto_guardar_activo = False
            self._auto_guardar_stop.set()
            self.view.set_estado_autoguardar(False)
            self.view.actualizar_estado("Auto-guardado: DESACTIVADO.")

    def _auto_guardar_loop(self):
        while not self._auto_guardar_stop.wait(10.0):
            try:
                self.modelo.guardar_csv(self.CSV_PATH)
                self.master.after(
                    0, lambda: self.view.actualizar_estado("Auto-guardado realizado.")
                )
            except Exception:
                self.master.after(
                    0, lambda: self.view.actualizar_estado("Error en auto-guardado.")
                )

    def salir(self):
        if self.auto_guardar_activo:
            self.auto_guardar_activo = False
            self._auto_guardar_stop.set()
            if (
                self._auto_guardar_thread
                and self._auto_guardar_thread.is_alive()
            ):
                self._auto_guardar_thread.join(timeout=1)
        self.master.destroy()
