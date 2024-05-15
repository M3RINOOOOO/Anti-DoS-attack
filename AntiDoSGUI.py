#!/usr/bin/env python3

"""
Este script implementa una interfaz gráfica de usuario (GUI) para el monitoreo y la configuración de un sistema Anti-DOS.
"""

import time
import ttkbootstrap as ttk
from tkinter.scrolledtext import ScrolledText
import sys, signal

import ttkbootstrap.dialogs.colorchooser

import config
import AntiDOSWeb
from threading import *
import GraphPage
from dotenv import load_dotenv, set_key
import os
import customtkinter
import subprocess

tiempo_grafica = 60
timer = None
min = 20
max = 120
kaki = None
colors = None
anti_dos = None

def defHandler(sig, frame):
    """
        Manejador de la señal SIGINT (Ctrl+C) para salir del programa.

        Args:
            sig (int): Número de la señal recibida.
            frame (frame): Marco de la señal.

        Returns:
            None
    """
    print("\n\n[!] Saliendo forzadamente...\n")
    sys.exit(1)


signal.signal(signal.SIGINT, defHandler)

first_time = True
graph_thread = None

########################FUNCIONES AUXILIARES########################


# Llamar siempre después de un resize
def centrarVentana(ventana):
    """
        Centra una ventana en la pantalla.

        Args:
            ventana: La ventana a centrar.

        Returns:
            None
    """
    ventana.update_idletasks()
    ancho_ventana = ventana.winfo_width()
    altura_ventana = ventana.winfo_height()
    x_cordinate = int((ventana.winfo_screenwidth() / 2) - (ancho_ventana / 2))
    y_cordinate = int((ventana.winfo_screenheight() / 2) -
                      (altura_ventana / 2))
    ventana.geometry("+{}+{}".format(x_cordinate, y_cordinate))


def verificarContenido(campo_entrada, boton_submit):
    """
        Verifica si hay contenido en un campo de entrada y actualiza el estado de un botón.

        Args:
            campo_entrada: El campo de entrada a verificar.
            boton_submit: El botón cuyo estado se actualizará.

        Returns:
            None
    """
    input = campo_entrada.get()
    if input:
        boton_submit.config(text="Enviar", style='success.TButton', state=ttk.NORMAL)
    else:
        boton_submit.config(text="Saltar", style='danger.TButton', state=ttk.NORMAL)


########################CREACIÓN VENTANA PRINCIPAL########################
def crearVentanaPrincipal():
    """
        Crea la ventana principal de la aplicación.

        Returns:
            None
    """
    global root, label_titulo
    root = ttk.Window(themename="superhero")
    root.protocol("WM_DELETE_WINDOW", onClosing)
    root.title("Anti-DOS")
    imagen_icono = ttk.PhotoImage(file="images/kaki.png")
    root.iconphoto(True, imagen_icono)
    label_titulo = ttk.Label(root,
                             text="Anti-DOS",
                             font="Helvetica 30 bold",
                             style='info.TLabel',
                             foreground='#247ca5')
    label_titulo.place(relx=0.5, y=int(root.winfo_screenheight()/50), anchor="center")


########################SELECCIÓN SERVIDOR########################


def seleccionarServidor(servidor, go_to_monitor=False):
    """
        Selecciona el servidor a monitorizar y muestra la siguiente pantalla.

        Args:
            servidor (str): El servidor seleccionado (APACHE o NGINX).
            go_to_monitor (bool): Indica si se debe ir directamente a la pantalla de monitoreo.

        Returns:
            None
    """
    global main_server

    main_server = servidor
    set_key(".env", "SERVER", servidor)

    label_servidor.destroy()
    boton_apache.destroy()
    boton_nginx.destroy()

    if go_to_monitor:
        putMonitorItems()
        # dir_actual = subprocess.getoutput("/usr/bin/pwd")
        # usuario = subprocess.getoutput("whoami")
        # subprocess.run(f"/usr/bin/pkexec {dir_actual}/setup.sh {usuario}", shell=True)
    else:
        putConfigItems()


def putServerItems(go_to_monitor=False):
    """
        Muestra la pantalla para seleccionar el servidor a monitorizar.

        Args:
            go_to_monitor (bool): Indica si se debe ir directamente a la pantalla de monitoreo.

        Returns:
            None
    """
    global label_servidor, boton_apache, boton_nginx
    
    root.resizable(True, True)
    root.geometry("400x180")
    label_titulo.place(relx=0.5, y=30, anchor="center")
    centrarVentana(root)

    label_servidor = ttk.Label(
        root,
        text="Por favor, seleccione el servidor a monitorizar:",
        font="Helvetica 12 bold",
        style='info.TLabel')
    label_servidor.place(relx=0.5, y=80, anchor="center")

    boton_apache = ttk.Button(
        root,
        text="Apache",
        width=15,
        command=lambda: seleccionarServidor("APACHE", go_to_monitor))
    boton_apache.place(relx=0.3, y=130, anchor="center")

    boton_nginx = ttk.Button(
        root,
        text="Nginx",
        width=15,
        command=lambda: seleccionarServidor("NGINX", go_to_monitor),
        style='warning.TButton')
    boton_nginx.place(relx=0.7, y=130, anchor="center")


########################SELECCIÓN RUTA CONFIG########################

def seleccionarRutaConfig(go_to_monitor=False):
    """
        Selecciona la ruta del archivo de configuración y muestra la siguiente pantalla.

        Args:
            go_to_monitor (bool): Indica si se debe ir directamente a la pantalla de monitoreo.

        Returns:
            None
    """
    global main_config_path, root

    root.unbind("<Return>")

    main_config_path = combo_box_config.get()
    set_key(".env", "CONFIG_PATH", main_config_path)

    label_pedir_config.destroy()
    boton_submit_config.destroy()
    combo_box_config.destroy()
    boton_volver_config.destroy()

    if go_to_monitor:
        putMonitorItems()
        dir_actual = subprocess.getoutput("/usr/bin/pwd")
        usuario = subprocess.getoutput("whoami")
        subprocess.run(f"/usr/bin/pkexec {dir_actual}/setup.sh {usuario}", shell=True)
    else:
        putLogsItems()

def VolverConfig(go_to_monitor=False):

    root.unbind("<Return>")

    label_pedir_config.destroy()
    boton_submit_config.destroy()
    combo_box_config.destroy()
    boton_volver_config.destroy()

    if go_to_monitor:
        putMonitorItems()
    else:
        putServerItems()

def putConfigItems(go_to_monitor=False):
    """
        Muestra la pantalla para seleccionar la ruta del archivo de configuración.

        Args:
            go_to_monitor (bool): Indica si se debe ir directamente a la pantalla de monitoreo.

        Returns:
            None
    """
    global combo_box_config, boton_submit_config, label_pedir_config, boton_volver_config

    label_titulo.place(relx=0.5, y=30, anchor="center")
    root.resizable(True, True)
    root.geometry("600x300")
    centrarVentana(root)

    if main_server == "APACHE":
        combo_box_config = ttk.Combobox(root,
                                        style="TCombobox",
                                        values=config.APACHE_CONFIG_PATH,
                                        width=50)
    elif main_server == "NGINX":
        combo_box_config = ttk.Combobox(root,
                                        style="TCombobox",
                                        values=config.NGINX_CONFIG_PATH,
                                        width=50)

    combo_box_config.current(0)
    combo_box_config.place(relx=0.5, y=160, anchor="center")

    boton_submit_config = ttk.Button(
        root,
        text="Enviar",
        width=15,
        command=lambda: seleccionarRutaConfig(go_to_monitor),
        style='success.TButton')
    boton_submit_config.place(relx=0.75, y=250, anchor="center")

    label_pedir_config = ttk.Label(
        root,
        text=
        "Por favor, introduzca la ruta del archivo de configuración del servidor:",
        font="Helvetica 12 bold",
        style='info.TLabel')
    label_pedir_config.place(relx=0.5, y=100, anchor="center")

    root.bind("<Return>", lambda event: seleccionarRutaConfig(go_to_monitor))

    boton_volver_config = ttk.Button(
        root,
        text="Volver",
        width=15,
        command=lambda: VolverConfig(go_to_monitor),
        style='danger.TButton')
    boton_volver_config.place(relx=0.25, y=250, anchor="center")

########################SELECCIÓN RUTA LOGS########################


def seleccionarRutaLogs(go_to_monitor=False):
    global main_log_path, root

    root.unbind("<Return>")

    main_log_path = combo_box_logs.get()
    set_key(".env", "LOG_PATH", main_log_path)

    label_pedir_logs.destroy()
    boton_submit_logs.destroy()
    combo_box_logs.destroy()
    boton_volver_logs.destroy()
    

    if go_to_monitor:
        putMonitorItems()
        dir_actual = subprocess.getoutput("/usr/bin/pwd")
        usuario = subprocess.getoutput("whoami")
        subprocess.run(f"/usr/bin/pkexec {dir_actual}/setup.sh {usuario}", shell=True)
    else:
        putBansItems()

def VolverLogs(go_to_monitor=False):
    
        root.unbind("<Return>")
    
        label_pedir_logs.destroy()
        boton_submit_logs.destroy()
        combo_box_logs.destroy()
        boton_volver_logs.destroy()
    
        if go_to_monitor:
            putMonitorItems()
        else:
            putConfigItems()

def putLogsItems(go_to_monitor=False):
    global combo_box_logs, boton_submit_logs, label_pedir_logs, boton_volver_logs

    label_titulo.place(relx=0.5, y=30, anchor="center")
    root.resizable(True, True)
    root.geometry("600x300")
    centrarVentana(root)

    if main_server == "APACHE":
        combo_box_logs = ttk.Combobox(root,
                                      style="TCombobox",
                                      values=config.APACHE_LOG_PATHS,
                                      width=50)
    elif main_server == "NGINX":
        combo_box_logs = ttk.Combobox(root,
                                      style="TCombobox",
                                      values=config.NGINX_LOG_PATHS,
                                      width=50)

    combo_box_logs.current(0)
    combo_box_logs.place(relx=0.5, y=160, anchor="center")

    boton_submit_logs = ttk.Button(
        root,
        text="Enviar",
        width=15,
        command=lambda: seleccionarRutaLogs(go_to_monitor),
        style='success.TButton')
    boton_submit_logs.place(relx=0.75, y=250, anchor="center")

    label_pedir_logs = ttk.Label(
        root,
        text=
        "Por favor, introduzca la ruta del archivo de los logs del servidor:",
        font="Helvetica 12 bold",
        style='info.TLabel')
    label_pedir_logs.place(relx=0.5, y=100, anchor="center")

    root.bind("<Return>", lambda event: seleccionarRutaLogs(go_to_monitor))

    boton_volver_logs = ttk.Button(
        root,
        text="Volver",
        width=15,
        command=lambda: VolverLogs(go_to_monitor),
        style='danger.TButton')
    boton_volver_logs.place(relx=0.25, y=250, anchor="center")

########################SELECCIÓN RUTA BANS########################  MAL


def seleccionarRutaBans(go_to_monitor=False):
    global main_ban_path, root

    root.unbind("<Return>")

    main_ban_path = combo_box_bans.get()
    set_key(".env", "BAN_PATH", main_ban_path)

    label_pedir_bans.destroy()
    boton_submit_bans.destroy()
    combo_box_bans.destroy()
    boton_volver_bans.destroy()

    if go_to_monitor:
        putMonitorItems()
        dir_actual = subprocess.getoutput("/usr/bin/pwd")
        usuario = subprocess.getoutput("whoami")
        subprocess.run(f"/usr/bin/pkexec {dir_actual}/setup.sh {usuario}", shell=True)
    else:
        putsDatabaseItems()

def VolverBans(go_to_monitor=False):
        
            root.unbind("<Return>")
        
            label_pedir_bans.destroy()
            boton_submit_bans.destroy()
            combo_box_bans.destroy()
            boton_volver_bans.destroy()
        
            if go_to_monitor:
                putMonitorItems()
            else:
                putLogsItems()

def putBansItems(go_to_monitor=False):
    global combo_box_bans, boton_submit_bans, label_pedir_bans, boton_volver_bans

    label_titulo.place(relx=0.5, y=30, anchor="center")
    root.resizable(True, True)
    root.geometry("600x300")
    centrarVentana(root)

    if main_server == "APACHE":
        combo_box_bans = ttk.Combobox(root,
                                      style="TCombobox",
                                      values=config.APACHE_BAN_PATH,
                                      width=50)
    elif main_server == "NGINX":
        combo_box_bans = ttk.Combobox(root,
                                      style="TCombobox",
                                      values=config.NGINX_BAN_PATH,
                                      width=50)

    combo_box_bans.current(0)
    combo_box_bans.place(relx=0.5, y=160, anchor="center")

    boton_submit_bans = ttk.Button(
        root,
        text="Enviar",
        width=15,
        command=lambda: seleccionarRutaBans(go_to_monitor),
        style='success.TButton')
    boton_submit_bans.place(relx=0.75, y=250, anchor="center")

    label_pedir_bans = ttk.Label(
        root,
        text=
        "Por favor, introduzca la ruta del archivo de los bans del servidor:",
        font="Helvetica 12 bold",
        style='info.TLabel')
    label_pedir_bans.place(relx=0.5, y=100, anchor="center")

    root.bind("<Return>", lambda event: seleccionarRutaBans(go_to_monitor))

    boton_volver_bans = ttk.Button(
        root,
        text="Volver",
        width=15,
        command=lambda: VolverBans(go_to_monitor),
        style='danger.TButton')
    boton_volver_bans.place(relx=0.25, y=250, anchor="center")

########################INTRODUCIÓN NOMBRE DATABASE########################


def seleccionarNombreDatabase(go_to_monitor=False):
    global data_base_name, root

    root.unbind("<Return>")

    data_base_name = combo_box_database.get()
    set_key(".env", "DATABASE_FILE", data_base_name)

    label_pedir_database.destroy()
    boton_submit_database.destroy()
    combo_box_database.destroy()
    boton_volver_database.destroy()

    if go_to_monitor:
        putMonitorItems()
        # dir_actual = subprocess.getoutput("/usr/bin/pwd")
        # usuario = subprocess.getoutput("whoami")
        # subprocess.run(f"/usr/bin/pkexec {dir_actual}/setup.sh {usuario}", shell=True)
    else:
        putsTelegramItems()

def VolverDatabase(go_to_monitor=False):
            
    root.unbind("<Return>")

    label_pedir_database.destroy()
    boton_submit_database.destroy()
    combo_box_database.destroy()
    boton_volver_database.destroy()

    if go_to_monitor:
        putMonitorItems()
    else:
        putBansItems()

def putsDatabaseItems(go_to_monitor=False):
    global combo_box_database, boton_submit_database, label_pedir_database, boton_volver_database

    label_titulo.place(relx=0.5, y=30, anchor="center")
    root.resizable(True, True)
    root.geometry("600x300")
    centrarVentana(root)

    combo_box_database = ttk.Combobox(root,
                                      style="TCombobox",
                                      values=config.DATABASE_FILE,
                                      width=50)
    combo_box_database.current(0)
    combo_box_database.place(relx=0.5, y=160, anchor="center")

    boton_submit_database = ttk.Button(
        root,
        text="Enviar",
        width=15,
        command=lambda: seleccionarNombreDatabase(go_to_monitor),
        style='success.TButton')
    boton_submit_database.place(relx=0.75, y=250, anchor="center")

    label_pedir_database = ttk.Label(
        root,
        text="Por favor, introduzca el nombre de la base de datos:",
        font="Helvetica 12 bold",
        style='info.TLabel')
    label_pedir_database.place(relx=0.5, y=100, anchor="center")

    root.bind("<Return>", lambda event: seleccionarNombreDatabase(go_to_monitor))

    boton_volver_database = ttk.Button(
        root,
        text="Volver",
        width=15,
        command=lambda: VolverDatabase(go_to_monitor),
        style='danger.TButton')
    boton_volver_database.place(relx=0.25, y=250, anchor="center")

########################INTRODUCIÓN USUARIO TELEGRAM########################


def seleccionarTelegramUser(muestraAviso=True):
    global telegram_username, root

    root.unbind("<Return>")

    telegram_username = input_telegram.get()
    set_key(".env", "TELEGRAM_USER", telegram_username)

    dir_actual = subprocess.getoutput("/usr/bin/pwd")
    usuario = subprocess.getoutput("whoami")
    subprocess.run(f"/usr/bin/pkexec {dir_actual}/setup.sh {usuario}", shell=True)

    input_telegram.destroy()
    boton_submit_telegram.destroy()
    label_pedir_telegram.destroy()
    boton_volver_telegram.destroy()

    putMonitorItems()

    if muestraAviso:
        putAviso()

def volverTelegramUser(putAviso=True):
    global telegram_username, root

    root.unbind("<Return>")

    input_telegram.destroy()
    boton_submit_telegram.destroy()
    label_pedir_telegram.destroy()
    boton_volver_telegram.destroy()

    if putAviso:
        putsDatabaseItems()
    else:
        putMonitorItems()

def putsTelegramItems(muestraAviso=True):
    global input_telegram, boton_submit_telegram, label_pedir_telegram, boton_volver_telegram
    
    label_titulo.place(relx=0.5, y=30, anchor="center")
    root.resizable(True, True)
    root.geometry("600x300")
    centrarVentana(root)

    input_telegram = ttk.Entry(root, style='info.TEntry')
    input_telegram.bind(
        "<KeyRelease>", lambda event: verificarContenido(
            input_telegram, boton_submit_telegram))
    input_telegram.place(relx=0.5, y=160, anchor="center")
    input_telegram.focus_set()

    boton_submit_telegram = ttk.Button(
        root,
        text="Saltar",
        width=15,
        state=ttk.NORMAL,
        command=lambda: seleccionarTelegramUser(muestraAviso),
        style='danger.TButton')
    boton_submit_telegram.place(relx=0.75, y=250, anchor="center")

    label_pedir_telegram = ttk.Label(
        root,
        text=
        "Por favor, introduzca el usuario de telegram:\n (Debes enviar /start al bot para que funcione)",
        font="Helvetica 12 bold",
        style='info.TLabel')
    label_pedir_telegram.place(relx=0.5, y=100, anchor="center")

    root.bind("<Return>", lambda event: seleccionarTelegramUser(muestraAviso))

    boton_volver_telegram = ttk.Button(
        root,
        text="Volver",
        width=15,
        command=lambda: volverTelegramUser(muestraAviso),
        style='danger.TButton')
    boton_volver_telegram.place(relx=0.25, y=250, anchor="center")

######################## AVISOS ########################


def putAviso():
    ventana_aviso = ttk.Toplevel()
    ventana_aviso.title("Aviso")
    ventana_aviso.geometry("450x180")

    label_aviso = ttk.Label(
        ventana_aviso,
        text=
        "Se han guardado los archivos de configuración en .env.\n\nPara modificarlos, selccionelo abajo a la izquierda y \npulsa el botón de modificar.",
        font="Helvetica 12 bold",
        style='info.TLabel')
    label_aviso.place(relx=0.5, rely=0.3, anchor="center")

    boton_ok = ttk.Button(ventana_aviso,
                          text="OK",
                          width=12,
                          command=ventana_aviso.destroy,
                          style='success.TButton')
    boton_ok.place(relx=0.5, rely=0.7, anchor="center")

    centrarVentana(ventana_aviso)


def mostrarVentanaMonitor():
    global root, splash_root
    root.deiconify()
    splash_root.destroy()


def cambiarColor(color_antiguo):
    global colors, graph
    ventana = ttkbootstrap.dialogs.colorchooser.ColorChooserDialog(initialcolor=color_antiguo)
    ventana.show()
    colors = ventana.result
    graph.cambiarColor(colors.hex)


######################## VENTANA PRINCIPAL PARA MONITORIZAR ########################
def putMonitorItems():
    """
        Muestra la pantalla de monitoreo.

        Returns:
            None
    """
    global kaki, slider, splash_root, max, min, graph_thread, slider_label, root, anti_dos, opciones_parametros, boton_monitor, boton_parar_monitor, boton_cerrar, label_modificar_parametro, boton_modificar_parametro, menu_botones, menu, scrolled_text_baneos, boton_cambiar_color 

    #Esconde la ventana del monitor
    root.withdraw()

    kaki = ttk.PhotoImage(file="images/kaki.png")
    kaki = kaki.subsample(3)

    splash_root = ttk.Toplevel()
    splash_root.withdraw()

    splash_label = ttk.Label(splash_root,
                             text="Cargando...",
                             font="Helvetica 30 bold",
                             style='info.TLabel',
                             background='#247ca5')
    splash_label.pack(pady=20)

    # Agregar la imagen debajo del título
    image_label = ttk.Label(splash_root, image=kaki)
    image_label.pack(pady=40)

    progress_bar = ttk.Progressbar(splash_root,
                                   orient="horizontal",
                                   length=300,
                                   mode="determinate")
    progress_bar.pack(pady=10)

    splash_root.wm_attributes('-type', 'splash')
    splash_root.title("Pantalla de carga")
    splash_root.geometry("400x500")
    splash_root.config(background="#247ca5")
    splash_root.resizable(False, False)

    # Centrar la ventana
    splash_root.deiconify()
    centrarVentana(splash_root)

    for i in range(1, 101):
        progress_bar["value"] = i
        splash_root.update_idletasks()
        time.sleep(0.03)

    splash_root.after(0, mostrarVentanaMonitor)

    root.attributes('-zoomed', True)
    label_titulo.place(relx=0.5, rely=0.025, anchor="center")
    scrolled_text_baneos = ScrolledText(root,
                                        width=int((root.winfo_screenwidth() / 11.15)),
                                        height=(root.winfo_screenheight() // 100),
                                        state='disabled')
    scrolled_text_baneos.place(relx=0.6, rely=0.87, anchor="center")

    anti_dos = AntiDOSWeb.AntiDOSWeb(main_server, main_config_path,
                                     main_log_path, main_ban_path,
                                     "%d/%b/%Y:%H:%M:%S %z", data_base_name,
                                     telegram_username, scrolled_text_baneos)

    crearHebraGrafica()

    root.style.configure('success.TButton', font=('Helvetica', 20))
    root.style.configure('warning.TButton', font=('Helvetica', 20))
    root.style.configure('danger.TButton', font=('Helvetica', 20))
    root.style.configure('info.TButton', font=('Helvetica', 16))
    root.style.configure('TMenubutton', font=('Helvetica', 16))

    boton_monitor = ttk.Button(root,
                               text="Empezar monitorización",
                               width=int((root.winfo_screenwidth() / 80)),
                               command=crearHebraMonitor,
                               style='success.TButton')
    boton_monitor.place(relx=0.12, rely=0.2, anchor="center")

    boton_parar_monitor = ttk.Button(root,
                                     text="Parar monitorización",
                                     width=int((root.winfo_screenwidth() / 80)),
                                     command=terminarMonitor,
                                     state=ttk.DISABLED,
                                     style='warning.TButton')
    boton_parar_monitor.place(relx=0.12, rely=0.28, anchor="center")

    boton_cerrar = ttk.Button(root,
                              text="Cerrar programa",
                              width=int((root.winfo_screenwidth() / 80)),
                              command=funcionSalir,
                              style='danger.TButton')
    boton_cerrar.place(relx=0.12, rely=0.36, anchor="center")

    label_modificar_parametro = ttk.Label(root,
                                          text="Modificación de parámetros",
                                          font="Helvetica 22 bold",
                                          style='info.TLabel',
                                          foreground='#247ca5')
    label_modificar_parametro.place(relx=0.12, rely=0.775, anchor="center")

    boton_modificar_parametro = ttk.Button(root,
                                           text="Modificar",
                                           width=int((root.winfo_screenwidth() / 95)),
                                           command=modificarParametro,
                                           style='info.Outline.TButton')
    boton_modificar_parametro.place(relx=0.12, rely=0.875, anchor="center")

    menu_botones = ttk.Menubutton(root,
                                  text='Seleccione el parámetro',
                                  style='info.Outline.TMenubutton')
    menu = ttk.Menu(menu_botones)
    menu_botones.config(width=int((root.winfo_screenwidth() / 80)))
    menu_botones.pack(fill="x", padx=10, pady=10)

    opciones_parametros = ttk.StringVar()
    opciones_parametros.trace_add('write',
                                  lambda *args: seleccionarParametro())
    for option in [
            "Server", "Config_path", "Log_path", "Ban_path", "Database_name",
            "Telegram_user", "Todos"
    ]:
        menu.add_radiobutton(label=option,
                             value=option,
                             variable=opciones_parametros)

    menu_botones['menu'] = menu
    menu_botones.place(relx=0.12, rely=0.825, anchor="center")

    # Slider para controlar el numero de segundos a mostrar en la grafica
    slider_label = ttk.Label(root,
                             text="Número de segundos a mostrar: 60",
                             font="Helvetica 14 bold",
                             style='info.TLabel',
                             foreground='#247ca5')
    slider_label.place(relx=0.35, rely=0.725, anchor="center")


    # Boton para cambiar el color de la grafica
    boton_cambiar_color = ttk.Button(root, text="Cambiar color de gráfica", command=lambda: cambiarColor(graph.graph_color), width=int((root.winfo_screenwidth() / 80)))
    boton_cambiar_color.place(relx=0.85, rely=0.725, anchor="center")

    #slider = ttk.Scale(root, from_=0, to=100, orient="horizontal", variable=slider_value, length=500, tickinterval=10, troughcolor="#C0C0C0")
    slider = customtkinter.CTkSlider(master=root,
                                     from_=min,
                                     to=max,
                                     width=int((root.winfo_screenwidth() / 4)),
                                     command=cambioSlider,
                                     number_of_steps=max - min)
    slider.place(relx=0.6, rely=0.725, anchor="center")


def cambioSlider(value):
    global timer, root, slider_label
    if timer is not None:
        root.after_cancel(timer)
    timer = root.after(250, lambda: actualizarGrafica(value))
    slider_label.config(text=f"Número de segundos a mostrar: {int(value)}")


def actualizarGrafica(tiempo):
    global graph
    tiempo = int(tiempo)
    if graph:
        graph.setTime(tiempo)


def crearHebraGrafica():
    global graph, colors
    color = colors.hex if colors else None
    graph = GraphPage.GraphPage(root, tiempo_grafica, anti_dos, max, color=color)
    graph.setTime(tiempo_grafica)
    graph.place(relx=0.6, rely=0.38, anchor="center")
    graph_thread = Thread(target=animateGraph)
    graph_thread.start()


def animateGraph():
    global graph, animar
    animar = True
    while animar:
        graph.animate()
        time.sleep(1)


def seleccionarParametro():
    """
	Actualiza el texto que aparece en el menú desplegable para seleccionar el parámetro a modificar
	"""
    parametro_elegido = opciones_parametros.get()
    menu_botones.config(text=parametro_elegido)


def actualizarScrolledTest(texto):
    scrolled_text_baneos.config(state='normal')
    scrolled_text_baneos.insert(ttk.END, texto, "mi_color")
    scrolled_text_baneos.config(state='disabled')


def crearHebraMonitor():
    monitor_thread = Thread(target=comenzarMonitor)
    monitor_thread.start()


def comenzarMonitor():
    scrolled_text_baneos.tag_config("mi_color",
                                    foreground="#0dc526",
                                    font=("Helvetica", 12, "bold"))
    actualizarScrolledTest("[+] Monitorizando...\n")
    boton_monitor.config(state=ttk.DISABLED)
    boton_parar_monitor.config(state=ttk.NORMAL)
    anti_dos.monitor()


def terminarMonitor():
    scrolled_text_baneos.tag_config("mi_color",
                                    foreground="orange",
                                    font=("Helvetica", 12, "bold"))
    actualizarScrolledTest("\n[!] Monitorización detenida\n\n")
    boton_parar_monitor.config(state=ttk.DISABLED)
    boton_monitor.config(state=ttk.NORMAL)
    anti_dos.terminarMonitor()


def funcionSalir():
    global animar
    animar = False
    terminarMonitor()
    print("\n\n[!] Saliendo...\n")
    sys.exit(1)


def modificarParametro():
    global graph, graph_thread, animar
    parametro = opciones_parametros.get()

    if parametro:
        animar = False
        terminarMonitor()
        root.attributes('-zoomed', False)
        graph.destroy()
        boton_monitor.destroy()
        boton_parar_monitor.destroy()
        boton_cerrar.destroy()
        label_modificar_parametro.destroy()
        boton_modificar_parametro.destroy()
        menu_botones.destroy()
        scrolled_text_baneos.master.destroy()
        slider_label.destroy()
        slider.destroy()
        boton_cambiar_color.destroy()
        root.style.configure('success.TButton', font=('Helvetica', 12))
        root.style.configure('warning.TButton', font=('Helvetica', 12))
        root.style.configure('danger.TButton', font=('Helvetica', 12))
        root.style.configure('info.TButton', font=('Helvetica', 12))

    graph_thread = None
    graph = None

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


######################## MAIN ########################
def onClosing():
    """
        Función para cerrar la aplicación.

        Returns:
            None
    """
    global animar
    animar = False
    if anti_dos is not None:
        anti_dos.terminarMonitor()
    print("\n\n[!] Saliendo...\n")
    sys.exit(1)


if __name__ == "__main__":
    global root

    if os.path.isfile('.env'):
        load_dotenv()
        main_server = os.getenv("SERVER")
        main_config_path = os.getenv("CONFIG_PATH")
        main_log_path = os.getenv("LOG_PATH")
        main_ban_path = os.getenv("BAN_PATH")
        data_base_name = os.getenv("DATABASE_FILE")
        telegram_username = os.getenv("TELEGRAM_USER")

        first_time = not main_server or not main_config_path or not main_log_path or not main_ban_path or not data_base_name or not telegram_username

        if not first_time:
            if ((main_config_path and not (os.access(main_config_path, os.R_OK) and os.access(main_config_path, os.W_OK)))
                    and (main_log_path and not os.access(main_log_path, os.R_OK))
                    and (main_ban_path and not (os.access(main_ban_path, os.R_OK) and os.access(main_ban_path, os.W_OK)))
                or not os.path.isfile(main_config_path) or not os.path.isfile(main_log_path) or not os.path.isfile(main_ban_path)
            ):
                dir_actual = subprocess.getoutput("/usr/bin/pwd")
                usuario = subprocess.getoutput("whoami")
                subprocess.run(f"/usr/bin/pkexec {dir_actual}/setup.sh {usuario}", shell=True)



    crearVentanaPrincipal()

    if first_time:
        putServerItems()
    else:
        putMonitorItems()

    root.mainloop()
