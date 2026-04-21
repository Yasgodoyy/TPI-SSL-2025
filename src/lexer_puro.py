import re
import ply.lex as lex
import os
import sys

tokens = (
    "CORCHETE_I", "CORCHETE_D", "LLAVE_I", "LLAVE_D",
    "COMA", "COMILLA", "DOSPUNTOS",
    "EQUIPOS", "VERSION", "FIRMA_DIGITAL", "NOMBRE_EQ", "IDENTIDAD_EQ", "LINK",
    "ASIGNATURA", "CARRERA", "UNIVERSIDAD_REG", "DIRECCION", "ALIANZA_EQ",
    "NOMBRE", "EDAD", "CARGO", "FOTO", "EMAIL", "HABILIDADES", "SALARIO", "ACTIVO",
    "PROYECTOS", "NOMBRE_PROY", "ESTADO_PROY", "RESUMEN_PROY", "TAREAS_PROY",
    "FECHA_INICIO", "FECHA_FIN", "FECHA_VALOR", "VIDEO_PROY", "CONCLUSION_PROY",
    "FECHA", "NULL", "INTEGER", "FLOAT", "BOOLEAN", "URL", "STRING"
)

t_COMILLA = r'\"'
t_CORCHETE_I = r'\['
t_CORCHETE_D = r'\]'
t_LLAVE_I = r'\{'
t_LLAVE_D = r'\}'
t_COMA = r','
t_DOSPUNTOS = r':'
t_ignore = ' \t\n'

def t_FECHA_VALOR(t):
    r'"(19|20)\d{2}-\d{2}-\d{2}"'
    return t

def t_URL(t):
    r'"https?://[^\s"]+"'
    return t

def t_STRING(t):
    r'"[^"]*"'
    palabras_reservadas = {
        '"equipos"': "EQUIPOS", '"version"': "VERSION", '"firma_digital"': "FIRMA_DIGITAL",
        '"nombre_equipo"': "NOMBRE_EQ", '"identidad_equipo"': "IDENTIDAD_EQ", '"link"': "LINK",
        '"asignatura"': "ASIGNATURA", '"carrera"': "CARRERA", '"universidad_regional"': "UNIVERSIDAD_REG",
        '"direccion"': "DIRECCION", '"alianza equipo"': "ALIANZA_EQ", '"nombre"': "NOMBRE",
        '"edad"': "EDAD", '"cargo"': "CARGO", '"foto"': "FOTO", '"email"': "EMAIL",
        '"habilidades"': "HABILIDADES", '"salario"': "SALARIO", '"activo"': "ACTIVO",
        '"proyectos"': "PROYECTOS", '"estado"': "ESTADO_PROY", '"resumen"': "RESUMEN_PROY",
        '"tareas"': "TAREAS_PROY", '"fecha_creacion"': "FECHA_INICIO", '"fecha_fin"': "FECHA_FIN",
        '"video"': "VIDEO_PROY", '"conclusion"': "CONCLUSION_PROY"
    }
    if t.value in palabras_reservadas:
        t.type = palabras_reservadas[t.value]
    return t

def t_FLOAT(t):
    r'\d+\.\d{1,2}'
    t.value = float(t.value)
    return t

def t_INTEGER(t):
    r'-?\d+'
    t.value = int(t.value)
    return t


def t_BOOLEAN(t):
    r'(true|false)'
    t.value = True if t.value == 'true' else False
    return t

def t_NULL(t):
    r'null'
    return t

def t_error(t):
    
    print(f"**ERROR:** Carácter inesperado '{t.value[0]}' "
          f"No es un token reconocido.")
    t.lexer.skip(1) # Salta el carácter ilegal para continuar el análisis

lexer = lex.lex()

opcion = input("Ingrese 1 para analisis interactivo, 2 para analisis de archivo\n")
if opcion == "2":
    # Búsqueda del archivo JSON"
    if getattr(sys, 'frozen', False):
        ruta_json = os.path.join(os.path.dirname(sys.executable), 'turing_version_base.json')
    else:
        ruta_base = os.path.dirname(os.path.abspath(__file__))
        ruta_json = os.path.join(ruta_base, 'turing_version_base.json')

    # Intentar leer el archivo JSON
    try:
        with open(ruta_json, 'r', encoding='utf-8') as f:
            data = f.read()
    except FileNotFoundError:
        print(f"[ERROR FATAL] No se encontró el archivo JSON en: {ruta_json}")
        print("Asegúrate de que 'turing_version_base.json' esté en el mismo directorio que el ejecutable.")
        sys.exit(1) # Salir si el archivo no se encuentra

    print("--- ANÁLISIS DEL ARCHIVO JSON ---")
    lexer.input(data) # Alimentar el lexer con el contenido del JSON

    # Procesar y mostrar los tokens del archivo JSON
    for tok in lexer:
        # Formato de salida para tokens encontrados
        print(f"Se encontró el token '{tok.value}' de tipo {tok.type}")
    
    print("----------------------------------\n")

    # Mantener el programa abierto y esperando EOF
    print("Análisis del archivo JSON completado.")
    print("Presiona 'Control + Z' y luego Enter para salir (en Windows).")
    print("En Linux/macOS, presiona 'Control + D'.")
    try:
       while True:
           # Esta línea es solo para mantener la consola abierta.
           # No procesa ninguna entrada aquí, solo espera la señal EOF.
           input()
    except EOFError:
        print("\nSaliendo del programa.")
    except Exception as e:
        print(f"Ocurrió un error inesperado durante la espera: {e}")

else: 
    if opcion == "1":
        # --- INICIO DEL CÓDIGO PARA MODO INTERACTIVO ---
        print("Modo interactivo: Ingresa palabras para ver si son tokens.")
        print("------------------------------")
        print("Para salir, presiona 'Control + Z' y luego Enter (en Windows).")
        print("En Linux/macOS, presiona 'Control + D'.")
        print("------------------------------")

    while True:
        try:
            # Pide al usuario que ingrese una palabra
            palabra = input(">> ").strip() # Leer la línea y eliminar espacios
            
            # Si el usuario ingresa una línea vacía, simplemente pide otra.
            if not palabra:
                continue 

            # Configura el lexer para analizar solo la palabra ingresada
            lexer.input(palabra)
            
            # Intenta obtener el primer (y debería ser único) token
            tok = lexer.token()

            # Verifica si se encontró un token y si no hay más caracteres sin tokenizar
            if tok and not lexer.token(): # Si tok existe y no hay un segundo token (significa que toda la entrada fue un token)
                print(f"'{palabra}' es un **TOKEN**: {tok.type} (Valor: {tok.value})")
            else:
                print(f"'{palabra}' **NO** es un token reconocido.")
        except EOFError:
            print("\nSaliendo del programa.")
            break # Salir del bucle al detectar EOF
        except Exception as e:
            # Capturar cualquier otra excepción inesperada
            print(f"Ocurrió un error inesperado: {e}")
            print("Por favor, inténtalo de nuevo o presiona Control+Z/D para salir.")   