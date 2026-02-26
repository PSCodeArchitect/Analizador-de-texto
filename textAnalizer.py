# normalizacion
def normalizar_texto(texto: str) -> str:
    texto = texto.lower()

    puntuacion = ".,;:!?()[]{}\"'"
    for p in puntuacion:
        texto = texto.replace(p, "")

    texto = " ".join(texto.split())
    return texto

# tokenizacion
def tokenizar(texto: str) -> list[str]:
    return texto.split()

# clase principal
class AnalizadorTexto:
    def __init__(self, texto: str):
        if not texto or not texto.strip():
            raise ValueError("el texto esta vacio")

        self.texto_original = texto
        self.texto_normalizado = ""
        self.tokens = []
        self.conteos = {}
        self.tokens_unicos = set()

    # analizar texto completo
    def analizar(self):
        self.texto_normalizado = normalizar_texto(self.texto_original)
        self.tokens = tokenizar(self.texto_normalizado)
        self.tokens_unicos = set(self.tokens)

        # conteo de tokens usando dict
        self.conteos = {}
        for token in self.tokens:
            self.conteos[token] = self.conteos.get(token, 0) + 1

    # reporte general
    def reporte(self):
        if not self.tokens:
            print("debe ejecutar analizar() primero")
            return

        total = len(self.tokens)
        unicos = len(self.tokens_unicos)

        print("\ntotal de tokens:", total)
        print("tokens unicos:", unicos)

        # top 10 palabras mas frecuentes
        top10 = sorted(self.conteos.items(), key=lambda x: x[1], reverse=True)[:10]
        print("\ntop 10 tokens mas frecuentes:")
        for token, cantidad in top10:
            print(token, ":", cantidad)

        # longitud promedio de palabra
        longitud_promedio = sum(len(t) for t in self.tokens) / total
        print("\nlongitud promedio de palabra:", round(longitud_promedio, 2))

        # palabra mas larga y mas corta
        max_len = max(len(t) for t in self.tokens)
        min_len = min(len(t) for t in self.tokens)

        mas_largas = {t for t in self.tokens if len(t) == max_len}
        mas_cortas = {t for t in self.tokens if len(t) == min_len}

        print("palabras mas largas:", mas_largas)
        print("palabras mas cortas:", mas_cortas)
        print()

    # consulta interactiva
    def consultar(self, palabra: str):
        palabra = normalizar_texto(palabra)

        total = len(self.tokens)
        cantidad = self.conteos.get(palabra, 0)

        if cantidad == 0:
            print("la palabra no existe en el texto")
            return

        porcentaje = (cantidad / total) * 100

        print("\nfrecuencia:", cantidad)
        print("porcentaje:", round(porcentaje, 2), "%")

        if cantidad == 1:
            print("clasificacion: palabra rara")
        elif cantidad >= 5:
            print("clasificacion: palabra comun")
        else:
            print("clasificacion: frecuencia media")

# modo archivo
def leer_desde_archivo():
    ruta = input("ingrese la ruta del archivo: ")
    try:
        with open(ruta, "r", encoding="utf-8") as f:
            texto = f.read()
        if not texto.strip():
            raise ValueError("el archivo esta vacio")
        return texto
    except FileNotFoundError:
        print("error: archivo no encontrado")
    except OSError:
        print("error: ruta invalida")
    except ValueError as e:
        print(e)
    return None

# modo consola
def leer_desde_consola():
    print("pegue el texto (escriba END para terminar):")
    lineas = []
    while True:
        linea = input()
        if "END" in linea:
            lineas.append(linea.split("END")[0].strip())
            break
        lineas.append(linea)
    texto = " ".join(lineas)
    if not texto.strip():
        raise ValueError("texto vacio")
    return texto

# pruebas minimas usando asserts
def ejecutar_pruebas():
    print("ejecutando pruebas...")

    # prueba normalizacion
    texto = "Hola!! Mundo"
    texto_norm = normalizar_texto(texto)
    assert texto_norm == "hola mundo", "fallo: normalizacion incorrecta"

    # prueba tokenizacion
    tokens = tokenizar("hola mundo")
    assert tokens == ["hola", "mundo"], "fallo: tokenizacion incorrecta"

    # prueba conteo
    analizador = AnalizadorTexto("hola hola mundo")
    analizador.analizar()
    # conteo de 'hola'
    assert analizador.conteos["hola"] == 2, "fallo: conteo de 'hola' incorrecto"
    # conteo de 'mundo'
    assert analizador.conteos["mundo"] == 1, "fallo: conteo de 'mundo' incorrecto"
    # tokens unicos
    assert len(analizador.tokens_unicos) == 2, "fallo: cantidad de tokens unicos incorrecta"

    print("todas las pruebas pasaron correctamente\n")

# programa principal
print("analizador de texto")
print("1.modo archivo")
print("2.modo consola")
print("3.ejecutar pruebas")

opcion = input("seleccione una opcion: ")

if opcion == "3":
    ejecutar_pruebas()
else:
    if opcion == "1":
        texto = leer_desde_archivo()
        if texto is None:
            exit()
    elif opcion == "2":
        try:
            texto = leer_desde_consola()
        except ValueError as e:
            print(e)
            exit()
    else:
        print("opcion invalida")
        exit()

    try:
        analizador = AnalizadorTexto(texto)
        analizador.analizar()
        analizador.reporte()

        while True:
            palabra = input("consultar palabra (exit para salir): ")
            if palabra.lower() == "exit":
                break
            analizador.consultar(palabra)
    except ValueError as e:
        print(e)