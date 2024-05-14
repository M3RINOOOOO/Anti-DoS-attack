import os
import re
import config
import requests
from datetime import datetime, timedelta
import sqlite3
import tkinter as tk
from file_read_backwards import FileReadBackwards
from termcolor import colored


class AntiDOSWeb:
    """
    Clase para gestionar la mitigación de ataques DDoS en servidores web.
    """

    def __init__(self,
                 server,
                 config_path,
                 log_path,
                 ban_path,
                 formato_fecha,
                 sqlite_path,
                 telegram_user,
                 scroll_gui=False):
        """
        Constructor de la clase AntiDOSWeb.

        Parámetros:
            server (str): El tipo de servidor web en uso (Apache o Nginx).
            config_path (str): La ruta al archivo de configuración del servidor.
            log_path (str): La ruta al archivo de logs del servidor.
            ban_path (str): La ruta al archivo de baneos.
            formato_fecha (str): El formato de fecha utilizado en los logs.
            sqlite_path (str): La ruta al archivo de base de datos SQLite.
            telegram_user (str): El usuario de Telegram para recibir notificaciones.
            scroll_gui (opcional): Interfaz grafica de desplazamiento por el monitor.
        """
        self.server = server
        self.config_path = config_path
        self.log_path = log_path
        self.ban_path = ban_path
        self.formato_fecha = formato_fecha
        self.sqlite_path = sqlite_path
        self.telegram_user = telegram_user
        self.scroll_gui = scroll_gui
        self.ult_mod = os.stat(log_path).st_mtime
        self.ips_horas = {}
        self.inicializarBaseDatos()
        self.lineas_leidas = 0
        self.extraerIpsHoras()

    def leerRegistros(self):
        """
        Lee los registros del archivo de logs y los devuelve como una cadena.

        Retorna:
            str: Los registros del archivo de logs.
        """
        try:
            with open(self.log_path, "r") as log:
                registros = log.read()

            return registros
        except Exception as e:
            return f"Error al leer los registros: {e}"

    def leerRegistrosCompletos(self):
        """
        Lee todos los registros del archivo de logs y los devuelve como una cadena.

        Retorna:
            str: Todos los registros del archivo de logs.
        """
        try:
            with open(self.log_path, "r") as log:
                registros = log.read()

            return registros
        except Exception as e:
            return f"Error al leer los registros: {e}"

    def extraerIpsHoras(self):
        """
        Extrae las IP y las horas de acceso desde los registros del archivo de logs.
        """
        ips_horas = {}
        patron = r'(\b(?:\d{1,3}\.){3}\d{1,3}\b) .* \[(.*?)\]'
        ips_desbanedas = self.obtenerIpsDesbaneadas()
        with FileReadBackwards(self.log_path, encoding="utf-8") as log:
            for l in log:
                matches = re.findall(patron, l)
                if len(matches) > 0:
                    match = matches[0]
                    ip = match[0]
                    fecha_ultimo_baneo = 0
                    hora = datetime.strptime(match[1],
                                             self.formato_fecha).timestamp()

                    if hora < (datetime.now() +
                               timedelta(seconds=-10)).timestamp():
                        break
                    else:
                        if ip in self.ips_baneadas:
                            fecha_ultimo_baneo = self.ips_baneadas[ip][
                                "last_ban"]

                        if not (ip in ips_desbanedas
                                and hora <= fecha_ultimo_baneo):
                            if ip in ips_horas:
                                if hora in ips_horas[ip]:
                                    ips_horas[ip][hora] += 1
                                else:
                                    ips_horas[ip][hora] = 1
                            else:
                                ips_horas[ip] = {hora: 1}
            self.ips_horas = ips_horas

    def extraerHorasActividad(self, tiempo=0):
        """
        Extrae las horas de actividad a partir de los registros del archivo de logs.

        Parámetros:
            tiempo (int, opcional): El tiempo límite en formato de marca de tiempo UNIX. Por defecto es 0.

        Retorna:
            dict: Un diccionario que contiene las horas de actividad y el número de peticiones en cada hora.
        """
        horas_actividad = {}
        patron = r'(\b(?:\d{1,3}\.){3}\d{1,3}\b) .* \[(.*?)\] ".*?" (\d{3}) \d+ "-" ".*?"'

        with FileReadBackwards(self.log_path, encoding="utf-8") as log:
            for l in log:
                matches = re.findall(patron, l)
                if len(matches) > 0:
                    match = matches[0]
                    hora = datetime.strptime(match[1],
                                             self.formato_fecha).timestamp()

                    if hora < tiempo - 10:
                        break
                    else:
                        codigo = int(match[2])
                        if codigo != 403:
                            if hora in horas_actividad:
                                horas_actividad[hora] += 1
                            else:
                                horas_actividad[hora] = 1

        return horas_actividad

    def inicializarBaseDatos(self):
        """
        Inicializa la base de datos SQLite para almacenar información sobre las IP baneadas.
        """
        conexion = sqlite3.connect(self.sqlite_path)
        cursor = conexion.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS ips (
                    id INTEGER PRIMARY KEY,
                    ip TEXT NOT NULL,
                    last_ban DOUBLE,
                    n_bans INTEGER,
                    is_banned BOOLEAN DEFAULT 1)''')
        conexion.commit()
        self.ips_baneadas = self.obtenerBaseDatos()
        conexion.close()

    def obtenerBaseDatos(self):
        """
        Obtiene las IP baneadas de la base de datos SQLite.

        Retorna:
            dict: Un diccionario que contiene información sobre las IP baneadas.
        """
        conexion = sqlite3.connect(self.sqlite_path)
        cursor = conexion.cursor()
        cursor.execute("SELECT ip, last_ban, n_bans, is_banned FROM ips")
        ips_baneadas = cursor.fetchall()
        ip_baneada = {}
        for ip, last_ban, n_bans, is_banned in ips_baneadas:
            ip_baneada[ip] = {
                'last_ban': last_ban,
                'n_bans': n_bans,
                "is_banned": is_banned
            }
        return ip_baneada

    def actualizarBaseDatos(self, ip, ban):
        """
        Actualiza la base de datos SQLite con información sobre las IP baneadas o desbaneadas.

        Parámetros:
            ip (str): La dirección IP a ser actualizada.
            ban (bool): Indica si la IP está siendo baneada (True) o desbaneada (False).
        """
        conexion = sqlite3.connect(self.sqlite_path)
        cursor = conexion.cursor()
        cursor.execute("SELECT n_bans FROM ips WHERE ip = ?", (ip,))
        n_bans = cursor.fetchone()

        if ban:
            if n_bans:
                n_bans = n_bans[0] + 1
                cursor.execute(
                    "UPDATE ips SET last_ban = ?, n_bans = ?, is_banned = 1 WHERE ip = ?",
                    (datetime.now().timestamp(), n_bans, ip))
            else:
                cursor.execute(
                    "INSERT INTO ips (ip, last_ban, n_bans, is_banned) VALUES (?, ?, ?, 1)",
                    (ip, datetime.now().timestamp(), 1))
        else:
            cursor.execute("UPDATE ips SET is_banned = 0 WHERE ip = ?", (ip,))

        conexion.commit()
        conexion.close()

        self.ips_baneadas = self.obtenerBaseDatos()

    def obtenerIpsDesbaneadas(self):
        """
        Obtiene las IP desbaneadas de la base de datos SQLite.

        Retorna:
            list: Una lista de direcciones IP desbaneadas.
        """
        conexion = sqlite3.connect(self.sqlite_path)
        cursor = conexion.cursor()
        cursor.execute("SELECT ip FROM ips WHERE is_banned = 0")
        ips = cursor.fetchall()

        ips_desbaneadas = []

        for ip in ips:
            ips_desbaneadas.append(ip[0])

        return ips_desbaneadas

    def banearIp(self, ip):
        """
        Banea una dirección IP y la registra en la base de datos.

        Parámetros:
            ip (str): La dirección IP a ser baneada.

        Retorna:
            str: Mensaje indicando el resultado del baneo.
        """
        try:
            with open(self.ban_path, "a") as ban_file:
                esta_baneado = (ip in self.ips_baneadas) and (self.ips_baneadas[ip]["is_banned"])
                if (f"Deny from {ip}" not in open(
                        self.ban_path).read()) and not esta_baneado:

                    if self.server == "APACHE":
                        ban_file.write(f"Deny from {ip}\n")

                    elif self.server == "NGINX":

                        with open(self.ban_path, "r") as ban_file:
                            lineas = ban_file.readlines()

                        with open(self.ban_path, "w") as ban_file:
                            for linea in lineas:
                                ban_file.write(linea)
                                if "location / {" in linea:
                                    ban_file.write(f"\t\tdeny {ip};\n")

                        os.system("sudo /usr/sbin/nginx -s reload")

                    self.enviarAvisoPorTelegram(ip)

                    self.actualizarBaseDatos(ip, True)

                    hora_actual = datetime.now()
                    hora_formateada = hora_actual.strftime(
                        "%d/%b/%Y:%H:%M:%S %z")

                    if self.scroll_gui:
                        self.scroll_gui.config(state='normal')
                        self.scroll_gui.insert(
                            tk.END,
                            f"[ {hora_formateada}] La IP {ip} ha sido baneada\n",
                            "mi_color")
                        self.scroll_gui.config(state='disabled')
                    else:
                        print(colored(f"[ {hora_formateada}]", "light_blue"), f"La IP {ip} ha sido",
                              colored("baneada", "red"))

            return f"La IP {ip} ha sido baneada"
        except Exception as e:
            return f"Error al banear la IP {ip}: {e}"

    def enviarAvisoPorTelegram(self, ip):
        """
        Envía un aviso de baneo por Telegram.

        Parámetros:
            ip (str): La dirección IP baneada.
        """
        if self.telegram_user:
            requests.get(
                f"{config.URL_ENVIAR_MENSAJE}?username={self.telegram_user}&ip={ip}"
            )

    def desbanearIp(self, ip):
        """
        Desbanea una dirección IP.

        Parámetros:
            ip (str): La dirección IP a ser desbaneada.

        Retorna:
            str: Mensaje indicando el resultado del desbaneo.
        """
        try:
            with open(self.ban_path, "r") as ban_file:
                lineas = ban_file.readlines()

            with open(self.ban_path, "w") as ban_file:
                for linea in lineas:
                    if self.server == "APACHE":
                        if f"Deny from {ip}" not in linea:
                            ban_file.write(linea)
                    elif self.server == "NGINX":
                        if f"deny {ip};" not in linea:
                            ban_file.write(linea)
            if self.server == "NGINX":
                os.system("sudo nginx -s reload")

            return f"La IP {ip} ha sido desbaneada"
        except Exception as e:
            return f"Error al desbanear la IP {ip}: {e}"

    def checkDos(self):
        """
        Verifica si se está produciendo un ataque DDoS y banea las IP involucradas.
        """
        for ip, horas in self.ips_horas.items():

            for hora, peticiones in horas.items():
                if peticiones > config.MAX_REQUESTS_PER_SEG:
                    self.banearIp(ip)

    def checkDisBan(self):
        """
        Verifica si alguna IP baneada debe ser desbaneada según el tiempo de baneo.
        """
        for ip in self.ips_baneadas:
            tiempo_baneado = 2 ** (self.ips_baneadas[ip]["n_bans"] -
                                   1) * config.TIEMPO_BANEO
            if self.ips_baneadas[ip][
                "last_ban"] + tiempo_baneado <= datetime.now().timestamp(
            ) and (self.ips_baneadas[ip]["is_banned"]):

                hora_actual = datetime.now()
                hora_formateada = hora_actual.strftime("%d/%b/%Y:%H:%M:%S %z")

                if self.scroll_gui:
                    self.scroll_gui.config(state='normal')
                    self.scroll_gui.insert(
                        tk.END,
                        f"[ {hora_formateada}] La IP {ip} ha sido desbaneada\n",
                        "mi_color")
                    self.scroll_gui.config(state='disabled')
                else:
                    print(colored(f"[ {hora_formateada}]", "light_blue"), f"La IP {ip} ha sido",
                          colored("desbaneada", "green"))
                self.actualizarBaseDatos(ip, False)
                self.desbanearIp(ip)

    def monitor(self):
        """
        Inicia el monitoreo de los logs para detectar ataques DDoS y gestionar los baneos.
        """
        self.monitorizar = True
        while self.monitorizar:
            self.checkDisBan()
            ult_mod_actual = os.stat(self.log_path).st_mtime
            self.extraerIpsHoras()

            if ult_mod_actual != self.ult_mod:
                self.ult_mod = ult_mod_actual
                self.checkDos()

    def terminarMonitor(self):
        """
        Detiene el monitoreo de los logs.
        """
        self.monitorizar = False
