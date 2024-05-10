import ttkbootstrap as ttk
import tkinter as tk
from ttkbootstrap import font
import sys, signal
import config
import AntiDOSWeb
from threading import *

def defHandler(sig, frame):
	print("\n\n[!] Saliendo forzadamente...\n")
	sys.exit(1)

signal.signal(signal.SIGINT, defHandler)

main_server = config.MAIN_SERVER
main_log_path = config.MAIN_LOG_PATH
main_ban_path = config.MAIN_BAN_PATH
telegram_username = config.TELEGRAM_USERNAME

########################FUNCIONES AUXILIARES########################

#Llamar siempre después de un resize
def centrarVentana(ventana):
    ventana.update_idletasks()
    ancho_ventana = ventana.winfo_width()
    altura_ventana = ventana.winfo_height()
    x_cordinate = int((ventana.winfo_screenwidth() / 2) - (ancho_ventana / 2))
    y_cordinate = int((ventana.winfo_screenheight() / 2) - (altura_ventana / 2))
    ventana.geometry("+{}+{}".format(x_cordinate, y_cordinate))

def verificarContenido(campo_entrada,boton_submit):
	input = campo_entrada.get()
	if input:
		boton_submit.config(state=tk.NORMAL)
	else:
		boton_submit.config(state=tk.DISABLED)

########################CREACIÓN VENTANA PRINCIPAL########################

root = ttk.Window(themename="superhero")
root.title("DoS Tester GUI")
root.geometry("400x180")
root.resizable(width=False, height=False)
centrarVentana(root)


label_titulo = ttk.Label(root, text="DoS Tester", font=("Arial", 30, "bold"))
label_titulo.place(relx=0.5, y=30, anchor="center")

label_servidor = ttk.Label(root, text="Por favor, seleccione el servidor a monitorizar:", font=("Arial", 12))
label_servidor.place(relx=0.5, y=80, anchor="center")

########################SELECCIÓN SERVIDOR########################

def seleccionarServidor(servidor):
	global main_server
	main_server = servidor
	label_servidor.destroy()
	boton_apache.destroy()
	boton_nginx.destroy()
	putLogsItems(servidor)

boton_apache = ttk.Button(root, text="Apache", width=15, command=lambda: seleccionarServidor("apache"))
boton_apache.place(relx=0.3, y=130, anchor="center")

boton_nginx = ttk.Button(root, text="Nginx", width=15, command=lambda: seleccionarServidor("nginx"), style='warning.TButton')
boton_nginx.place(relx=0.7, y=130, anchor="center")

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
	if servidor=="apache":
		root.geometry("600x400")
	elif servidor=="nginx":
		root.geometry("600x300")
	centrarVentana(root)
	global boton_submit_logs, input_logs, label_pedir_logs, label_logs
	input_logs = ttk.Entry(root)
	input_logs.bind("<KeyRelease>", lambda event: verificarContenido(input_logs,boton_submit_logs))
	if servidor=="apache":
		input_logs.place(relx=0.5, y=300, anchor="center")
	elif servidor=="nginx":
		input_logs.place(relx=0.5, y=210, anchor="center")

	boton_submit_logs = ttk.Button(root, text="Enviar", width=15, state=tk.DISABLED, command=lambda: seleccionarRutaLogs(), style='success.TButton')
	if servidor=="apache":
		boton_submit_logs.place(relx=0.5, y=350, anchor="center")
	elif servidor=="nginx":
		boton_submit_logs.place(relx=0.5, y=260, anchor="center")

	label_pedir_logs = ttk.Label(root, text="Por favor, introduzca la ruta del archivo de los logs del servidor.", font="Arial 15")
	label_pedir_logs.place(relx=0.5, y=100, anchor="center")

	##TODO: Permitir seleccionar para copiar las rutas??
	if servidor=="apache":
		label_logs = ttk.Label(root, text="Rutas usuales donde se encuentran los logs en Apache2 :\n/var/log/apache2/access.log\n/var/log/apache/access.log\n/var/log/httpd/access.log\n/var/log/httpd/access_log\n/var/log/httpd-access.log", font="Arial 12")
		label_logs.place(relx=0.5, y=200, anchor="center")

	elif servidor=="nginx":
		label_logs = ttk.Label(root, text="Rutas usuales donde se encuentran los logs en Nginx :\n/var/log/nginx/access.log", font="Arial 12")
		label_logs.place(relx=0.5, y=150, anchor="center")

########################SELECCIÓN RUTA BANS########################  MAL

def seleccionarRutaBans():
	global main_ban_path
	main_ban_path = input_bans.get()
	label_pedir_bans.destroy()
	input_bans.destroy()
	label_bans.destroy()
	boton_submit_bans.destroy()
	putsTelegramItems()


def putBansItems():
	root.geometry("600x300")
	centrarVentana(root)
	global boton_submit_bans, input_bans, label_pedir_bans, label_bans
	input_bans = ttk.Entry(root)
	input_bans.bind("<KeyRelease>", lambda event: verificarContenido(input_bans,boton_submit_bans))
	input_bans.place(relx=0.5, y=200, anchor="center")

	boton_submit_bans = ttk.Button(root, text="Enviar", width=15, state=tk.DISABLED, command=lambda: seleccionarRutaBans(), style='success.TButton')
	boton_submit_bans.place(relx=0.5, y=250, anchor="center")
	label_pedir_bans = ttk.Label(root, text="Por favor, introduzca la ruta del archivo de bans:", font="Arial 12")
	label_pedir_bans.place(relx=0.5, y=100, anchor="center")

	if main_server=="apache":
		label_bans = ttk.Label(root, text="Rutas usuales donde se encuentran los bans en Apache2 :\n/var/www/html/.htaccess", font="Arial 12")
		label_bans.place(relx=0.5, y=150, anchor="center")

	elif main_server=="nginx":
		label_bans = ttk.Label(root, text="Rutas usuales donde se encuentran los bans en Nginx :\n/etc/nginx/sites-available/default", font="Arial 12")
		label_bans.place(relx=0.5, y=150, anchor="center")

########################INTRODUCIÓN USUARIO TELEGRAM########################

def seleccionarTelegramUser():
	global telegram_username
	telegram_username = input_telegram.get()
	input_telegram.destroy()
	boton_submit_telegram.destroy()
	label_pedir_telegram.destroy()
	putMonitorItems()

def putsTelegramItems():
	global input_telegram, boton_submit_telegram, label_pedir_telegram
	input_telegram = ttk.Entry(root)
	input_telegram.bind("<KeyRelease>", lambda event: verificarContenido(input_telegram,boton_submit_telegram))
	input_telegram.place(relx=0.5, y=200, anchor="center")

	boton_submit_telegram = ttk.Button(root, text="Enviar", width=15, state=tk.DISABLED, command=lambda: seleccionarTelegramUser(), style='success.TButton')
	boton_submit_telegram.place(relx=0.5, y=250, anchor="center")
	label_pedir_telegram = ttk.Label(root, text="Por favor, introduzca el usuario de telegram:\n (Debes enviar /start al bot para que funcione)", font="Arial 12")
	label_pedir_telegram.place(relx=0.5, y=100, anchor="center")

########################VENTANA PRINCIPAL PARA MONITORIZAR########################

anti_dos = AntiDOSWeb.AntiDOSWeb(main_server, main_log_path, main_ban_path, "%d/%b/%Y:%H:%M:%S %z", "ip_bans.db", telegram_username)
monitor_thread=Thread()

def putMonitorItems():
	global boton_monitor, boton_parar_monitor
	root.attributes('-zoomed', True)
	#root.geometry("1000x1000")
	boton_monitor = ttk.Button(root, text="Empezar monitorización", width=25, command=threading, style='success.TButton')
	boton_monitor.place(relx=0.33, y=800, anchor="center")

	boton_parar_monitor = ttk.Button(root, text="Parar monitorización", width=25, command=terminarMonitor,state=tk.DISABLED, style='warning.TButton')
	boton_parar_monitor.place(relx=0.66, y=800, anchor="center")

	boton_cerrar = ttk.Button(root, text="Cerrar programa", width=15, command=funcionSalir, style='danger.TButton')
	boton_cerrar.place(relx=0.5, y=900, anchor="center")

def threading(): 
    monitor_thread=Thread(target=comenzarMonitor) 
    monitor_thread.start() 

def comenzarMonitor():
	boton_monitor.config(state=tk.DISABLED)
	boton_parar_monitor.config(state=tk.NORMAL)
	anti_dos.monitor()

def terminarMonitor():
	boton_parar_monitor.config(state=tk.DISABLED)
	boton_monitor.config(state=tk.NORMAL)
	anti_dos.terminarMonitor()

def funcionSalir():
	terminarMonitor()
	print("\n\n[!] Saliendo...\n")
	sys.exit(1)

root.mainloop()