import db
from sqlalchemy import Column, Integer, String

class Persona(db.Base):
    __tablename__ = "persona"
    id = Column(Integer, primary_key=True) # Automaticamente esta PK se convertirá en SERIAL (AUTOINCREMENT)
    nombre = Column(String, nullable=False)
    edad = Column(Integer)

    def __init__(self, nombre, edad):
        self.nombre = nombre
        self.edad = edad

    def __str__(self):
        return "Persona({}: {}, {})".format(self.id, self.nombre, self.edad)

