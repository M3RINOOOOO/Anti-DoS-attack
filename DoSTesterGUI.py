import tkinter as tk
from tkinter import font
import sys, signal

def def_handler(sig, frame):
	print("\n\n[!] Saliendo forzadamente...\n")
	sys.exit(1)

signal.signal(signal.SIGINT, def_handler)


########################---VENTANA PRINCIPAL---########################

root = tk.Tk()
root.title("DoS Tester GUI")
root.geometry("1000x1000")

fuente_titulo = font.Font(family="Helvetica", size=26, weight="bold")
titulo = tk.Label(root, text="Dos Tester", font=fuente_titulo, fg="#6a581c")
titulo.place(relx=0.5, y=30, anchor="center")


root.mainloop()