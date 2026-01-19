# main.py
from tkinterdnd2 import TkinterDnD
import ui


def main():
    root = TkinterDnD.Tk()
    root.title("Comparador de Archivos")
    root.geometry("1000x850")
    widgets = ui.construir_ui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
