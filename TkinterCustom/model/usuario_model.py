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
        self._usuarios.append(Usuario("Ana", 25, "Femenino", "avatar1.png"))
        self._usuarios.append(Usuario("Luis", 31, "Masculino", "avatar2.png"))
        self._usuarios.append(Usuario("Maria", 29, "Femenino", "avatar3.png"))

    def listar(self):
        return self._usuarios

    def obtener(self, indice):
        return self._usuarios[indice]
