import time
import tkinter as tk
import ttkbootstrap as ttk
from tkinter.scrolledtext import ScrolledText
import sys, signal
import config
import AntiDOSWeb
from threading import *
import GraphPage
from dotenv import load_dotenv, set_key
import os
import customtkinter
import multiprocessing
from pypot.utils import StoppableThread

tiempo_grafica = 60
graph = None
timer = None


def defHandler(sig, frame):
	print("\n\n[!] Saliendo forzadamente...\n")
	sys.exit(1)

signal.signal(signal.SIGINT, defHandler)

first_time = True
graph_thread = None

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
	label_titulo = ttk.Label(root, text="DoS Tester", font="Helvetica 30 bold", style='info.TLabel', foreground='#247ca5')
	label_titulo.place(relx=0.5, y=30, anchor="center")

########################SELECCIÓN SERVIDOR########################

def seleccionarServidor(servidor,go_to_monitor=False):
	global main_server

	main_server = servidor
	set_key(".env", "SERVER", servidor)

	label_servidor.destroy()
	boton_apache.destroy()
	boton_nginx.destroy()

	if go_to_monitor:
		putMonitorItems()
	else:
		putConfigItems()

def putServerItems(go_to_monitor=False):
	global label_servidor, boton_apache, boton_nginx

	root.geometry("400x180")
	centrarVentana(root)

	label_servidor = ttk.Label(root, text="Por favor, seleccione el servidor a monitorizar:", font="Helvetica 12 bold", style='info.TLabel')
	label_servidor.place(relx=0.5, y=80, anchor="center")

	boton_apache = ttk.Button(root, text="Apache", width=15, command=lambda: seleccionarServidor("apache",go_to_monitor))
	boton_apache.place(relx=0.3, y=130, anchor="center")

	boton_nginx = ttk.Button(root, text="Nginx", width=15, command=lambda: seleccionarServidor("nginx",go_to_monitor), style='warning.TButton')
	boton_nginx.place(relx=0.7, y=130, anchor="center")

########################SELECCIÓN RUTA CONFIG########################

def seleccionarRutaConfig(go_to_monitor=False):
	global main_config_path

	main_config_path = combo_box_config.get()
	set_key(".env", "CONFIG_PATH", main_config_path)

	label_pedir_config.destroy()
	boton_submit_config.destroy()
	combo_box_config.destroy()

	if go_to_monitor:
		putMonitorItems()
	else:
		putLogsItems()

def putConfigItems(go_to_monitor=False):
	global combo_box_config, boton_submit_config, label_pedir_config

	root.geometry("600x300")
	centrarVentana(root)

	if main_server=="apache":
		combo_box_config = ttk.Combobox(root, style="TCombobox", values=config.APACHE_CONFIG_PATH,width=50)
	elif main_server=="nginx":
		combo_box_config = ttk.Combobox(root, style="TCombobox", values=config.NGINX_CONFIG_PATH,width=50)

	combo_box_config.current(0)
	combo_box_config.place(relx=0.5, y=160, anchor="center")

	boton_submit_config = ttk.Button(root, text="Enviar", width=15, command=lambda: seleccionarRutaConfig(go_to_monitor), style='success.TButton')
	boton_submit_config.place(relx=0.5, y=250, anchor="center")

	label_pedir_config = ttk.Label(root, text="Por favor, introduzca la ruta del archivo de configuración del servidor:", font="Helvetica 12 bold", style='info.TLabel')
	label_pedir_config.place(relx=0.5, y=100, anchor="center")

########################SELECCIÓN RUTA LOGS########################

def seleccionarRutaLogs(go_to_monitor=False):
	global main_log_path

	main_log_path = combo_box_logs.get()
	set_key(".env", "LOG_PATH", main_log_path)

	label_pedir_logs.destroy()
	boton_submit_logs.destroy()
	combo_box_logs.destroy()

	if go_to_monitor:
		putMonitorItems()
	else:
		putBansItems()

def putLogsItems(go_to_monitor=False):
	global combo_box_logs, boton_submit_logs, label_pedir_logs

	root.geometry("600x300")
	centrarVentana(root)

	if main_server=="apache":
		combo_box_logs = ttk.Combobox(root, style="TCombobox", values=config.APACHE_LOG_PATHS,width=50)
	elif main_server=="nginx":
		combo_box_logs = ttk.Combobox(root, style="TCombobox", values=config.NGINX_LOG_PATHS,width=50)

	combo_box_logs.current(0)
	combo_box_logs.place(relx=0.5, y=160, anchor="center")

	boton_submit_logs = ttk.Button(root, text="Enviar", width=15, command=lambda: seleccionarRutaLogs(go_to_monitor), style='success.TButton')
	boton_submit_logs.place(relx=0.5, y=250, anchor="center")

	label_pedir_logs = ttk.Label(root, text="Por favor, introduzca la ruta del archivo de los logs del servidor:", font="Helvetica 12 bold", style='info.TLabel')
	label_pedir_logs.place(relx=0.5, y=100, anchor="center")

########################SELECCIÓN RUTA BANS########################  MAL

def seleccionarRutaBans(go_to_monitor=False):
	global main_ban_path

	main_ban_path = combo_box_bans.get()
	set_key(".env", "BAN_PATH", main_ban_path)

	label_pedir_bans.destroy()
	boton_submit_bans.destroy()
	combo_box_bans.destroy()

	if go_to_monitor:
		putMonitorItems()
	else:
		putsDatabaseItems()

def putBansItems(go_to_monitor=False):
	global combo_box_bans, boton_submit_bans, label_pedir_bans

	root.geometry("600x300")
	centrarVentana(root)

	if main_server=="apache":
		combo_box_bans = ttk.Combobox(root, style="TCombobox", values=config.APACHE_BAN_PATH,width=50)
	elif main_server=="nginx":
		combo_box_bans = ttk.Combobox(root, style="TCombobox", values=config.NGINX_BAN_PATH,width=50)

	combo_box_bans.current(0)
	combo_box_bans.place(relx=0.5, y=160, anchor="center")

	boton_submit_bans = ttk.Button(root, text="Enviar", width=15, command=lambda: seleccionarRutaBans(go_to_monitor), style='success.TButton')
	boton_submit_bans.place(relx=0.5, y=250, anchor="center")

	label_pedir_bans = ttk.Label(root, text="Por favor, introduzca la ruta del archivo de los bans del servidor:", font="Helvetica 12 bold", style='info.TLabel')
	label_pedir_bans.place(relx=0.5, y=100, anchor="center")

########################INTRODUCIÓN NOMBRE DATABASE########################

def seleccionarNombreDatabase(go_to_monitor=False):
	global data_base_name

	data_base_name = combo_box_database.get()
	set_key(".env", "DATABASE_FILE", data_base_name)

	label_pedir_database.destroy()
	boton_submit_database.destroy()
	combo_box_database.destroy()

	if go_to_monitor:
		putMonitorItems()
	else:
		putsTelegramItems()

def putsDatabaseItems(go_to_monitor=False):
	global combo_box_database, boton_submit_database, label_pedir_database

	root.geometry("600x300")
	centrarVentana(root)

	combo_box_database = ttk.Combobox(root, style="TCombobox", values=config.DATABASE_FILE,width=50)
	combo_box_database.current(0)
	combo_box_database.place(relx=0.5, y=160, anchor="center")

	boton_submit_database = ttk.Button(root, text="Enviar", width=15, command=lambda: seleccionarNombreDatabase(go_to_monitor), style='success.TButton')
	boton_submit_database.place(relx=0.5, y=250, anchor="center")

	label_pedir_database = ttk.Label(root, text="Por favor, introduzca el nombre de la base de datos:", font="Helvetica 12 bold", style='info.TLabel')
	label_pedir_database.place(relx=0.5, y=100, anchor="center")

########################INTRODUCIÓN USUARIO TELEGRAM########################

def seleccionarTelegramUser(muestraAviso=True):
	global telegram_username

	telegram_username = input_telegram.get()
	set_key(".env", "TELEGRAM_USER", telegram_username)

	input_telegram.destroy()
	boton_submit_telegram.destroy()
	label_pedir_telegram.destroy()

	putMonitorItems()

	if muestraAviso:
		putAviso()

def putsTelegramItems(muestraAviso=True):
	global input_telegram, boton_submit_telegram, label_pedir_telegram

	root.geometry("600x300")
	centrarVentana(root)

	input_telegram = ttk.Entry(root, style='info.TEntry')
	input_telegram.bind("<KeyRelease>", lambda event: verificarContenido(input_telegram,boton_submit_telegram))
	input_telegram.place(relx=0.5, y=160, anchor="center")


	boton_submit_telegram = ttk.Button(root, text="Enviar", width=15, state=tk.DISABLED, command=lambda: seleccionarTelegramUser(muestraAviso), style='success.TButton')
	boton_submit_telegram.place(relx=0.5, y=250, anchor="center")

	label_pedir_telegram = ttk.Label(root, text="Por favor, introduzca el usuario de telegram:\n (Debes enviar /start al bot para que funcione)", font="Helvetica 12 bold", style='info.TLabel')
	label_pedir_telegram.place(relx=0.5, y=100, anchor="center")

######################## AVISOS ########################

def putAviso():
	ventana_aviso = tk.Toplevel()
	ventana_aviso.title("Aviso")
	ventana_aviso.geometry("450x150")

	label_aviso = ttk.Label(ventana_aviso, text="Se han guardado los archivos de configuración en .env.\n\nPara modificarlos, selccionelo abajo a la izquierda y \npulsa el botón de modificar.", font="Helvetica 12 bold", style='info.TLabel')
	label_aviso.place(relx=0.5, rely=0.3, anchor="center")

	boton_ok = ttk.Button(ventana_aviso, text="OK", width=12, command=ventana_aviso.destroy, style='success.TButton')
	boton_ok.place(relx=0.5, rely=0.7, anchor="center")

	centrarVentana(ventana_aviso)

######################## VENTANA PRINCIPAL PARA MONITORIZAR ########################
def putMonitorItems():
	global graph_thread, slider_label, root, anti_dos, opciones_parametros, graph, boton_monitor, boton_parar_monitor, boton_cerrar, label_modificar_parametro, boton_modificar_parametro, menu_botones, menu, scrolled_text_baneos

	root.attributes('-zoomed', True)

	scrolled_text_baneos = ScrolledText(root, width=172,  height=10, state='disabled')
	scrolled_text_baneos.place(relx=0.6, y=870, anchor="center")

	anti_dos = AntiDOSWeb.AntiDOSWeb(main_server, main_config_path, main_log_path, main_ban_path, "%d/%b/%Y:%H:%M:%S %z", data_base_name, telegram_username, scrolled_text_baneos)

	print("EJECUTANDO ESTO")
	graph_thread = actualizarGrafica(60)

	root.style.configure('success.TButton', font=('Helvetica', 20))
	root.style.configure('warning.TButton', font=('Helvetica', 20))
	root.style.configure('danger.TButton', font=('Helvetica', 20))
	root.style.configure('info.TButton', font=('Helvetica', 16))
	root.style.configure('TMenubutton', font=('Helvetica', 16))

	boton_monitor = ttk.Button(root, text="Empezar monitorización", width=25, command=threading, style='success.TButton')
	boton_monitor.place(relx=0.12, y=200, anchor="center")

	boton_parar_monitor = ttk.Button(root, text="Parar monitorización", width=25, command=terminarMonitor,state=tk.DISABLED, style='warning.TButton')
	boton_parar_monitor.place(relx=0.12, y=280, anchor="center")

	boton_cerrar = ttk.Button(root, text="Cerrar programa", width=25, command=funcionSalir, style='danger.TButton')
	boton_cerrar.place(relx=0.12, y=360, anchor="center")

	label_modificar_parametro = ttk.Label(root, text="Modificación de parámetros", font="Helvetica 22 bold", style='info.TLabel', foreground='#247ca5')
	label_modificar_parametro.place(relx=0.12, y=775, anchor="center")

	boton_modificar_parametro = ttk.Button(root, text="Modificar", width=15, command=modificarParametro, style='info.Outline.TButton')
	boton_modificar_parametro.place(relx=0.12, y=875, anchor="center")

	menu_botones = ttk.Menubutton(root, text='Seleccione el parámetro', style='info.Outline.TMenubutton')
	menu = tk.Menu(menu_botones)
	menu_botones.config(width=25)
	menu_botones.pack(fill="x", padx=10, pady=10)

	opciones_parametros = tk.StringVar()
	opciones_parametros.trace_add('write', lambda *args: seleccionarParametro())
	for option in ["Server", "Config_path", "Log_path", "Ban_path", "Database_name", "Telegram_user","Todos"]:
		menu.add_radiobutton(label=option, value=option, variable=opciones_parametros)

	menu_botones['menu'] = menu
	menu_botones.place(relx=0.12, y=825, anchor="center")

	# Slider para controlar el numero de segundos a mostrar en la grafica
	slider_label = ttk.Label(root, text="Número de segundos a mostrar: 60", font="Helvetica 14 bold", style='info.TLabel',
							 foreground='#247ca5')
	slider_label.place(relx=0.35, y=725, anchor="center")

	#slider = tk.Scale(root, from_=0, to=100, orient="horizontal", variable=slider_value, length=500, tickinterval=10, troughcolor="#C0C0C0")
	min = 20
	max = 120
	slider = customtkinter.CTkSlider(master=root, from_=min, to=max, width=500, command=cambioSlider, number_of_steps=max - min)
	slider.place(relx=0.6, y=725, anchor="center")


def cambioSlider(value):
	global timer, root, slider_label
	if timer is not None:
		root.after_cancel(timer)
	timer = root.after(250, lambda:actualizarGrafica(value))
	slider_label.config(text=f"Número de segundos a mostrar: {int(value)}")


def actualizarGrafica(tiempo):
	global graph, graph_thread
	tiempo = int(tiempo)
	print(tiempo)

	if not graph:
		graph = GraphPage.GraphPage(root, tiempo, anti_dos)
	else:
		print("SETTINGS TIME: " + str(tiempo))
		graph.setTime(tiempo)
	graph.place(relx=0.6, y=370, anchor="center")
	if not graph_thread:
		graph_thread = threading_graph()
	return graph_thread


def seleccionarParametro():
	"""
	Actualiza el texto que aparece en el menú desplegable para seleccionar el parámetro a modificar
	"""
	parametro_elegido = opciones_parametros.get()
	menu_botones.config(text=parametro_elegido)


def actualizarScrolledTest(texto):
	scrolled_text_baneos.config(state='normal')
	scrolled_text_baneos.insert(tk.END, texto, "mi_color")
	scrolled_text_baneos.config(state='disabled')

def	threading_graph():
	global graph_thread

	if graph_thread:
		print("PARANDO")
		graph_thread.stop()

	if not graph_thread:
		graph_thread = Thread(target=animateGraph)
	graph_thread.start()
	return graph_thread

def animateGraph():
	global graph, anti_dos, root, tiempo_grafica
	if tiempo_grafica:
		tiempo_grafica = int(tiempo_grafica)
	else:
		tiempo_grafica = 60
	graph = GraphPage.GraphPage(root, tiempo_grafica, anti_dos)
	graph.place(relx=0.6, y=370, anchor="center")
	while True:
		graph.animate()
		time.sleep(1)

def threading():
    monitor_thread=Thread(target=comenzarMonitor)
    monitor_thread.start()

def comenzarMonitor():
	scrolled_text_baneos.tag_config("mi_color", foreground="#0dc526", font=("Helvetica", 12, "bold"))
	actualizarScrolledTest("[+] Monitorizando...\n")
	boton_monitor.config(state=tk.DISABLED)
	boton_parar_monitor.config(state=tk.NORMAL)
	anti_dos.monitor()

def terminarMonitor():
	scrolled_text_baneos.tag_config("mi_color", foreground="orange", font=("Helvetica", 12, "bold"))
	actualizarScrolledTest("\n[!] Monitorización detenida\n\n")
	boton_parar_monitor.config(state=tk.DISABLED)
	boton_monitor.config(state=tk.NORMAL)
	anti_dos.terminarMonitor()

def funcionSalir():
	terminarMonitor()
	print("\n\n[!] Saliendo...\n")
	sys.exit(1)

def modificarParametro():

	parametro = opciones_parametros.get()

	if parametro:
		terminarMonitor()
		root.attributes('-zoomed', False)
		graph.destroy()
		boton_monitor.destroy()
		boton_parar_monitor.destroy()
		boton_cerrar.destroy()
		label_modificar_parametro.destroy()
		boton_modificar_parametro.destroy()
		menu_botones.destroy()
		root.style.configure('success.TButton', font=('Helvetica', 12))
		root.style.configure('warning.TButton', font=('Helvetica', 12))
		root.style.configure('danger.TButton', font=('Helvetica', 12))
		root.style.configure('info.TButton', font=('Helvetica', 12))

	if parametro == "Todos":
		putServerItems()
	elif parametro == "Server":
		putServerItems(True)
	elif parametro == "Config_path":
		putConfigItems(True)
	elif parametro == "Log_path":
		putLogsItems(True)
	elif parametro == "Ban_path":
		putBansItems(True)
	elif parametro == "Database_name":
		putsDatabaseItems(True)
	elif parametro == "Telegram_user":
		putsTelegramItems(False)

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