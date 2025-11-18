import csv
from pathlib import Path


class Usuario:
    def __init__(self, nombre, edad, genero, avatar):
        self.nombre = nombre
        self.edad = edad
        self.genero = genero
        self.avatar = avatar


class GestorUsuarios:
    def __init__(self):
        self._cargar_por_defecto()

    def _cargar_por_defecto(self):
        self.usuarios = [
            Usuario("Ana", 25, "Femenino", "mujer 1.png"),
            Usuario("Luis", 30, "Masculino", "hombre.png"),
            Usuario("María", 28, "Femenino", "mujer 2.png"),
        ]

    def listar(self):
        return self.usuarios

    def obtener(self, indice):
        return self.usuarios[indice]

    def añadir(self, usuario):
        self.usuarios.append(usuario)

    def eliminar(self, indice):
        del self.usuarios[indice]

    def guardar_csv(self, ruta):
        ruta = Path(ruta)
        with open(ruta, "w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["nombre", "edad", "genero", "avatar"])
            for u in self.usuarios:
                writer.writerow([u.nombre, u.edad, u.genero, u.avatar])

    def cargar_csv(self, ruta):
        ruta = Path(ruta)
        if not ruta.exists():
            return False

        nuevos = []
        with open(ruta, "r", newline="", encoding="utf-8") as f:
            reader = csv.reader(f)
            next(reader, None)
            for row in reader:
                if len(row) != 4:
                    continue
                nombre, edad_txt, genero, avatar = row
                try:
                    edad = int(edad_txt)
                except ValueError:
                    continue
                nuevos.append(Usuario(nombre, edad, genero, avatar))

        if not nuevos:
            self._cargar_por_defecto()
            return False

        self.usuarios = nuevos
        return True
