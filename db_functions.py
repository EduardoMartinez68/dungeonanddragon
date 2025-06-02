

# Función para agregar un jugador
def insertar_jugador(nombre, vida, mana, armadura, imagen):
    nuevo = Jugador(
        nombre=nombre,
        vida=vida,
        mana=mana,
        armadura=armadura,
        imagen=imagen
    )
    db.session.add(nuevo)
    db.session.commit()
    print(f"✅ Jugador '{nombre}' insertado con éxito.")

# Función para agregar un escenario
def insertar_escenario(lugar, clima, tiempo_dia):
    nuevo = Escenario(
        lugar=lugar,
        clima=clima,
        tiempo_dia=tiempo_dia
    )
    db.session.add(nuevo)
    db.session.commit()
    print(f"✅ Escenario '{lugar}' insertado con éxito.")

# Obtener todos los jugadores
def obtener_jugadores():
    return Jugador.query.all()

# Obtener todos los escenarios
def obtener_escenarios():
    return Escenario.query.all()

# Buscar jugador por nombre
def buscar_jugador(nombre):
    return Jugador.query.filter_by(nombre=nombre).first()

# Eliminar jugador
def eliminar_jugador(id_jugador):
    jugador = Jugador.query.get(id_jugador)
    if jugador:
        db.session.delete(jugador)
        db.session.commit()
        print(f"🗑️ Jugador eliminado: {jugador.nombre}")
    else:
        print("⚠️ Jugador no encontrado.")