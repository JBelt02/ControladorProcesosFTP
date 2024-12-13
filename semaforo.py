import os
import time
import subprocess
import threading
import tkinter as tk
from tkinter import font
import math

# Ruta de la carpeta que contiene los archivos .bat y el archivo de orden
ruta_procesos = './Acciones'  
nombre_orden_txt = 'orden.txt'
ruta_orden_txt = os.path.join(ruta_procesos, nombre_orden_txt)

# Leer el archivo orden.txt y eliminar líneas vacías
with open(ruta_orden_txt, 'r') as archivo_orden:
    lineas = [linea.strip() for linea in archivo_orden if linea.strip()]  

luces = []
ejecutando = True

# Etiqueta para mostrar el nombre del script en ejecución
script_actual_label = None

# Función para ejecutar los scripts y actualizar el semáforo
def ejecutar_scripts():
    global ejecutando  
    ejecutar() 

def ejecutar():
    global ejecutando
    while ejecutando:
        for i, linea in enumerate(lineas):
            archivo_bat = os.path.join(ruta_procesos, linea.strip())  
            
            if os.path.exists(archivo_bat): 
                print(f"Ejecutando {archivo_bat}...")
                # Actualizar el semáforo y la etiqueta de script actual
                actualizar_semaforo(i, linea.strip())
                
                result = subprocess.call('"' + archivo_bat + '"', shell=True)

                if result != 0:  # Comprobar si hubo un error
                    error_label.config(text=f"Ha habido un error en el script {linea.strip()}.", fg="red", bg="#FFCCCB")  
                    error_label.update_idletasks()  
                    return  
                else:
                    error_label.config(text="", bg="#2C3E50")  
                    error_label.update_idletasks()  

            else:
                print(f"El archivo {archivo_bat} no existe.")
        
        # Apagar todas las luces al finalizar la secuencia
        restablecer_semaforos()

        # Temporizador de espera de 5 segundos
        for tiempo_restante in range(5, 0, -1):  
            # Actualizar la etiqueta de tiempo restante
            tiempo_label.config(text=f"Tiempo restante para la ejecución: {tiempo_restante} seg")
            tiempo_label.update_idletasks()  
            time.sleep(1)

        # Asegurarse de mostrar "0 seg" al finalizar la cuenta regresiva
        tiempo_label.config(text="Tiempo restante para la ejecución: 0 seg")
        tiempo_label.update_idletasks()  
        
        print("Esperando 5 segundos para repetir los scripts...")

# Función para actualizar el semáforo
def actualizar_semaforo(indice, nombre_script):
    # Apagar todas las luces
    for luz in luces:
        luz.config(bg='#E0E0E0')  

    # Encender la luz correspondiente en verde
    if 0 <= indice < len(luces):
        luces[indice].config(bg='green')
    
    # Actualizar la etiqueta que muestra el script actual
    script_actual_label.config(text=f"Ejecutándose: {nombre_script}")

# Función para restablecer el estado de los semáforos
def restablecer_semaforos():
    for luz in luces:
        luz.config(bg='#E0E0E0') 
    script_actual_label.config(text="")  
    root.update_idletasks()  

# Crear la ventana principal
root = tk.Tk()
root.title("Semáforo de Ejecución de Scripts (BAT)")
root.configure(bg="#2C3E50")  
root.geometry("800x500")  

# Estilo de fuente
fuente_titulo = font.Font(family="Helvetica", size=16, weight="bold")
fuente_luz = font.Font(family="Helvetica", size=12)

# Etiqueta del título
titulo_label = tk.Label(root, text="Control de Procesos", font=fuente_titulo, bg="#2C3E50", fg="white")
titulo_label.pack(pady=10) 

# Crear un marco para organizar elementos
frame = tk.Frame(root, bg="#34495E")
frame.pack(pady=20, padx=20, fill="both", expand=True)

# Determinar el número de scripts y la disposición de la matriz
num_scripts = len(lineas)

# Definir el tamaño de la cuadrícula basado en el número de scripts
if num_scripts <= 4:
    columns = 2  
    rows = 2  
elif num_scripts <= 9:
    columns = 3  
    rows = 3  
else:
    columns = math.ceil(math.sqrt(num_scripts))  
    rows = math.ceil(num_scripts / columns)  

# Crear los elementos del semáforo dinámicamente en una matriz
for i in range(num_scripts):
    # Muestra el nombre del archivo .bat en lugar de "Script X"
    nombre_script = lineas[i].strip()
    luz = tk.Label(frame, text=nombre_script, width=30, height=5, bg='#E0E0E0', font=fuente_luz)  # Ajustar el tamaño de los cuadros
    luz.grid(row=i // columns, column=i % columns, padx=10, pady=10, sticky="nsew")  # Usar sticky para hacerla responsiva
    luces.append(luz)  

# Configurar la cuadrícula para ser responsiva
for i in range(rows):
    frame.grid_rowconfigure(i, weight=1)
for j in range(columns):
    frame.grid_columnconfigure(j, weight=1)

# Etiqueta para mostrar el tiempo restante
tiempo_label = tk.Label(root, text="Tiempo restante para la ejecución: 0 seg", font=("Arial", 12), bg="#34495E", fg="white")
tiempo_label.pack(pady=10)

# Etiqueta para mostrar mensajes de error 
error_label = tk.Label(root, text="", font=("Arial", 12), bg="#FFCCCB", fg="red") 
error_label.pack(pady=10)

# Etiqueta para mostrar el nombre del script que se está ejecutando
script_actual_label = tk.Label(root, text="", font=("Arial", 12), bg="#2C3E50", fg="white")
script_actual_label.pack(pady=10)

# Crear un hilo para ejecutar los scripts en segundo plano
ejecutar_hilo = threading.Thread(target=ejecutar_scripts, daemon=True)
ejecutar_hilo.start()

# Iniciar la interfaz gráfica
root.mainloop()
