import tkinter as tk
import ttkbootstrap as ttk
import sys, signal
import config
import AntiDOSWeb
from threading import *
import GraphPage
from dotenv import load_dotenv, set_key
import os

def defHandler(sig, frame):
	print("\n\n[!] Saliendo forzadamente...\n")
	sys.exit(1)

signal.signal(signal.SIGINT, defHandler)

first_time = True

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
def crearVentanaPrincipal():
	global root
	root = ttk.Window(themename="superhero")
	root.title("DoS Tester GUI")
	imagen_icono = tk.PhotoImage(file="images/kaki.png")
	root.iconphoto(True, imagen_icono)
	label_titulo = ttk.Label(root, text="DoS Tester", font=("Arial", 30, "bold"))
	label_titulo.place(relx=0.5, y=30, anchor="center")

########################SELECCIÓN SERVIDOR########################

def seleccionarServidor(servidor):
	global main_server
	main_server = servidor
	set_key(".env", "SERVER", servidor)
	label_servidor.destroy()
	boton_apache.destroy()
	boton_nginx.destroy()
	if servidor=="apache":
		putConfigItems()
	elif servidor=="nginx":
		set_key(".env", "SERVER", config.NGINX_BAN_PATH)
		putLogsItems()

def putServerItems():
	global boton_submit_server, input_server, label_server, label_servidor, boton_apache, boton_nginx

	root.geometry("400x180")
	centrarVentana(root)
	
	label_servidor = ttk.Label(root, text="Por favor, seleccione el servidor a monitorizar:", font=("Arial", 12))
	label_servidor.place(relx=0.5, y=80, anchor="center")

	boton_apache = ttk.Button(root, text="Apache", width=15, command=lambda: seleccionarServidor("apache"))
	boton_apache.place(relx=0.3, y=130, anchor="center")

	boton_nginx = ttk.Button(root, text="Nginx", width=15, command=lambda: seleccionarServidor("nginx"), style='warning.TButton')
	boton_nginx.place(relx=0.7, y=130, anchor="center")

########################SELECCIÓN RUTA CONFIG########################

def seleccionarRutaConfig(go_to_monitor=False):
	global main_config_path
	main_config_path = input_config.get()
	set_key(".env", "CONFIG_PATH", main_config_path)
	label_pedir_config.destroy()
	input_config.destroy()
	label_config.destroy()
	boton_submit_config.destroy()

	if go_to_monitor:
		putMonitorItems()
	else:
		putLogsItems()

def putConfigItems(go_to_monitor=False):
	root.geometry("600x300")
	centrarVentana(root)

	global boton_submit_config, input_config, label_pedir_config, label_config
	input_config = ttk.Entry(root, style='info.TEntry')
	input_config.bind("<KeyRelease>", lambda event: verificarContenido(input_config,boton_submit_config))
	input_config.place(relx=0.5, y=200, anchor="center")

	boton_submit_config = ttk.Button(root, text="Enviar", width=15, state=tk.DISABLED, command=lambda: seleccionarRutaConfig(go_to_monitor), style='success.TButton')
	boton_submit_config.place(relx=0.5, y=250, anchor="center")
	label_pedir_config = ttk.Label(root, text="Por favor, introduzca la ruta del archivo de configuración del servidor:", font="Arial 12")
	label_pedir_config.place(relx=0.5, y=100, anchor="center")

	if main_server=="apache":
		label_config = ttk.Label(root, text="Rutas usuales donde se encuentran los archivos de configuración en Apache2 :\n/etc/apache2/apache2.conf", font="Arial 12")
		label_config.place(relx=0.5, y=150, anchor="center")

########################SELECCIÓN RUTA LOGS########################

def seleccionarRutaLogs(go_to_monitor=False):
	global main_log_path
	main_log_path = input_logs.get()
	set_key(".env", "LOG_PATH", main_log_path)
	label_pedir_logs.destroy()
	input_logs.destroy()
	label_logs.destroy()
	boton_submit_logs.destroy()
	if go_to_monitor:
		putMonitorItems()
	else:
		putBansItems()

def putLogsItems(go_to_monitor=False):
	if main_server=="apache":
		root.geometry("600x400")
	elif main_server=="nginx":
		root.geometry("600x300")

	centrarVentana(root)

	global boton_submit_logs, input_logs, label_pedir_logs, label_logs
	input_logs = ttk.Entry(root, style='info.TEntry')
	input_logs.bind("<KeyRelease>", lambda event: verificarContenido(input_logs,boton_submit_logs))

	if main_server=="apache":
		input_logs.place(relx=0.5, y=300, anchor="center")
	elif main_server=="nginx":
		input_logs.place(relx=0.5, y=210, anchor="center")

	boton_submit_logs = ttk.Button(root, text="Enviar", width=15, state=tk.DISABLED, command=lambda: seleccionarRutaLogs(go_to_monitor), style='success.TButton')
	
	if main_server=="apache":
		boton_submit_logs.place(relx=0.5, y=350, anchor="center")
	elif main_server=="nginx":
		boton_submit_logs.place(relx=0.5, y=260, anchor="center")

	label_pedir_logs = ttk.Label(root, text="Por favor, introduzca la ruta del archivo de los logs del servidor.", font="Arial 15")
	label_pedir_logs.place(relx=0.5, y=100, anchor="center")

	##TODO: Permitir seleccionar para copiar las rutas??
	if main_server=="apache":
		label_logs = ttk.Label(root, text="Rutas usuales donde se encuentran los logs en Apache2 :\n/var/log/apache2/access.log\n/var/log/apache/access.log\n/var/log/httpd/access.log\n/var/log/httpd/access_log\n/var/log/httpd-access.log", font="Arial 12")
		label_logs.place(relx=0.5, y=200, anchor="center")

	elif main_server=="nginx":
		label_logs = ttk.Label(root, text="Rutas usuales donde se encuentran los logs en Nginx :\n/var/log/nginx/access.log", font="Arial 12")
		label_logs.place(relx=0.5, y=150, anchor="center")

########################SELECCIÓN RUTA BANS########################  MAL

def seleccionarRutaBans(go_to_monitor=False):
	global main_ban_path
	main_ban_path = input_bans.get()
	set_key(".env", "BAN_PATH", main_ban_path)
	label_pedir_bans.destroy()
	input_bans.destroy()
	label_bans.destroy()
	boton_submit_bans.destroy()
	if go_to_monitor:
		putMonitorItems()
	else:
		putsDatabaseItems()

def putBansItems(go_to_monitor=False):
	root.geometry("600x300")
	centrarVentana(root)
	global boton_submit_bans, input_bans, label_pedir_bans, label_bans
	input_bans = ttk.Entry(root, style='info.TEntry')
	input_bans.bind("<KeyRelease>", lambda event: verificarContenido(input_bans,boton_submit_bans))
	input_bans.place(relx=0.5, y=200, anchor="center")

	boton_submit_bans = ttk.Button(root, text="Enviar", width=15, state=tk.DISABLED, command=lambda: seleccionarRutaBans(go_to_monitor), style='success.TButton')
	boton_submit_bans.place(relx=0.5, y=250, anchor="center")
	label_pedir_bans = ttk.Label(root, text="Por favor, introduzca la ruta del archivo de bans:", font="Arial 12")
	label_pedir_bans.place(relx=0.5, y=100, anchor="center")

	if main_server=="apache":
		label_bans = ttk.Label(root, text="Rutas usuales donde se encuentran los bans en Apache2 :\n/var/www/html/.htaccess", font="Arial 12")
		label_bans.place(relx=0.5, y=150, anchor="center")

	elif main_server=="nginx":
		label_bans = ttk.Label(root, text="Rutas usuales donde se encuentran los bans en Nginx :\n/etc/nginx/sites-available/default", font="Arial 12")
		label_bans.place(relx=0.5, y=150, anchor="center")

########################INTRODUCIÓN NOMBRE DATABASE########################

def seleccionarNombreDatabase(go_to_monitor=False):
	global data_base_name
	data_base_name = input_database.get()
	set_key(".env", "DATABASE_FILE", data_base_name)
	label_pedir_database.destroy()
	input_database.destroy()
	label_database.destroy()
	boton_submit_database.destroy()
	if go_to_monitor:
		putMonitorItems()
	else:
		putsTelegramItems()			

def putsDatabaseItems(go_to_monitor=False):		
	root.geometry("600x300")
	centrarVentana(root)
	global boton_submit_database, input_database, label_pedir_database, label_database
	input_database = ttk.Entry(root, style='info.TEntry')
	input_database.bind("<KeyRelease>", lambda event: verificarContenido(input_database,boton_submit_database))
	input_database.place(relx=0.5, y=200, anchor="center")

	boton_submit_database = ttk.Button(root, text="Enviar", width=15, state=tk.DISABLED, command=lambda: seleccionarNombreDatabase(go_to_monitor), style='success.TButton')
	boton_submit_database.place(relx=0.5, y=250, anchor="center")
	label_pedir_database = ttk.Label(root, text="Por favor, introduzca el nombre de la base de datos:", font="Arial 12")
	label_pedir_database.place(relx=0.5, y=100, anchor="center")

	label_database = ttk.Label(root, text="Por defecto: ip_bans.db", font="Arial 12")
	label_database.place(relx=0.5, y=150, anchor="center")

########################INTRODUCIÓN USUARIO TELEGRAM########################

def seleccionarTelegramUser():
	global telegram_username
	telegram_username = input_telegram.get()
	set_key(".env", "TELEGRAM_USER", telegram_username)
	input_telegram.destroy()
	boton_submit_telegram.destroy()
	label_pedir_telegram.destroy()
	putMonitorItems()

def putsTelegramItems():
	global input_telegram, boton_submit_telegram, label_pedir_telegram
	input_telegram = ttk.Entry(root, style='info.TEntry')
	input_telegram.bind("<KeyRelease>", lambda event: verificarContenido(input_telegram,boton_submit_telegram))
	input_telegram.place(relx=0.5, y=200, anchor="center")

	boton_submit_telegram = ttk.Button(root, text="Enviar", width=15, state=tk.DISABLED, command=lambda: seleccionarTelegramUser(), style='success.TButton')
	boton_submit_telegram.place(relx=0.5, y=250, anchor="center")
	label_pedir_telegram = ttk.Label(root, text="Por favor, introduzca el usuario de telegram:\n (Debes enviar /start al bot para que funcione)", font="Arial 12")
	label_pedir_telegram.place(relx=0.5, y=100, anchor="center")

########################VENTANA PRINCIPAL PARA MONITORIZAR########################
def putMonitorItems():
	global anti_dos, opciones_parametros, graph, boton_monitor, boton_parar_monitor, boton_cerrar, label_modificar_parametro, boton_modificar_parametro, menu_botones, menu
	root.style.configure('success.TButton', font=('Helvetica', 20))
	root.style.configure('warning.TButton', font=('Helvetica', 20))
	root.style.configure('danger.TButton', font=('Helvetica', 20))
	root.style.configure('info.TButton', font=('Helvetica', 16))
	root.style.configure('TMenubutton', font=('Helvetica', 16))
	
	root.attributes('-zoomed', True)
	anti_dos = AntiDOSWeb.AntiDOSWeb(main_server, main_config_path, main_log_path, main_ban_path, "%d/%b/%Y:%H:%M:%S %z", data_base_name, telegram_username)

	graph = GraphPage.GraphPage(root, 60, anti_dos)
	graph.place(relx=0.6, y=420, anchor="center")
	graph.animate()

	boton_monitor = ttk.Button(root, text="Empezar monitorización", width=25, command=threading, style='success.TButton')
	boton_monitor.place(relx=0.12, y=200, anchor="center")

	boton_parar_monitor = ttk.Button(root, text="Parar monitorización", width=25, command=terminarMonitor,state=tk.DISABLED, style='warning.TButton')
	boton_parar_monitor.place(relx=0.12, y=280, anchor="center")

	boton_cerrar = ttk.Button(root, text="Cerrar programa", width=25, command=funcionSalir, style='danger.TButton')
	boton_cerrar.place(relx=0.12, y=360, anchor="center")

	label_modificar_parametro = ttk.Label(root, text="Modificación de parámetros", font="Helvetica 25", style='info.Inverse.TLabel', foreground='#2C647E')
	label_modificar_parametro.place(relx=0.12, y=650, anchor="center")

	boton_modificar_parametro = ttk.Button(root, text="Modificar", width=15, command=modificarParametro, style='info.TButton')
	boton_modificar_parametro.place(relx=0.12, y=749, anchor="center")

	#Menu desplegable con opciones para modificar
	menu_botones = ttk.Menubutton(root, text='Seleccione el parámetro', style='info.Outline.TMenubutton')
	menu = tk.Menu(menu_botones)

	opciones_parametros = tk.StringVar()
	for option in ["Server", "Config_path", "Log_path", "Ban_path", "Database_name", "Telegram_user"]:
		menu.add_radiobutton(label=option, value=option, variable=opciones_parametros)

	menu_botones['menu'] = menu
	menu_botones.place(relx=0.12, y=700, anchor="center")

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

def modificarParametro():
	root.attributes('-zoomed', False)
	graph.destroy()
	boton_monitor.destroy()
	boton_parar_monitor.destroy()
	boton_cerrar.destroy()
	label_modificar_parametro.destroy()
	boton_modificar_parametro.destroy()
	menu_botones.destroy()


	parametro = opciones_parametros.get()
	if parametro == "Server":
		putServerItems()
	elif parametro == "Config_path":
		putConfigItems(True)
	elif parametro == "Log_path":
		putLogsItems(True)
	elif parametro == "Ban_path":
		putBansItems(True)
	elif parametro == "Database_name":
		putsDatabaseItems(True)
	elif parametro == "Telegram_user":
		putsTelegramItems()

########################MAIN########################

if __name__ == "__main__":

	if os.path.isfile('.env'):
		first_time = False
		load_dotenv()
		main_server = os.getenv("SERVER")
		main_config_path = os.getenv("CONFIG_PATH")
		main_log_path = os.getenv("LOG_PATH")
		main_ban_path = os.getenv("BAN_PATH")
		data_base_name = os.getenv("DATABASE_FILE")
		telegram_username = os.getenv("TELEGRAM_USER")

	crearVentanaPrincipal()

	if first_time:
		putServerItems()
	else :
		putMonitorItems()

	root.mainloop()