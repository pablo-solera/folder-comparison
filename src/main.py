# main.py
from tkinterdnd2 import TkinterDnD
import tkinter as tk
import ui

def main():
    root = TkinterDnD.Tk()
    root.title("Comparador de Archivos")
    root.geometry("1000x850")
    root.iconphoto(True,tk.PhotoImage(file="../img/icon.png"))
    widgets = ui.construir_ui(root)
    root.mainloop()

if __name__ == "__main__":
    main()
