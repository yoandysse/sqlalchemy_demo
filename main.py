import db
import sys
from models import Persona
from sqlalchemy import and_, or_, text

def agregarPersonasIniciales():
    print("\n > AGREGAR PERSONAS INICIALES")

    p1 = Persona("Sara", 20)
    db.session.add(p1)

    p2 = Persona("Carlos", 30)
    db.session.add(p2)

    p3 = Persona("Ana", 32)
    db.session.add(p3)

    db.session.commit() # Enviamos los cambios a la bases de datos

    print("P1:", p1)
    print("P2:", p2)
    print("P3:", p3)

def consultasDePrueba():
    print("\n > CONSULTAS DE PRUEBA")

    print("\n #1. Obtener un objeto a partir de su id (primary key). Si no lo encuentra nos va a devolver None")
    result = db.session.query(Persona).get(1)
    print(result)

    print("\n #2. Obtener todos los objetos de una consulta: ")
    # Por defecto la instrucción query esta programada para devolver todos los resultados (coincidencias) que encuentre
    # No obstante, si queremos ejecutar de forma explicita que nos devuelve TODOS los resultados, sería así:
    # result = db.session.query(Persona).all()
    result = db.session.query(Persona)
    for p in result:
        print("\t > Nombre:", p.nombre, " -> Edad:", p.edad)

    print("\n #3. Obtener el primer objeto de una consulta:")
    result = db.session.query(Persona).first()
    print(result)

    print("\n #4. Contar el número de elementos devueltos por una consulta:")
    result = db.session.query(Persona).count()
    print(result)

    print("\n #5. Ordenar el resultado de una consulta:")
    result = db.session.query(Persona).order_by("nombre")
    for i in result:
        print(i)

    print("\n #6. Aplicar fltros a una consulta con filter_by: ")
    # filter_by es un filtro avanzado, el cual puede integrar codigo Python en sus comparativas
    result = db.session.query(Persona).filter_by(nombre="Sara").first()
    print(result)

    print("\n #7 Aplicar filtros a una consulta con filter: ")
    # filter es el where de sql, se pueden usar condicionales basicos como  == != < <= > >=
    result = db.session.query(Persona).filter(Persona.edad < 25)
    for i in result:
        print(i)

    print("\n #8 Aplicar el filtro ilike: ")
    result = db.session.query(Persona).filter(Persona.nombre.ilike("Sa%")) # ilike funciona buscando patrones en mayuscula y en minuscula
    for i in result:
        print(i)

    print("\n #9. Aplicar el operador in_: ")
    result = db.session.query(Persona).filter(Persona.id.in_([1,2])) # El operador in lleva un _ detras
    for i in result:
        print(i)

    print("\n #10. Aplicar el operador and_: ")
    # Hay que realizar el import: from sqlalchemy import and_
    result = db.session.query(Persona).filter(and_(Persona.id > 2, Persona.nombre.ilike("A%"))) # El operador and lleva un _ detras
    for i in result:
        print(i)

    print("\n #11. Aplicar el operador or_: ")
    # Hay que realizar el import: from sqlalchemy import or_
    result = db.session.query(Persona).filter(or_(Persona.id > 2, Persona.nombre.ilike("S%"))) # El operador or lleva un _ detras
    for i in result:
        print(i)

    print("\n #12. Ejecutar instrucciones SQL explicitas: ")
    # Hay que realizar el import: from sqlalchemy import text
    result = db.session.query(Persona).from_statement(text("SELECT * FROM Persona"))
    for i in result:
        print(i)

def aniadirPersona():
    print("\n > Agregar Persona: ")

    nombre = input("Nombre de la Persona: ")
    precio = int(input("Edad de la Persona: "))
    p = Persona(nombre, precio)
    db.session.add(p)
    db.session.commit()
    print("Persona CREADA")

def editarPersona():
    print("\n > Editar Persona: ")

    persona_id = input("ID de la Persona: ")
    exist_person = (db.session.query(Persona).filter_by(id=persona_id).first())

    if exist_person is None:
        print("La Persona indicada no existe")
    else:
        edad_nueva = int(input("Introduzca la nueva edad: "))
        exist_person.edad = edad_nueva
        db.session.commit()
        print("Persona ACTUALIZADA")

def borrarPersona():
    print("\n > Borrar Persona: ")

    persona_id = input("ID de la Persona: ")
    exist_person = (db.session.query(Persona).filter_by(id=persona_id).first())

    if exist_person is None:
        print("La Persona indicada no existe")
    else:
        db.session.query(Persona).filter(Persona.id == exist_person.id).delete()
        db.session.commit()
        print("Persona ELIMINADA")

def verTodasPersonas():
    print("\n > Ver todas las Personas: ")

    personas = db.session.query(Persona).all()
    for p in personas:
        print("\t > Nombre:", p.nombre, "-> Edad:", p.edad)

def buscarConPatron():
    print("\n > Buscar Personas que concuerden con el patrón: ")
    busqueda = input("Introduzca el patron: ")

    personas = db.session.query(Persona).filter(Persona.nombre.ilike(f'%{busqueda}%')).all()
    for p in personas:
        print("\t > Nombre:", p.nombre, "-> Edad:", p.edad)


if __name__ == '__main__':
    #  En la siguiente linea estamos indicando a SQLAlchemy que cree, si no existen, las tablas de
    #  todos los modelos que encuentre en la aplicación. Sin embargo, para que esto ocurra es necesario
    #  que cualquier modelo se haya importado previamente antes de llamar a la función create_all().
    db.Base.metadata.create_all(db.engine)

    while (True):
        print("\n1. Agregar personas iniciales\n"
              "2. Consultas de prueba\n"
              "3. Añadir una persona\n"
              "4. Editar una persona\n"
              "5. Eliminar una persona\n"
              "6. Ver todas las personas\n"
              "7. Buscar con un patrón\n"
              "8. Salir")
        opcion = int(input("Introduzca una opcion: "))
        if opcion == 1:
            agregarPersonasIniciales()
        elif opcion == 2:
            consultasDePrueba()
        elif opcion == 3:
            aniadirPersona()
        elif opcion == 4:
            editarPersona()
        elif opcion == 5:
            borrarPersona()
        elif opcion == 6:
            verTodasPersonas()
        elif opcion == 7:
            buscarConPatron()
        elif opcion == 8:
            sys.exit(1)
        else:
            print("Opcion no válida")