import json
import os

# Base de datos temporal
Equipos = []
NOMBRE_ARCHIVO = "torneo.txt"


# --- FUNCIONES DE PERSISTENCIA (GUARDAR Y CARGAR) ---
def CargarDatos():
    """Busca el archivo JSON al iniciar. Si existe, carga los datos en la lista global."""
    global Equipos
    if os.path.exists(NOMBRE_ARCHIVO):
        try:
            with open(NOMBRE_ARCHIVO, "r", encoding="utf-8") as archivo:
                Equipos = json.load(archivo)
            print(
                f"\n[SISTEMA] Se cargaron correctamente {len(Equipos)} equipos desde '{NOMBRE_ARCHIVO}'."
            )
        except (IOError, json.JSONDecodeError):
            print(
                "\n[ERROR] El archivo de datos existe pero está corrupto o es ilegible."
            )
            print("Se iniciará con una base de datos vacía.")
    else:
        print(
            "\n[SISTEMA] No se encontró historial previo. Iniciando torneo desde cero."
        )


def GuardarDatos():
    """Toma la lista 'Equipos' y la escribe en el archivo JSON."""
    try:
        with open(NOMBRE_ARCHIVO, "w", encoding="utf-8") as archivo:
            # indent=4 hace que el archivo JSON sea legible si lo abres con el bloc de notas
            json.dump(Equipos, archivo, indent=4, ensure_ascii=False)
        print(
            f"\n[SISTEMA] ¡Datos guardados exitosamente en '{NOMBRE_ARCHIVO}'!"
        )
    except IOError:
        print("\n[ERROR] No se pudieron guardar los datos en el disco.")


# --- VALIDACIONES DE ENTRADA ---
def pedir_texto(mensaje):
    texto = ""
    while texto == "":
        texto = input(mensaje).strip()
        if texto == "":
            print("Error: el dato no puede estar vacio.")
    return texto


def pedir_entero(mensaje, minimo):
    valido = False
    numero = 0
    while not valido:
        try:
            numero = int(input(mensaje))
            if numero < minimo:
                print(f"Error: el numero no puede ser menor que {minimo}")
            else:
                valido = True
        except ValueError:
            print("Error: debe ingresar un numero entero.")
    return numero


# --- LÓGICA DEL TORNEO ---
def BuscarEquipo(Nombre):
    # Optimizado usando un bucle for simplificado con enumerate
    for i, equipo in enumerate(Equipos):
        if equipo["NEquipo"].lower() == Nombre.lower():
            return i
    return -1


def RegistrarEquipo():
    print("\n--- REGISTRAR EQUIPO ---")
    Nuevo = {}
    Nuevo["NEquipo"] = pedir_texto("Nombre del equipo: ")

    if BuscarEquipo(Nuevo["NEquipo"]) != -1:
        print("Ese equipo ya existe.")
    else:
        Nuevo["Ciudad"] = pedir_texto("Ciudad: ")
        Nuevo["Parti"] = 0
        Nuevo["Vic"] = 0
        Nuevo["Emp"] = 0
        Nuevo["Derr"] = 0
        Nuevo["GolFav"] = 0
        Nuevo["GolCon"] = 0
        Nuevo["DifGol"] = 0
        Nuevo["TarjA"] = 0
        Nuevo["TarjR"] = 0
        Nuevo["PTS"] = 0

        Equipos.append(Nuevo)
        print("Equipo registrado correctamente.")


def MostrarEquipos():
    print("\n--- EQUIPOS REGISTRADOS ---")
    if len(Equipos) == 0:
        print("No hay equipos registrados.")
    else:
        for i, equipo in enumerate(Equipos):
            print(f"{i + 1} - {equipo['NEquipo']} - {equipo['Ciudad']}")


def ActualizarEquipo(Posicion, GFavor, GContra, Amarillas, Rojas):
    Equipos[Posicion]["Parti"] += 1
    Equipos[Posicion]["GolFav"] += GFavor
    Equipos[Posicion]["GolCon"] += GContra
    Equipos[Posicion]["DifGol"] = (
        Equipos[Posicion]["GolFav"] - Equipos[Posicion]["GolCon"]
    )
    Equipos[Posicion]["TarjA"] += Amarillas
    Equipos[Posicion]["TarjR"] += Rojas

    if GFavor > GContra:
        Equipos[Posicion]["Vic"] += 1
        Equipos[Posicion]["PTS"] += 3
    elif GFavor == GContra:
        Equipos[Posicion]["Emp"] += 1
        Equipos[Posicion]["PTS"] += 1
    else:
        Equipos[Posicion]["Derr"] += 1


def RegistrarPartido():
    print("\n--- REGISTRAR PARTIDO ---")
    if len(Equipos) < 2:
        print("Deben existir al menos 2 equipos para registrar un partido.")
    else:
        MostrarEquipos()
        Nombre1 = pedir_texto("\nPrimer equipo: ")
        Nombre2 = pedir_texto("Segundo equipo: ")

        Pos1 = BuscarEquipo(Nombre1)
        Pos2 = BuscarEquipo(Nombre2)

        if Pos1 == -1 or Pos2 == -1:
            print("Equipo inexistente.")
        elif Pos1 == Pos2:
            print("No puede jugar contra si mismo.")
        else:
            print(f"\nDatos de {Equipos[Pos1]['NEquipo']}")
            Goles1 = pedir_entero("Goles equipo 1: ", 0)
            Amarillas1 = pedir_entero("Tarjetas amarillas equipo 1: ", 0)
            Rojas1 = pedir_entero("Tarjetas rojas equipo 1: ", 0)

            print(f"\nDatos de {Equipos[Pos2]['NEquipo']}")
            Goles2 = pedir_entero("Goles equipo 2: ", 0)
            Amarillas2 = pedir_entero("Tarjetas amarillas equipo 2: ", 0)
            Rojas2 = pedir_entero("Tarjetas rojas equipo 2: ", 0)

            ActualizarEquipo(Pos1, Goles1, Goles2, Amarillas1, Rojas1)
            ActualizarEquipo(Pos2, Goles2, Goles1, Amarillas2, Rojas2)
            print("Partido registrado correctamente.")


def BuscarDatosEquipo():
    print("\n--- BUSCAR DATOS DE EQUIPO ---")
    if len(Equipos) == 0:
        print("No hay equipos registrados.")
    else:
        Nombre1 = pedir_texto("Nombre del equipo: ")
        Pos1 = BuscarEquipo(Nombre1)

        if Pos1 == -1:
            print("Equipo inexistente.")
        else:
            eq = Equipos[Pos1]
            print(f"\nEquipo: {eq['NEquipo']}")
            print(f"Ciudad: {eq['Ciudad']}")
            print(f"Partidos Jugados: {eq['Parti']}")
            print(f"Victorias: {eq['Vic']}")
            print(f"Empates: {eq['Emp']}")
            print(f"Derrotas: {eq['Derr']}")
            print(f"Gol a Favor: {eq['GolFav']}")
            print(f"Gol en Contra: {eq['GolCon']}")
            print(f"Diferencia de Goles: {eq['DifGol']}")
            print(f"Tarjetas Amarillas: {eq['TarjA']}")
            print(f"Tarjetas Rojas: {eq['TarjR']}")
            print(f"PTS: {eq['PTS']}")


def MostrarTabla():
    print("\n--- TABLA DE POSICIONES ---")
    if len(Equipos) == 0:
        print("No hay equipos registrados.")
    else:
        Tabla = sorted(
            Equipos,
            key=lambda Equipo: (
                Equipo["PTS"],
                Equipo["DifGol"],
                Equipo["GolFav"],
            ),
            reverse=True,
        )

        print("POS EQUIPO             PJ  VIC EMP DERR GF  GC  DG  TA  TR  PTS")
        print("---------------------------------------------------------------")
        for i, eq in enumerate(Tabla):
            # Optimizado usando alineaciones con f-strings modernos (< izquierda, > derecha)
            print(
                f"{i + 1:<3} {eq['NEquipo']:<18} {eq['Parti']:>2} {eq['Vic']:>4} "
                f"{eq['Emp']:>3} {eq['Derr']:>4} {eq['GolFav']:>2} {eq['GolCon']:>3} "
                f"{eq['DifGol']:>3} {eq['TarjA']:>3} {eq['TarjR']:>3} {eq['PTS']:>4}"
            )


def MostrarEstadisticas():
    print("\n--- ESTADISTICAS GENERALES ---")
    if len(Equipos) == 0:
        print("No hay datos para mostrar.")
    else:
        TotalGoles = 0
        TotalTarjetasAmarillas = 0
        TotalTarjetasRojas = 0
        TotalPartidosContados = 0

        EquipoMasPuntos = Equipos[0]
        EquipoMasGoleador = Equipos[0]
        EquipoMasTarjetasRojas = Equipos[0]

        for Equipo in Equipos:
            TotalGoles += Equipo["GolFav"]
            TotalTarjetasAmarillas += Equipo["TarjA"]
            TotalTarjetasRojas += Equipo["TarjR"]
            TotalPartidosContados += Equipo["Parti"]

            if Equipo["PTS"] > EquipoMasPuntos["PTS"]:
                EquipoMasPuntos = Equipo
            if Equipo["GolFav"] > EquipoMasGoleador["GolFav"]:
                EquipoMasGoleador = Equipo
            if Equipo["TarjR"] > EquipoMasTarjetasRojas["TarjR"]:
                EquipoMasTarjetasRojas = Equipo

        TotalPartidos = TotalPartidosContados // 2

        print(f"Cantidad de equipos: {len(Equipos)}")
        print(f"Total de partidos jugados: {TotalPartidos}")
        print(f"Total de goles: {TotalGoles}")
        print(f"Total de tarjetas amarillas: {TotalTarjetasAmarillas}")
        print(f"Total de tarjetas rojas: {TotalTarjetasRojas}")

        if TotalPartidos > 0:
            PromedioGoles = TotalGoles / TotalPartidos
            print(f"Promedio de goles por partido: {round(PromedioGoles, 2)}")
        else:
            print("Promedio de goles por partido: 0")

        print(f"Equipo con mas puntos: {EquipoMasPuntos['NEquipo']}")
        print(f"Equipo mas goleador: {EquipoMasGoleador['NEquipo']}")
        print(
            f"Equipo con mas tarjetas rojas: {EquipoMasTarjetasRojas['NEquipo']}"
        )


def MostrarMenu():
    print("\n====================================")
    print("     GESTION DE TORNEO AMATEUR")
    print("====================================")
    print("1. Registrar equipo")
    print("2. Mostrar equipos")
    print("3. Registrar partido")
    print("4. Buscar datos de equipo")
    print("5. Mostrar tabla de posiciones")
    print("6. Mostrar estadisticas generales")
    print("7. Salir y Guardar")


def Menu():
    # NUEVO: Intentar cargar los datos al iniciar la aplicación
    CargarDatos()

    Opcion = 0
    while Opcion != 7:
        MostrarMenu()
        Opcion = pedir_entero("Seleccione una opcion: ", 1)

        if Opcion == 1:
            RegistrarEquipo()
        elif Opcion == 2:
            MostrarEquipos()
        elif Opcion == 3:
            RegistrarPartido()
        elif Opcion == 4:
            BuscarDatosEquipo()
        elif Opcion == 5:
            MostrarTabla()
        elif Opcion == 6:
            MostrarEstadisticas()
        elif Opcion == 7:
            # NUEVO: Guardar automáticamente los datos antes de cerrar
            GuardarDatos()
            print("Gracias por usar el sistema.")
        else:
            print("Opcion invalida. Intente nuevamente.")


# Arrancar el programa
Menu()
