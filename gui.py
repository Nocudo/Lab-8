import serial
import threading
import tkinter as tk
from tkinter import messagebox

PUERTO = 'COM7'
BAUDIOS = 115200


class ContadorApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Monitor de Sensores Industriales - ESP32")
        self.root.geometry("600x400")
        self.root.configure(bg="#2c3e50")
        self.val_inductivo = tk.StringVar(value="0")
        self.val_foto = tk.StringVar(value="0")
        self.val_capacitivo = tk.StringVar(value="0")
        self.setup_ui()
        self.continuar_leyendo = True
        self.hilo_serial = threading.Thread(
            target=self.lectura_serial, daemon=True)
        self.hilo_serial.start()

    def setup_ui(self):
        titulo = tk.Label(self.root, text="CONTROL DE CONTEO", font=("Arial", 20, "bold"),
                          bg="#2c3e50", fg="white", pady=20)
        titulo.pack()
        frame_tarjetas = tk.Frame(self.root, bg="#2c3e50")
        frame_tarjetas.pack(expand=True, fill="both", padx=20)
        self.crear_tarjeta(frame_tarjetas, "INDUCTIVO\n(Metal)",
                           self.val_inductivo, "#e67e22", 0)
        self.crear_tarjeta(
            frame_tarjetas, "FOTOELECTRICO\n(BMS)", self.val_foto, "#3498db", 1)
        self.crear_tarjeta(frame_tarjetas, "CAPACITIVO\n(Gral)",
                           self.val_capacitivo, "#2ecc71", 2)
        btn_salir = tk.Button(self.root, text="CERRAR SISTEMA", command=self.root.quit,
                              bg="#c0392b", fg="white", font=("Arial", 10, "bold"), pady=10)
        btn_salir.pack(side="bottom", fill="x")

    def crear_tarjeta(self, parent, nombre, variable, color, columna):
        frame = tk.Frame(parent, bg=color, bd=5, relief="flat")
        frame.grid(row=0, column=columna, padx=10, pady=10, sticky="nsew")
        parent.grid_columnconfigure(columna, weight=1)
        tk.Label(frame, text=nombre, font=("Arial", 12, "bold"),
                 bg=color, fg="white").pack(pady=10)
        tk.Label(frame, textvariable=variable, font=(
            "Arial", 40, "bold"), bg=color, fg="white").pack(pady=20)

    def lectura_serial(self):
        try:
            ser = serial.Serial(PUERTO, BAUDIOS, timeout=1)
            ser.reset_input_buffer()
            while self.continuar_leyendo:
                if ser.in_waiting > 0:
                    linea = ser.readline().decode('utf-8', errors='ignore').strip()
                    datos = linea.split(',')
                    if len(datos) == 3:
                        self.val_inductivo.set(datos[0])
                        self.val_foto.set(datos[1])
                        self.val_capacitivo.set(datos[2])
        except Exception as e:
            print(f"Error Serial: {e}")
            self.root.after(0, lambda: messagebox.showerror(
                "Error", f"No se pudo conectar al puerto {PUERTO}"))


if __name__ == "__main__":
    root = tk.Tk()
    app = ContadorApp(root)
    root.mainloop()
