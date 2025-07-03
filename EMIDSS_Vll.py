import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, filedialog
import serial
import serial.tools.list_ports as list_ports
from PIL import Image, ImageTk
import threading
import time
import runpy

class SerialGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("EMIDSS-Vll GUI")
        self.ser = None
        self.stop_thread = False

        # Top frame for port/baudrate selection
        frame_top = tk.Frame(root)
        frame_top.pack(pady=5)

        tk.Label(frame_top, text="Port:").pack(side=tk.LEFT)
        self.port_var = tk.StringVar(value="COM7")
        self.port_entry = ttk.Combobox(frame_top, textvariable=self.port_var, width=8)
        self.port_entry['values'] = [port.device for port in list_ports.comports()]
        self.port_entry.pack(side=tk.LEFT, padx=5)

        tk.Label(frame_top, text="Baudrate:").pack(side=tk.LEFT)
        self.baud_var = tk.StringVar(value="9600")
        self.baud_entry = ttk.Entry(frame_top, textvariable=self.baud_var, width=8)
        self.baud_entry.pack(side=tk.LEFT, padx=5)

        self.connect_btn = ttk.Button(frame_top, text="Connect", command=self.connect_serial)
        self.connect_btn.pack(side=tk.LEFT, padx=5)

        self.clear_btn = ttk.Button(frame_top, text="Clear Output", command=lambda: self.output_text.delete(1.0, tk.END))
        self.clear_btn.pack(side=tk.LEFT, padx=5)

        # Output area
        self.output_text = scrolledtext.ScrolledText(root, width=90, height=18, fg="blue")
        self.output_text.pack(padx=10, pady=5)

        # Command frame
        frame_cmd = tk.Frame(root)
        frame_cmd.pack(pady=5)

        # Read Service
        tk.Label(frame_cmd, text="Read:").grid(row=0, column=0)
        self.combo_read = ttk.Combobox(frame_cmd, values=["Time", "Memory", "SW Version"], width=12)
        self.combo_read.grid(row=0, column=1)
        self.read_btn = ttk.Button(frame_cmd, text="Send", command=self.send_read)
        self.read_btn.grid(row=0, column=2, padx=5)

        # Write Service
        tk.Label(frame_cmd, text="Write:").grid(row=0, column=3)
        self.combo_write = ttk.Combobox(frame_cmd, values=["Hour"], width=8)
        self.combo_write.grid(row=0, column=4)
        self.write_in1 = ttk.Entry(frame_cmd, width=3)
        self.write_in1.grid(row=0, column=5)
        self.write_in2 = ttk.Entry(frame_cmd, width=3)
        self.write_in2.grid(row=0, column=6)
        self.write_btn = ttk.Button(frame_cmd, text="Send", command=self.send_write)
        self.write_btn.grid(row=0, column=7, padx=5)

        # Reset Service
        tk.Label(frame_cmd, text="Reset:").grid(row=0, column=8)
        self.combo_reset = ttk.Combobox(frame_cmd, values=["Sensor", "Memory"], width=8)
        self.combo_reset.grid(row=0, column=9)
        self.reset_btn = ttk.Button(frame_cmd, text="Send", command=self.send_reset)
        self.reset_btn.grid(row=0, column=10, padx=5)

        # Raw command
        tk.Label(frame_cmd, text="Raw:").grid(row=1, column=0)
        self.raw_entry = ttk.Entry(frame_cmd, width=20)
        self.raw_entry.grid(row=1, column=1, columnspan=2)
        self.raw_btn = ttk.Button(frame_cmd, text="Send", command=self.send_raw)
        self.raw_btn.grid(row=1, column=3, padx=5)

        # Info and Exit
        self.info_btn = ttk.Button(frame_cmd, text="Info", command=self.show_info)
        self.info_btn.grid(row=1, column=9)
        self.exit_btn = ttk.Button(frame_cmd, text="Exit", command=self.on_exit)
        self.exit_btn.grid(row=1, column=10, padx=5)

        # Graph button
        self.graph_btn = ttk.Button(frame_cmd, text="Graph Data", command=self.run_graph)
        self.graph_btn.grid(row=1, column=7, padx=5)

        # Serial reading thread
        self.read_thread = None

    def connect_serial(self):
        port = self.port_var.get()
        try:
            baud = int(self.baud_var.get())
        except ValueError:
            messagebox.showerror("Error", "Baudrate must be an integer.")
            return
        try:
            self.ser = serial.Serial(port, baud, timeout=1)
            self.output_text.insert(tk.END, f"Connected to {port} at {baud} baud\n")
            self.stop_thread = False
            self.read_thread = threading.Thread(target=self.read_serial, daemon=True)
            self.read_thread.start()
        except Exception as e:
            messagebox.showerror("Serial Error", str(e))

    def read_serial(self):
        while not self.stop_thread and self.ser and self.ser.is_open:
            try:
                if self.ser.in_waiting > 0:
                    line = self.ser.readline().decode('utf-8', errors='ignore').rstrip()
                    if line:
                        self.output_text.insert(tk.END, line + "\n")
                        self.output_text.see(tk.END)
                time.sleep(0.05)
            except Exception as e:
                self.output_text.insert(tk.END, f"Serial read error: {e}\n")
                break

    def send_read(self):
        if not self.ser or not self.ser.is_open:
            messagebox.showwarning("Warning", "Serial port not connected.")
            return
        action = self.combo_read.get()
        if action == "Time":
            self.ser.write(b"S2201")
            self.ser.write(b"S2201")
            self.output_text.insert(tk.END, "Reading Time\n")
        elif action == "Memory":
            self.ser.write(b"S2202")
            self.ser.write(b"S2202")
            self.output_text.insert(tk.END, "Reading Memory\n")
        elif action == "SW Version":
            self.ser.write(b"S2203")
            self.ser.write(b"S2203")
            self.output_text.insert(tk.END, "Reading SW Version\n")

    def send_write(self):
        if not self.ser or not self.ser.is_open:
            messagebox.showwarning("Warning", "Serial port not connected.")
            return
        action = self.combo_write.get()
        in1 = self.write_in1.get()
        in2 = self.write_in2.get()
        if action == "Hour":
            cmd = f"S2301{in1}{in2}"
            self.ser.write(cmd.encode('utf-8'))
            self.ser.write(cmd.encode('utf-8'))
            self.output_text.insert(tk.END, f"Write Time [{in1}:{in2}]\n")

    def send_reset(self):
        if not self.ser or not self.ser.is_open:
            messagebox.showwarning("Warning", "Serial port not connected.")
            return
        action = self.combo_reset.get()
        if action == "Sensor":
            self.ser.write(b"S1101")
            self.ser.write(b"S1101")
            self.output_text.insert(tk.END, "Reset Sensor...\n")
        elif action == "Memory":
            self.ser.write(b"S1102")
            self.ser.write(b"S1102")
            self.output_text.insert(tk.END, "Reset Memory...\n")

    def send_raw(self):
        if not self.ser or not self.ser.is_open:
            messagebox.showwarning("Warning", "Serial port not connected.")
            return
        cmd = self.raw_entry.get()
        self.ser.write(cmd.encode('utf-8'))
        self.ser.write(cmd.encode('utf-8'))
        self.output_text.insert(tk.END, f"Raw Command Sent: {cmd}\n")

    def run_graph(self):
        try:
            runpy.run_path('GraphicData.py')
        except Exception as e:
            messagebox.showerror("Error", f"Could not run GraphicData.py: {e}")

    def show_info(self):
        messagebox.showinfo("How To Use this GUI",
            "1. How to graph data:\n"
            "   Fill EMIDSS_V_Data.xlsx with the data obtained from\n"
            "   the EMIDSS memory data."
        )

    def on_exit(self):
        self.stop_thread = True
        if self.ser and self.ser.is_open:
            self.ser.close()
        self.root.destroy()

if __name__ == "__main__":
    root = tk.Tk()
    app = SerialGUI(root)
    root.protocol("WM_DELETE_WINDOW", app.on_exit)
    root.mainloop()