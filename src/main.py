import os
import shutil
from tkinter import messagebox, filedialog, Tk, Canvas, Frame, Label
from tkinterdnd2 import DND_FILES, TkinterDnD
from tkinter import ttk

# -------------------------
# Paleta de colores profesional
# -------------------------
COLORS = {
    'primary': '#2563eb',  # Azul profesional
    'primary_hover': '#1d4ed8',
    'secondary': '#64748b',  # Gris azulado
    'background': '#f8fafc',  # Gris muy claro
    'card': '#ffffff',
    'border': '#e2e8f0',
    'border_hover': '#2563eb',
    'text_primary': '#0f172a',
    'text_secondary': '#64748b',
    'success': '#10b981',
    'text_muted': '#94a3b8'
}


# -------------------------
# Funciones Drag & Drop
# -------------------------
def drop_carpeta(event, entry, label, canvas, rect):
    ruta = event.data.strip("{}")
    canvas.itemconfig(rect, outline=COLORS['border'])
    if not os.path.isdir(ruta):
        messagebox.showerror("Error", "Solo se permiten carpetas.")
        return
    entry.config(state="normal")
    entry.delete(0, "end")
    entry.insert(0, ruta)
    entry.config(state="readonly")
    label.config(text=os.path.basename(ruta), foreground=COLORS['text_primary'])


def on_enter_canvas(canvas, rect):
    canvas.itemconfig(rect, outline=COLORS['border_hover'])


def on_leave_canvas(canvas, rect):
    canvas.itemconfig(rect, outline=COLORS['border'])


def on_click(entry, label):
    carpeta = filedialog.askdirectory()
    if carpeta:
        entry.config(state="normal")
        entry.delete(0, "end")
        entry.insert(0, carpeta)
        entry.config(state="readonly")
        label.config(text=os.path.basename(carpeta), foreground=COLORS['text_primary'])


# -------------------------
# Función de copia
# -------------------------
def copiar_archivos_nuevos():
    from datetime import datetime

    base = entry_base.get()
    comparar = entry_comparar.get()
    destino = entry_destino.get()

    if not all(map(os.path.isdir, [base, comparar, destino])):
        messagebox.showerror("Error", "Debes seleccionar todas las carpetas.")
        return

    # Crear nombre de carpeta con formato: NombreComparado_YYYY-MM-DD
    nombre_comparar = os.path.basename(comparar.rstrip(os.sep))
    fecha_actual = datetime.now().strftime("%Y-%m-%d")
    nombre_carpeta_destino = f"{nombre_comparar}_{fecha_actual}"

    # Crear ruta completa de destino
    destino_final = os.path.join(destino, nombre_carpeta_destino)

    # Crear la carpeta de destino
    try:
        os.makedirs(destino_final, exist_ok=True)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo crear la carpeta de destino:\n{str(e)}")
        return

    # Limpiar Treeview y barra de progreso
    for item in tree.get_children():
        tree.delete(item)
    progreso["value"] = 0

    total = sum(len(files) for _, _, files in os.walk(comparar))
    progreso["maximum"] = total

    copiados = 0
    registros = []

    for root_dir, _, files in os.walk(comparar):
        for file in files:
            progreso["value"] += 1
            root.update_idletasks()

            ruta_origen = os.path.join(root_dir, file)
            ruta_relativa = os.path.relpath(ruta_origen, comparar)
            ruta_base = os.path.join(base, ruta_relativa)
            ruta_destino = os.path.join(destino_final, ruta_relativa)

            if not os.path.exists(ruta_base):
                os.makedirs(os.path.dirname(ruta_destino), exist_ok=True)
                if not os.path.exists(ruta_destino):
                    shutil.copy2(ruta_origen, ruta_destino)
                    msg = f"✓ Copiado: {ruta_relativa}"
                    copiados += 1
                else:
                    msg = f"⊘ Ignorado (ya existe en destino): {ruta_relativa}"
            else:
                msg = f"⊘ Ignorado (existe en base): {ruta_relativa}"

            registros.append(msg)
            tree.insert("", "end", values=(msg,))

    log_path = os.path.join(destino_final, "registro_copia.txt")
    with open(log_path, "w", encoding="utf-8") as f:
        f.write("\n".join(registros))

    messagebox.showinfo(
        "Proceso completado",
        f"Archivos copiados: {copiados}\n\nCarpeta creada:\n{destino_final}\n\nRegistro generado en:\n{log_path}"
    )


# -------------------------
# UI principal
# -------------------------
root = TkinterDnD.Tk()
root.title("Comparador de Archivos")
root.geometry("1000x850")
root.configure(bg=COLORS['background'])

try:
    root.iconbitmap("img/icon.ico")
except Exception:
    pass

# -------------------------
# Estilos ttk
# -------------------------
style = ttk.Style()
style.theme_use('clam')

# Configuración de Frame
style.configure("Card.TFrame", background=COLORS['card'])

# Configuración de Labels
style.configure("Title.TLabel",
                background=COLORS['background'],
                foreground=COLORS['text_primary'],
                font=("Segoe UI", 11, "bold"))

style.configure("Subtitle.TLabel",
                background=COLORS['background'],
                foreground=COLORS['text_secondary'],
                font=("Segoe UI", 9))

# Configuración de Entry
style.configure("Custom.TEntry",
                fieldbackground=COLORS['card'],
                background=COLORS['card'],
                foreground=COLORS['text_primary'],
                bordercolor=COLORS['border'],
                lightcolor=COLORS['border'],
                darkcolor=COLORS['border'])

# Configuración de botones
style.configure("Primary.TButton",
                background=COLORS['primary'],
                foreground="white",
                borderwidth=0,
                focuscolor='none',
                font=("Segoe UI", 10, "bold"),
                padding=(20, 12))

style.map("Primary.TButton",
          background=[('active', COLORS['primary_hover']),
                      ('pressed', COLORS['primary_hover'])])

style.configure("Secondary.TButton",
                background=COLORS['card'],
                foreground=COLORS['text_primary'],
                borderwidth=1,
                bordercolor=COLORS['border'],
                focuscolor='none',
                font=("Segoe UI", 9),
                padding=(12, 8))

# Progressbar
style.configure("Custom.Horizontal.TProgressbar",
                background=COLORS['primary'],
                troughcolor=COLORS['border'],
                borderwidth=0,
                lightcolor=COLORS['primary'],
                darkcolor=COLORS['primary'])

# -------------------------
# Header
# -------------------------
header_frame = Frame(root, bg=COLORS['card'], height=80)
header_frame.pack(fill="x", padx=0, pady=0)
header_frame.pack_propagate(False)

header_title = Label(header_frame,
                     text="Comparador de Carpetas",
                     font=("Segoe UI", 20, "bold"),
                     bg=COLORS['card'],
                     fg=COLORS['text_primary'])
header_title.pack(pady=(20, 5))

header_subtitle = Label(header_frame,
                        text="Compara carpetas y copia archivos nuevos automáticamente",
                        font=("Segoe UI", 10),
                        bg=COLORS['card'],
                        fg=COLORS['text_secondary'])
header_subtitle.pack()

# -------------------------
# Container principal
# -------------------------
main_container = Frame(root, bg=COLORS['background'])
main_container.pack(fill="both", expand=True, padx=30, pady=20)

# -------------------------
# Frame para zonas drag & drop HORIZONTAL
# -------------------------
drag_label = ttk.Label(main_container,
                       text="Selecciona las Carpetas",
                       style="Title.TLabel")
drag_label.pack(anchor="w", pady=(0, 10))

frame_drag = Frame(main_container, bg=COLORS['background'])
frame_drag.pack(fill="x", pady=(0, 20))


def crear_zona_drag_drop(parent, titulo, placeholder):
    # Frame contenedor con peso igual
    container = Frame(parent, bg=COLORS['background'])
    container.pack(side="left", fill="both", expand=True, padx=5)

    # Label del título
    titulo_label = Label(container, text=titulo,
                         font=("Segoe UI", 11, "bold"),
                         bg=COLORS['background'],
                         fg=COLORS['text_primary'])
    titulo_label.pack(anchor="w", pady=(0, 8))

    # Canvas para el área de drop
    canvas = Canvas(container, height=120, bg=COLORS['card'],
                    highlightthickness=0, bd=0)
    canvas.pack(fill="both", expand=True)

    # Rectángulo con borde
    rect = canvas.create_rectangle(
        2, 2, 1, 118,
        outline=COLORS['border'],
        dash=(8, 4),
        width=2
    )

    # Label placeholder
    label = Label(canvas,
                  text=placeholder,
                  font=("Segoe UI", 9),
                  fg=COLORS['text_muted'],
                  bg=COLORS['card'],
                  wraplength=400)
    label_window = canvas.create_window(0, 40, window=label)

    # Entry
    entry = ttk.Entry(canvas, font=("Segoe UI", 9),
                      state="readonly", style="Custom.TEntry")
    entry_window = canvas.create_window(0, 85, window=entry, width=0)

    # Ajuste dinámico
    def ajustar_canvas(event):
        ancho = event.width - 4
        canvas.coords(rect, 2, 2, ancho, 118)
        canvas.coords(label_window, ancho / 2, 40)
        canvas.coords(entry_window, ancho / 2, 85)
        canvas.itemconfig(entry_window, width=ancho - 40)

    canvas.bind("<Configure>", ajustar_canvas)

    # Drag & Drop
    canvas.drop_target_register(DND_FILES)
    canvas.dnd_bind("<<Drop>>", lambda e: drop_carpeta(e, entry, label, canvas, rect))

    # Hover - aplicar a todos los elementos
    def enter_handler(e):
        on_enter_canvas(canvas, rect)

    def leave_handler(e):
        on_leave_canvas(canvas, rect)

    canvas.bind("<Enter>", enter_handler)
    canvas.bind("<Leave>", leave_handler)
    label.bind("<Enter>", enter_handler)
    label.bind("<Leave>", leave_handler)
    entry.bind("<Enter>", enter_handler)
    entry.bind("<Leave>", leave_handler)

    # Click
    canvas.bind("<Button-1>", lambda e: on_click(entry, label))
    label.bind("<Button-1>", lambda e: on_click(entry, label))
    entry.bind("<Button-1>", lambda e: on_click(entry, label))

    return entry


# Crear las dos zonas en horizontal
entry_base = crear_zona_drag_drop(
    frame_drag,
    "📁 Carpeta Base",
    "Arrastra aquí o haz clic para seleccionar"
)

entry_comparar = crear_zona_drag_drop(
    frame_drag,
    "📂 Carpeta a Comparar",
    "Arrastra aquí o haz clic para seleccionar"
)

# -------------------------
# Carpeta destino
# -------------------------
frame_destino = Frame(main_container, bg=COLORS['background'])
frame_destino.pack(fill="x", pady=(0, 20))

ttk.Label(frame_destino, text="📥 Carpeta de Destino",
          style="Title.TLabel").pack(anchor="w", pady=(0, 8))

destino_input_frame = Frame(frame_destino, bg=COLORS['card'], bd=1,
                            relief="solid", highlightthickness=0)
destino_input_frame.pack(fill="x")

entry_destino = ttk.Entry(destino_input_frame, font=("Segoe UI", 9),
                          state="readonly", style="Custom.TEntry")
entry_destino.pack(side="left", fill="x", expand=True, padx=10, pady=10)


def seleccionar_destino():
    carpeta = filedialog.askdirectory()
    if carpeta:
        entry_destino.config(state="normal")
        entry_destino.delete(0, "end")
        entry_destino.insert(0, carpeta)
        entry_destino.config(state="readonly")


ttk.Button(destino_input_frame, text="Seleccionar",
           command=seleccionar_destino,
           style="Secondary.TButton").pack(side="right", padx=10, pady=10)

# -------------------------
# Barra de progreso
# -------------------------
progreso_frame = Frame(main_container, bg=COLORS['background'])
progreso_frame.pack(fill="x", pady=(0, 15))

ttk.Label(progreso_frame, text="Progreso",
          style="Subtitle.TLabel").pack(anchor="w", pady=(0, 5))

progreso = ttk.Progressbar(progreso_frame, orient="horizontal",
                           mode="determinate", style="Custom.Horizontal.TProgressbar")
progreso.pack(fill="x", ipady=4)

# -------------------------
# Treeview con scroll
# -------------------------
tree_frame = Frame(main_container, bg=COLORS['background'])
tree_frame.pack(fill="both", expand=True, pady=(0, 15))

ttk.Label(tree_frame, text="Archivos Procesados",
          style="Subtitle.TLabel").pack(anchor="w", pady=(0, 5))

tree_container = Frame(tree_frame, bg=COLORS['card'], bd=1, relief="solid")
tree_container.pack(fill="both", expand=True)

scroll = ttk.Scrollbar(tree_container, orient="vertical")
tree = ttk.Treeview(tree_container, yscrollcommand=scroll.set,
                    selectmode="browse", show="tree headings")
scroll.config(command=tree.yview)

tree.pack(side="left", fill="both", expand=True)
scroll.pack(side="right", fill="y")

# Configurar columna
tree["columns"] = ("Archivo",)
tree.column("#0", width=0, stretch=False)
tree.column("Archivo", anchor="w")
tree.heading("Archivo", text="Estado y Ruta", anchor="w")

# Estilo del Treeview
style.configure("Treeview",
                background=COLORS['card'],
                foreground=COLORS['text_primary'],
                fieldbackground=COLORS['card'],
                borderwidth=0,
                font=("Segoe UI", 9))

style.configure("Treeview.Heading",
                background=COLORS['background'],
                foreground=COLORS['text_primary'],
                borderwidth=0,
                font=("Segoe UI", 10, "bold"))

style.map("Treeview",
          background=[('selected', COLORS['primary'])],
          foreground=[('selected', 'white')])

# -------------------------
# Botón principal
# -------------------------
button_frame = Frame(main_container, bg=COLORS['background'])
button_frame.pack(fill="x")

ttk.Button(
    button_frame,
    text="Comparar y Copiar Archivos Nuevos",
    command=copiar_archivos_nuevos,
    style="Primary.TButton"
).pack(pady=0)

root.mainloop()