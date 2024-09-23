import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd
import requests

# URL base de la API MockAPI
BASE_URL = "https://66eb02a355ad32cda47b545d.mockapi.io/IoTCarStatus"


# Función para obtener los últimos 10 registros desde MockAPI
def get_last_10_records():
    try:
        response = requests.get(BASE_URL)
        if response.status_code == 200:
            data = response.json()
            # Convertir los datos en un DataFrame de pandas
            df = pd.DataFrame(data)
            # Ordenar por fecha y obtener los últimos 10 registros
            df['date'] = pd.to_datetime(df['date'])
            last_10_records = df.sort_values(by='date', ascending=False).head(10)
            return last_10_records
        else:
            messagebox.showerror("Error", "No se pudo obtener los registros.")
            return None
    except Exception as e:
        messagebox.showerror("Error", f"Error en la solicitud: {e}")
        return None


# Función para mostrar los últimos 10 registros en la interfaz
def display_last_10_records():
    records = get_last_10_records()
    if records is not None:
        # Limpiar la tabla anterior
        for row in records_table.get_children():
            records_table.delete(row)

        # Insertar los nuevos registros en la tabla
        for index, row in records.iterrows():
            records_table.insert("", tk.END, values=(row['id'], row['status'], row['date'], row['ipClient']))


# Crear la ventana principal
root = tk.Tk()
root.title("Visualización de Registros IoT")
root.geometry("800x400")

# Crear un marco para la tabla
table_frame = tk.Frame(root)
table_frame.pack(pady=20)

# Crear la tabla utilizando Treeview
columns = ("ID", "Status", "Date", "IP Client")
records_table = ttk.Treeview(table_frame, columns=columns, show="headings")

# Definir los encabezados de la tabla
for col in columns:
    records_table.heading(col, text=col)
    records_table.column(col, width=150, anchor="center")

records_table.pack(fill="both", expand=True)

# Botón para actualizar la vista con los últimos 10 registros
btn_refresh = ttk.Button(root, text="Actualizar Registros", command=display_last_10_records)
btn_refresh.pack(pady=10)

# Cargar los registros al iniciar la aplicación
display_last_10_records()

# Ejecutar la ventana principal
root.mainloop()
