import csv

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

    def guardar_csv(self, ruta):
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            escritor = csv.writer(f)
            escritor.writerow(["nombre", "edad", "genero", "avatar"])
            for u in self._usuarios:
                escritor.writerow([u.nombre, u.edad, u.genero, u.avatar])

    def cargar_csv(self, ruta):
        try:
            with open(ruta, "r", newline="", encoding="utf-8") as f:
                lector = csv.reader(f)
                next(lector, None)
                self._usuarios.clear()
                for fila in lector:
                    if not fila:
                        continue
                    try:
                        nombre, edad_txt, genero, avatar = fila
                        edad = int(edad_txt)
                    except ValueError:
                        continue
                    self._usuarios.append(Usuario(nombre, edad, genero, avatar))
            return True
        except FileNotFoundError:
            self._usuarios.clear()
            self._cargar_datos_de_ejemplo()
            return False
