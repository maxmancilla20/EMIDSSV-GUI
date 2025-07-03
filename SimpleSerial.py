import serial
import keyboard  # Necesario para detectar teclas

# Configuración del puerto serial
port = 'COM10'
baud_rate = 9600

# Crear conexión serial
try:
    ser = serial.Serial(port, baud_rate)
    print(f"Conectado al puerto {port} con baud rate {baud_rate}")
except serial.SerialException as e:
    print(f"Error al conectar al puerto {port}: {e}")
    ser = None

if ser:
    try:
        print("Presiona 'Escape' para salir.")
        while True:
            # Leer datos del puerto serial
            if ser.in_waiting > 0:
                received_data = ser.read(ser.in_waiting).decode('utf-8', errors='ignore')
                print(f"Datos recibidos: {received_data}")

            # Verificar si se presionó 'Escape' para salir
            if keyboard.is_pressed('Escape'):
                print("Saliendo del programa...")
                break

            # Leer y enviar caracteres ingresados desde el teclado
            if keyboard.read_event(suppress=True).event_type == 'down':
                event = keyboard.read_event(suppress=True)
                if len(event.name) == 1:  # Solo enviar caracteres válidos
                    ser.write(event.name.encode())
                    print(f"Carácter enviado: {event.name}")
    except Exception as e:
        print(f"Error durante la comunicación: {e}")
    finally:
        # Cerrar conexión
        ser.close()
        print("Conexión cerrada.")