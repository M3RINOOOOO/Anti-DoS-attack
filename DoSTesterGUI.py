import tkinter as tk
from tkinter import font
import sys, signal
import config
import AntiDOSWeb
from time import sleep
import threading

def defHandler(sig, frame):
	print("\n\n[!] Saliendo forzadamente...\n")
	sys.exit(1)

signal.signal(signal.SIGINT, defHandler)

main_server = config.MAIN_SERVER
main_log_path = config.MAIN_LOG_PATH
main_ban_path = config.MAIN_BAN_PATH


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

def seleccionarServidor(servidor):
	global main_server
	main_server = servidor
	label_servidor.destroy()
	boton_apache.destroy()
	boton_nginx.destroy()
	putLogsItems(servidor)

boton_apache = tk.Button(root, text="Apache", width=15, height=5, command=lambda: seleccionarServidor("apache"), bg="#9966cb")
boton_apache.place(x=60, y=220)

boton_nginx = tk.Button(root, text="Nginx", width=15, height=5, command=lambda: seleccionarServidor("nginx"), bg="#9966cb")
boton_nginx.place(x=280, y=220)

########################SELECCIÓN RUTA LOGS########################

def seleccionarRutaLogs():
	global main_log_path
	main_log_path = input_logs.get()
	label_pedir_logs.destroy()
	input_logs.destroy()
	label_logs.destroy()
	boton_submit_logs.destroy()
	putBansItems()

def putLogsItems(servidor):
	global boton_submit_logs, input_logs, label_pedir_logs, label_logs
	input_logs = tk.Entry(root)
	input_logs.bind("<KeyRelease>", lambda event: verificarContenido(input_logs,boton_submit_logs))
	input_logs.place(relx=0.5, y=300, anchor="center")

	boton_submit_logs = tk.Button(root, text="Enviar", width=15, height=5, state=tk.DISABLED, command=lambda: seleccionarRutaLogs(), bg="#9966cb")
	boton_submit_logs.place(relx=0.5, y=400, anchor="center")
	label_pedir_logs = tk.Label(root, text="Por favor, introduzca la ruta del archivo de logs:", font="Helvetica 12")
	label_pedir_logs.place(relx=0.5, y=100, anchor="center")

	if servidor=="apache":
		label_logs = tk.Label(root, text="Rutas usuales donde se encuentran los logs en Apache2 :\n/var/log/apache2/access.log\n/var/log/apache/access.log\n/var/log/httpd/access.log\n/var/log/httpd/access_log\n/var/log/httpd-access.log", font="Helvetica 12")
		label_logs.place(relx=0.5, y=200, anchor="center")

	elif servidor=="nginx":
		label_logs = tk.Label(root, text="Rutas usuales donde se encuentran los logs en Nginx :\n/var/log/nginx/access.log", font="Helvetica 12")
		label_logs.place(relx=0.5, y=200, anchor="center")

def verificarContenido(campo_entrada,bot_submit):
	input = campo_entrada.get()
	if input:
		bot_submit.config(state=tk.NORMAL)
	else:
		bot_submit.config(state=tk.DISABLED)

########################SELECCIÓN RUTA BANS########################  MAL

def seleccionarRutaBans():
	global main_ban_path
	main_ban_path = input_bans.get()
	label_pedir_bans.destroy()
	input_bans.destroy()
	label_bans.destroy()
	boton_submit_bans.destroy()
	print(main_server, main_log_path, main_ban_path)
	putMonitorItems()


def putBansItems():
	global boton_submit_bans, input_bans, label_pedir_bans, label_bans
	input_bans = tk.Entry(root)
	input_bans.bind("<KeyRelease>", lambda event: verificarContenido(input_bans,boton_submit_bans))
	input_bans.place(relx=0.5, y=300, anchor="center")

	boton_submit_bans = tk.Button(root, text="Enviar", width=15, height=5, state=tk.DISABLED, command=lambda: seleccionarRutaBans(), bg="#9966cb")
	boton_submit_bans.place(relx=0.5, y=400, anchor="center")
	label_pedir_bans = tk.Label(root, text="Por favor, introduzca la ruta del archivo de bans:", font="Helvetica 12")
	label_pedir_bans.place(relx=0.5, y=100, anchor="center")

	if main_server=="apache":
		label_bans = tk.Label(root, text="Rutas usuales donde se encuentran los bans en Apache2 :\n/var/www/html/.htaccess", font="Helvetica 12")
		label_bans.place(relx=0.5, y=200, anchor="center")

	elif main_server=="nginx":
		label_bans = tk.Label(root, text="Rutas usuales donde se encuentran los bans en Nginx :\n/etc/nginx/sites-available/default", font="Helvetica 12")
		label_bans.place(relx=0.5, y=200, anchor="center")

########################VENTANA PRINCIPAL PARA MONITORIZAR########################

def putMonitorItems():
	root.attributes("-fullscreen", True)
	boton_monitor = tk.Button(root, text="Empezar monitorización", width=25, height=5, command=comenzarMonitor, bg="#45f74a")
	boton_monitor.place(relx=0.33, y=800, anchor="center")

	boton_parar_monitor = tk.Button(root, text="Para monitorización", width=25, height=5, command=comenzarMonitor, bg="#45f74a")
	boton_parar_monitor.place(relx=0.66, y=800, anchor="center")

	boton_cerrar = tk.Button(root, text="Cerrar programa", width=15, height=5, command=funcionSalir, bg="#FF0000")
	boton_cerrar.place(relx=0.5, y=900, anchor="center")


def comenzarMonitor():
	global monitor_process
	anti_dos = AntiDOSWeb.AntiDOSWeb(main_server, main_log_path, main_ban_path, "%d/%b/%Y:%H:%M:%S %z", "ip_bans.db")
	monitor_process = threading.Thread(target=anti_dos.monitor())
	monitor_process.start()


def funcionSalir():
    print("\n\n[!] Saliendo...\n")
    sys.exit(1)	

root.mainloop()