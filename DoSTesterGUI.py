import tkinter as tk
from tkinter import font
import sys, signal
import config

def def_handler(sig, frame):
	print("\n\n[!] Saliendo forzadamente...\n")
	sys.exit(1)

signal.signal(signal.SIGINT, def_handler)

main_log_path = config.MAIN_LOG_PATH
main_ban_path = config.MAIN_BAN_PATH
main_server = config.MAIN_SERVER

########################CREACIÓN VENTANA PRINCIPAL########################

root = tk.Tk()
root.title("DoS Tester GUI")
root.geometry("500x500")

fuente_titulo = font.Font(family="Helvetica", size=26, weight="bold")
label_titulo = tk.Label(root, text="Dos Tester", font=fuente_titulo, fg="#6a581c")
label_titulo.place(relx=0.5, y=30, anchor="center")

label_servidor = tk.Label(root, text="Por favor, seleccione el servidor a utilizar:", font="Helvetica 12")
label_servidor.place(relx=0.5, y=100, anchor="center")

########################SELECCIÓN SERVIDOR########################

def seleccionar_servidor(servidor):
	global main_server
	main_server = servidor
	label_servidor.destroy()
	boton_apache.destroy()
	boton_nginx.destroy()
	put_ruta_logs_items(servidor)

boton_apache = tk.Button(root, text="Apache", width=15, height=5, command=lambda: seleccionar_servidor("apache"), bg="#9966cb")
boton_apache.place(x=60, y=220)

boton_nginx = tk.Button(root, text="Nginx", width=15, height=5, command=lambda: seleccionar_servidor("nginx"), bg="#9966cb")
boton_nginx.place(x=280, y=220)

########################SELECCIÓN RUTA LOGS########################

def seleccionar_ruta_logs(campo_entrada):
	global main_log_path
	main_log_path = campo_entrada.get()
	label_pedir_ruta_logs.destroy()
	input_ruta.delete(0, tk.END)
	label_ruta.destroy()
	boton_submit.config(state=tk.DISABLED)
	put_ruta_bans_items()

def put_ruta_logs_items(servidor):
	global boton_submit, input_ruta, label_pedir_ruta_logs, label_ruta
	input_ruta = tk.Entry(root)
	input_ruta.bind("<KeyRelease>", lambda event: verificar_contenido(input_ruta,boton_submit))
	input_ruta.place(relx=0.5, y=300, anchor="center")

	boton_submit = tk.Button(root, text="Enviar", width=15, height=5, state=tk.DISABLED, command=lambda: seleccionar_ruta_logs(input_ruta), bg="#9966cb")
	boton_submit.place(relx=0.5, y=400, anchor="center")
	label_pedir_ruta_logs = tk.Label(root, text="Por favor, introduzca la ruta del archivo de logs:", font="Helvetica 12")
	label_pedir_ruta_logs.place(relx=0.5, y=100, anchor="center")

	if servidor=="apache":
		label_ruta = tk.Label(root, text="Rutas usuales donde se encuentran los logs en Apache2 :\n/var/log/apache2/access.log\n/var/log/apache/access.log\n/var/log/httpd/access.log\n/var/log/httpd/access_log\n/var/log/httpd-access.log", font="Helvetica 12")
		label_ruta.place(relx=0.5, y=200, anchor="center")

	elif servidor=="nginx":
		label_ruta = tk.Label(root, text="Rutas usuales donde se encuentran los logs en Nginx :\n/var/log/nginx/access.log", font="Helvetica 12")
		label_ruta.place(relx=0.5, y=200, anchor="center")

def verificar_contenido(campo_entrada,bot_submit):
	input = campo_entrada.get()
	if input:
		bot_submit.config(state=tk.NORMAL)
	else:
		bot_submit.config(state=tk.DISABLED)

########################SELECCIÓN RUTA BANS########################  MAL

def seleccionar_ruta_bans(campo_entrada):
	global main_ban_path
	main_ban_path = campo_entrada.get()
	label_pedir_ruta_bans.destroy()
	input_ruta.delete(0, tk.END)
	label_ruta_ban.destroy()
	boton_submit.config(state=tk.DISABLED)

def put_ruta_bans_items():
	global label_pedir_ruta_bans,label_ruta_ban, boton_submit
	boton_submit = tk.Button(root, text="Enviar", width=15, height=5, state=tk.DISABLED, command=lambda: seleccionar_ruta_bans(input_ruta), bg="#9966cb")

	label_pedir_ruta_bans = tk.Label(root, text="Por favor, introduzca la ruta del archivo de bans:", font="Helvetica 12")
	label_pedir_ruta_bans.place(relx=0.5, y=100, anchor="center")

	if main_server=="apache":
		label_ruta_ban = tk.Label(root, text="Rutas usuales donde se encuentran los bans en Apache2 :\n/var/www/html/.htaccess", font="Helvetica 12")
		label_ruta_ban.place(relx=0.5, y=200, anchor="center")

	elif main_server=="nginx":
		label_ruta = tk.Label(root, text="Rutas usuales donde se encuentran los bans en Nginx :\n/etc/nginx/sites-available/default", font="Helvetica 12")
		label_ruta.place(relx=0.5, y=200, anchor="center")

########################INTRODUCIR USUARIO TELEGRAM########################


#def put_real_main_items():
	

root.mainloop()