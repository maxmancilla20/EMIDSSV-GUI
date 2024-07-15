import serial
import serial.tools.list_ports as list_ports
import PySimpleGUI as sg
from PIL import Image

port_name = "COM22"  # the name / address we found for our device

ser = serial.Serial(
    port=port_name,
    baudrate=9600,
    bytesize=serial.EIGHTBITS,  # set this to the amount of data you want to send
    )

# the information we want to send: 8 bits = 1 byte
#byte_to_send = b"Hola soy python"
#ser.write(byte_to_send)

# After measurements are done, close the connection
#ser.close()
# Function to be called when the first button is pressed
def first_button_function():
    print("First button pressed!")

# Function to be called when the send button is pressed
def send_command_function(command):
    print(f"Command sent: {command}")

# Resize the image
def resize_image(image_path, size, name):
    image = Image.open(image_path)
    image = image.resize(size, Image.LANCZOS)
    image.save(name + "_png.png")
    return name + "_png.png"

# Path to your image
emidss_path = 'EMIDS.png'
# Desired size (width, height)
emidss_size = (70, 70)  # Adjust the size as needed
emidss_png = resize_image(emidss_path, emidss_size, "emidss")

# Path to your image
send_path = 'send.png'
# Desired size (width, height)
send_size = (25, 25)  # Adjust the size as needed
send_png = resize_image(send_path, send_size, "send")

# Path to your image
exit_path = 'exit.png'
# Desired size (width, height)
exit_size = (25, 25)  # Adjust the size as needed
exit_png = resize_image(exit_path, exit_size, "exit")

combo_read  = sg.Combo(['Memory', 'Sensor', 'Hour'], font=('Arial Bold', 10), enable_events=True, size=(12,1),key='-COMBO READ-')
combo_write = sg.Combo(['Hour'], font=('Arial Bold', 10), enable_events=True,size=(12,1), key='-COMBO WRITE-')
combo_reset = sg.Combo(['Memory', 'Sensor', 'EMIDSS'], font=('Arial Bold', 10), enable_events=True, size=(12,1), key='-COMBO RESET-')
blank_space_1 = sg.Text('                         ',background_color='white', key=None)
blank_space_2 = sg.Text('                         ',background_color='white', key=None)
Read_Service_Text  = sg.Text('Read Service',  font=("Verdana Bold",12), text_color="black", size=(27, 1), background_color='white')
Write_Service_Text = sg.Text('Write Service', font=("Verdana Bold",12), text_color="black", size=(28, 1), background_color='white')
Reset_Service_Text = sg.Text('Reset Service', font=("Verdana Bold",12), text_color="black", size=(15, 1), background_color='white')
Raw_Message_Text = sg.Text('Raw Message', font=("Verdana Bold",12), text_color="black", size=(12, 1), background_color='white')
exit_button = sg.Button(image_filename='exit_png.png', key='-EXIT-')
port_button = sg.Button('Get Ports', key='-GET PORTS-')

# Layout of the window
layout = [
    [sg.Text('',background_color='white', size=(33,1)), sg.Image(filename=emidss_png, key='-IMAGE-'), sg.Text('', font=("Verdana", 20), text_color="blue", size=(15, 1), background_color='white')],
    [Read_Service_Text, Write_Service_Text, Reset_Service_Text],
    [combo_read, sg.Button(image_filename='send_png.png', border_width=None, key='-SEND READ-'), blank_space_1,  combo_write, sg.Button(image_filename='send_png.png', border_width=None, key='-SEND WRITE-'), blank_space_2,  combo_reset, sg.Button(image_filename='send_png.png', border_width=None, key='-SEND RESET-')],
    [sg.Text('________________________________________________________________________', font=("Verdana Bold",12), text_color="black", size=(72, 1), background_color='white')],
    [Raw_Message_Text, sg.Input(size=(20,1), key='-COMMAND-'), sg.Button(image_filename='send_png.png', border_width=None, key='-SEND RAW-'), sg.Text('',background_color='white', size=(27,1)), port_button],
    [sg.Output(size=(90, 10))],  # Output area for displaying logs
    [exit_button]
]

# Create the window
window = sg.Window("EMIDSS-V GUI", layout, background_color='white')

# Event loop
while True:
    event, values = window.read()
    
    if event == sg.WIN_CLOSED or event == '-EXIT-':
        break
            
    if event == '-SEND READ-':
        read_action = values['-COMBO READ-']
        if read_action == 'Memory':
            print('Reading Memory')
            
            byte_to_send = b"S2203"
            ser.write(byte_to_send)
            ser.write(byte_to_send)

        elif read_action == 'Sensor':
            print('Reading Sensor')
            
            byte_to_send = b"S2201"
            #ser.write(byte_to_send)
            #ser.write(byte_to_send)

        elif read_action == 'Hour':
            print('Reading Hour')
            
            byte_to_send = b"S2202"
            #ser.write(byte_to_send)
            #ser.write(byte_to_send)
    
    if event == '-SEND WRITE-':
        read_action = values['-COMBO WRITE-']
        if read_action == 'Hour':
            print('Performing WRITE MEM...')
            
    if event == '-SEND RESET-':
        read_action = values['-COMBO RESET-']
        if read_action == 'Memory':
            print('Performing reset MEM...')
        elif read_action == 'Sensor':
            print('Performing Sensor reset...')

        elif read_action == 'EMIDSS':
            print('Performing emidss reset...')
            
               
    if event == '-SEND RAW-':
        command = values['-COMMAND-']
        send_command_function(command)
        
    if event == '-GET PORTS-':
        # List all comports
        all_ports = list_ports.comports()
        print(all_ports)

        # Each entry in the `all_ports` list is a serial device. Check it's
        # description and device attributes to learn more
        first_serial_device = all_ports[0]
        print(first_serial_device.device)  # the `port_name`
        print(first_serial_device.description)  # perhaps helpful to know if this is your device

     
window.close()
ser.close()