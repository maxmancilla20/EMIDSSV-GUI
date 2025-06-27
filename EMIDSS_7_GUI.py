import serial
import serial.tools.list_ports as list_ports
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import time
import os
import runpy

# Definir los valores por defecto
default_port_name = 'COM5'
default_baudrate = 9600

# Función para redimensionar imágenes
def resize_image(image_path, size):
    image = Image.open(image_path)
    image = image.resize(size, Image.LANCZOS)
    return ImageTk.PhotoImage(image)

# Función para verificar y manejar la conexión serial
def check_serial_connection(port, baudrate):
    try:
        ser = serial.Serial(
            port=port,
            baudrate=baudrate,
            bytesize=serial.EIGHTBITS,
            timeout=1
        )
        if not ser.is_open:
            raise serial.SerialException('No se puede establecer la conexión serial.')
        return ser
    except serial.SerialException as e:
        messagebox.showerror("Error", str(e))
        exit()

# Función para listar puertos
def list_ports():
    all_ports = list_ports.comports()
    output_text.insert(tk.END, "Available Ports:\n")
    for port in all_ports:
        output_text.insert(tk.END, f"{port.device} - {port.description}\n")

# Función para enviar comandos
def send_command(command):
    try:
        ser.write(command.encode('utf-8'))
        ser.write(command.encode('utf-8'))
        output_text.insert(tk.END, f"Command Sent: {command}\n")
    except Exception as e:
        output_text.insert(tk.END, f"Error: {str(e)}\n")

# Función para limpiar la salida
def clear_output():
    output_text.delete(1.0, tk.END)

# Función para graficar datos
def graph_data():
    runpy.run_path('GraphicData.py')

# Función para mostrar información
def show_info():
    messagebox.showinfo("How To Use this GUI",
                        "1. How to graph data:\n"
                        "    Fill EMIDSS_V_Data.xlsx with the data obtained from\n"
                        "    the EMIDSS memory data.")

# Configuración de la conexión serial
port_name = default_port_name
baudrate = default_baudrate
ser = check_serial_connection(port_name, baudrate)

# Crear la ventana principal
root = tk.Tk()
root.title("EMIDSS-V GUI")
root.configure(bg='white')

# Cargar imágenes
emidss_png = resize_image('EMIDS.png', (70, 70))
send_png = resize_image('send.png', (25, 25))
exit_png = resize_image('exit.png', (25, 25))

# Layout de la ventana
header_frame = tk.Frame(root, bg='white')
header_frame.pack(pady=10)
tk.Label(header_frame, image=emidss_png, bg='white').pack(side=tk.LEFT)
tk.Label(header_frame, text="EMIDSS-V GUI", font=("Verdana", 20), fg="blue", bg='white').pack(side=tk.LEFT)

services_frame = tk.Frame(root, bg='white')
services_frame.pack(pady=10)

# Read Service
tk.Label(services_frame, text="Read Service", font=("Verdana Bold", 12), bg='white').grid(row=0, column=0, padx=5)
combo_read = ttk.Combobox(services_frame, values=['Time', 'Memory', 'SW Version'], state="readonly", width=12)
combo_read.grid(row=1, column=0, padx=5)
tk.Button(services_frame, image=send_png, command=lambda: send_command(combo_read.get())).grid(row=1, column=1, padx=5)

# Write Service
tk.Label(services_frame, text="Write Service. Bytes", font=("Verdana Bold", 12), bg='white').grid(row=0, column=2, padx=5)
combo_write = ttk.Combobox(services_frame, values=['Hour'], state="readonly", width=12)
combo_write.grid(row=1, column=2, padx=5)
write_input_1 = tk.Entry(services_frame, width=3)
write_input_1.grid(row=1, column=3, padx=5)
write_input_2 = tk.Entry(services_frame, width=3)
write_input_2.grid(row=1, column=4, padx=5)
tk.Button(services_frame, image=send_png, command=lambda: send_command(f"S2301{write_input_1.get()}{write_input_2.get()}")).grid(row=1, column=5, padx=5)

# Reset Service
tk.Label(services_frame, text="Reset Service", font=("Verdana Bold", 12), bg='white').grid(row=0, column=6, padx=5)
combo_reset = ttk.Combobox(services_frame, values=['Sensor', 'Memory'], state="readonly", width=12)
combo_reset.grid(row=1, column=6, padx=5)
tk.Button(services_frame, image=send_png, command=lambda: send_command(f"S1101" if combo_reset.get() == "Sensor" else "S1102")).grid(row=1, column=7, padx=5)

# Raw Command
raw_frame = tk.Frame(root, bg='white')
raw_frame.pack(pady=10)
tk.Label(raw_frame, text="Raw Message", font=("Verdana Bold", 12), bg='white').pack(side=tk.LEFT, padx=5)
raw_command = tk.Entry(raw_frame, width=20)
raw_command.pack(side=tk.LEFT, padx=5)
tk.Button(raw_frame, image=send_png, command=lambda: send_command(raw_command.get())).pack(side=tk.LEFT, padx=5)

# Output and Buttons
output_frame = tk.Frame(root, bg='white')
output_frame.pack(pady=10)
output_text = scrolledtext.ScrolledText(output_frame, width=100, height=20, fg="green", wrap=tk.WORD)
output_text.pack()

buttons_frame = tk.Frame(root, bg='white')
buttons_frame.pack(pady=10)
tk.Button(buttons_frame, text="Clear Output", command=clear_output).pack(side=tk.LEFT, padx=5)
tk.Button(buttons_frame, text="Graph Data", command=graph_data).pack(side=tk.LEFT, padx=5)
tk.Button(buttons_frame, text="Info", command=show_info).pack(side=tk.LEFT, padx=5)
tk.Button(buttons_frame, image=exit_png, command=root.quit).pack(side=tk.LEFT, padx=5)

# Loop para leer datos del puerto serial
def read_serial():
    if ser.in_waiting > 0:
        line = ser.readline().decode('utf-8').rstrip()
        output_text.insert(tk.END, f"{line}\n")
        output_text.see(tk.END)
    root.after(100, read_serial)

read_serial()
root.mainloop()
ser.close()