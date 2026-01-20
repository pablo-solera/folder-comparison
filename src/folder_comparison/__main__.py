# main.py
from tkinterdnd2 import TkinterDnD

from folder_comparison.ui.app import construir_ui


def main():
    root = TkinterDnD.Tk()
    root.title("Comparador de Archivos")
    root.geometry("1000x850")
    construir_ui(root)
    root.mainloop()


if __name__ == "__main__":
    main()
