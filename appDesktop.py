import tkinter as tk
from tkinter import ttk, messagebox
import requests
from datetime import datetime
import socket

# URL base de la API MockAPI
BASE_URL = "https://66eb02a355ad32cda47b545d.mockapi.io/IoTCarStatus"


# Función para obtener la IP local
def get_local_ip():
    try:
        return socket.gethostbyname(socket.gethostname())
    except:
        return '127.0.0.1'  # IP local por defecto en caso de error


# Función para inyectar un registro a MockAPI
def inject_record(status):
    data = {
        "status": status,
        "date": datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
        "ipClient": get_local_ip()
    }

    try:
        response = requests.post(BASE_URL, json=data)
        if response.status_code == 201:
            update_logs()
            messagebox.showinfo("Éxito", f"Registro inyectado: {data}")
        else:
            messagebox.showerror("Error", "No se pudo inyectar el registro.")
    except Exception as e:
        messagebox.showerror("Error", f"Error en la solicitud: {e}")


# Función para actualizar el área de registros
def update_logs():
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            logs_text.delete('1.0', tk.END)  # Limpiar el área de texto
            records = response.json()
            for record in records:
                logs_text.insert(tk.END,
                                 f"ID: {record['id']} | Status: {record['status']} | Date: {record['date']} | IP: {record['ipClient']}\n")
        else:
            logs_text.insert(tk.END, "Error al obtener registros.")
    except Exception as e:
        logs_text.insert(tk.END, f"Error en la solicitud: {e}")


# Crear la ventana principal
root = tk.Tk()
root.title("Control de Carro IoT")
root.geometry("600x500")

# Crear el marco para los botones
buttons_frame = tk.Frame(root)
buttons_frame.pack(pady=20)

# Organizar los botones en forma de cruz
btn_forward = ttk.Button(buttons_frame, text="Adelante", command=lambda: inject_record("Adelante"))
btn_forward.grid(row=0, column=1, padx=5, pady=5)  # Posición superior

btn_backward = ttk.Button(buttons_frame, text="Atrás", command=lambda: inject_record("Atrás"))
btn_backward.grid(row=2, column=1, padx=5, pady=5)  # Posición inferior

btn_left = ttk.Button(buttons_frame, text="Izquierda", command=lambda: inject_record("Izquierda"))
btn_left.grid(row=1, column=0, padx=5, pady=5)  # Posición izquierda

btn_stop = ttk.Button(buttons_frame, text="Alto", command=lambda: inject_record("Alto"))
btn_stop.grid(row=1, column=1, padx=5, pady=5)  # Posición centro

btn_right = ttk.Button(buttons_frame, text="Derecha", command=lambda: inject_record("Derecha"))
btn_right.grid(row=1, column=2, padx=5, pady=5)  # Posición derecha

# Área de texto para mostrar los registros inyectados
logs_frame = tk.LabelFrame(root, text="Registros inyectados", padx=10, pady=10)
logs_frame.pack(fill="both", expand="yes", padx=20, pady=20)

logs_text = tk.Text(logs_frame, height=10, wrap="word")
logs_text.pack(fill="both", expand="yes")

# Actualizar los registros al iniciar la aplicación
update_logs()

# Ejecutar la ventana principal
root.mainloop()
