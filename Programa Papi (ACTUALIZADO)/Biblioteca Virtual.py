import csv
import tkinter as tk
from tkinter import ttk, messagebox
import ttkbootstrap as tb

# Función para guardar un libro
def guardar_libro():
    codigo = entry_codigo.get()
    nombre = entry_nombre.get()
    autor = entry_autor.get()
    anio = entry_anio.get()
    genero = entry_genero.get()
    paginas = entry_paginas.get()
    tamano = entry_tamano.get()
    estado = entry_estado.get()
    
    if codigo and nombre and autor and anio and genero and paginas and tamano and estado:
        with open("biblioteca.csv", mode="a", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerow([codigo, nombre, autor, anio, genero, paginas, tamano, estado])
        for entry in entries:
            entry.delete(0, tk.END)
        
        lbl_status.config(text="📖 Libro guardado con éxito!", foreground="green")
        mostrar_libros()
    else:
        lbl_status.config(text="⚠️ Complete todos los campos", foreground="red")

# Función para mostrar los libros en la tabla
def mostrar_libros():
    for row in tree.get_children():
        tree.delete(row)
    try:
        with open("biblioteca.csv", mode="r", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            for fila in lector:
                tree.insert("", "end", values=fila)
    except FileNotFoundError:
        pass

# Función para eliminar un libro seleccionado
def eliminar_libro():
    seleccionado = tree.selection()
    if seleccionado:
        valores = tree.item(seleccionado, "values")
        libros = []
        with open("biblioteca.csv", mode="r", encoding="utf-8") as archivo:
            lector = csv.reader(archivo)
            libros = [fila for fila in lector if fila != list(valores)]
        with open("biblioteca.csv", mode="w", newline="", encoding="utf-8") as archivo:
            escritor = csv.writer(archivo)
            escritor.writerows(libros)
        mostrar_libros()
    else:
        messagebox.showwarning("⚠️ Advertencia", "Seleccione un libro para eliminar")

# Función para limpiar todos los registros
def limpiar_registros():
    confirmacion = messagebox.askyesno("Confirmar", "¿Está seguro de borrar todos los libros?")
    if confirmacion:
        with open("biblioteca.csv", mode="w", newline="", encoding="utf-8") as archivo:
            pass
        mostrar_libros()

# Crear ventana principal
root = tb.Window(themename="darkly")  # Tema oscuro moderno
root.title("📚 Biblioteca Digital")
root.geometry("900x600")
root.configure(bg="#1E1E1E")  # Fondo oscuro

# Marco principal
frame = ttk.Frame(root, padding=20)
frame.pack(fill="both", expand=True)

lbl_titulo = ttk.Label(frame, text="📚 Biblioteca Digital", font=("Helvetica", 18, "bold"), background="#1E1E1E", foreground="white")
lbl_titulo.pack(pady=10)

# Campos de entrada
labels = ["Código", "Nombre", "Autor", "Año", "Género", "Número de Páginas", "Tamaño del Libro", "Estado"]
entries = []
for label in labels:
    ttk.Label(frame, text=label, background="#1E1E1E", foreground="white").pack(anchor="w")
    entry = ttk.Entry(frame)
    entry.pack(fill="x", pady=5)
    entries.append(entry)

entry_codigo, entry_nombre, entry_autor, entry_anio, entry_genero, entry_paginas, entry_tamano, entry_estado = entries

# Botones
btn_frame = ttk.Frame(frame)
btn_frame.pack(pady=10)

btn_guardar = ttk.Button(btn_frame, text="Guardar Libro", command=guardar_libro, bootstyle="success")
btn_guardar.grid(row=0, column=0, padx=5)

btn_eliminar = ttk.Button(btn_frame, text="Eliminar Libro", command=eliminar_libro, bootstyle="danger")
btn_eliminar.grid(row=0, column=1, padx=5)

btn_limpiar = ttk.Button(btn_frame, text="Limpiar Registros", command=limpiar_registros, bootstyle="warning")
btn_limpiar.grid(row=0, column=2, padx=5)

lbl_status = ttk.Label(frame, text="", font=("Helvetica", 10), background="#1E1E1E", foreground="white")
lbl_status.pack()

# Tabla de libros
tree = ttk.Treeview(frame, columns=("Código", "Nombre", "Autor", "Año", "Género", "Número de Páginas", "Tamaño del Libro", "Estado"), show="headings")
for col in ["Código", "Nombre", "Autor", "Año", "Género", "Número de Páginas", "Tamaño del Libro", "Estado"]:
    tree.heading(col, text=col)
    tree.column(col, width=120)
tree.pack(pady=10, fill="both", expand=True)

mostrar_libros()

root.mainloop()
