class Usuario:
    def __init__(self, nombre, edad, genero, avatar):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.avatar = avatar

class GestorUsuarios:
    def __init__(self):
        self._usuarios = []
        self._cargar_datos_de_ejemplo()

    def _cargar_datos_de_ejemplo(self):
        self._usuarios.append(Usuario("Ana", 25, "Femenino", "Mujer 1.png"))
        self._usuarios.append(Usuario("Luis", 31, "Masculino", "Hombre.png"))
        self._usuarios.append(Usuario("Maria", 29, "Femenino", "Mujer 2.png"))

    def listar(self):
        return self._usuarios

    def obtener(self, indice):
        return self._usuarios[indice]

    def añadir(self, usuario):
        self._usuarios.append(usuario)
