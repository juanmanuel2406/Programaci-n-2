class Persona: 
    def __init__(self, nombre, apellido):
        self.nombre = nombre
        self.apellido = apellido

    def presentacion(self):
        print("Hola Soy {} {} ".format(self.nombre, self.apellido))

class Mamifero:
    especie = "Homo Sapiens"
    def presentacion(self):
        print("Hola soy un {}".format(self.especie))


class Profesor(Persona, Mamifero):
    pass

a = Profesor("Guille", "Ferrari")
#print(a.nombre, a.apellido, a.especie)
a.presentacion()