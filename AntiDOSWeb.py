import os
import re
import config
import requests
from datetime import datetime
import sqlite3

class AntiDOSWeb:
########################################  CONSTRUCTOR   ########################################
    def __init__(self, server, log_path, ban_path, formato_fecha, sqlite_path, telegram_user):
        self.server = server
        self.log_path = log_path
        self.ban_path = ban_path
        self.formato_fecha = formato_fecha
        self.sqlite_path = sqlite_path
        self.telegram_user = telegram_user
        self.ult_mod = os.stat(log_path).st_mtime        
        self.ips_horas = {}
        self.inicializarBaseDatos()

######################################## GESTIÓN DE LOGS   ########################################
    def leerRegistros(self):
        try:
            with open(self.log_path, "r") as log:
                registros = log.read()

            return registros
        except Exception as e:
            return f"Error al leer los registros: {e}"    
        
    def extraerIpsHoras(self):
        ips_horas = {}
        patron = r'(\b(?:\d{1,3}\.){3}\d{1,3}\b) .* \[(.*?)\]'
        registros = self.leerRegistros()
        matches = re.findall(patron, registros)

        ips_desbanedas = self.obtenerIpsDesbaneadas()

        for match in matches:
            ip = match[0]
            hora = datetime.strptime(match[1], self.formato_fecha).timestamp()


            fecha_ultimo_baneo = 0
            if ip in self.ips_baneadas:
                fecha_ultimo_baneo = self.ips_baneadas[ip]["last_ban"]


            if not (ip in ips_desbanedas and hora <= fecha_ultimo_baneo):
                if ip in ips_horas:
                    if hora in ips_horas[ip]:
                        ips_horas[ip][hora] += 1
                    else:
                        ips_horas[ip][hora] = 1
                else:
                    ips_horas[ip] = {hora: 1}

        self.ips_horas = ips_horas


    def extraerHorasActividad(self):
        horas_actividad = {}
        patron = r'(\b(?:\d{1,3}\.){3}\d{1,3}\b) .* \[(.*?)\] ".*?" (\d{3}) \d+ "-" ".*?"'
        registros = self.leerRegistros()
        matches = re.findall(patron, registros)

        for match in matches:
            ip = match[0]
            hora = datetime.strptime(match[1], self.formato_fecha).timestamp()
            codigo = int(match[2])

            if codigo != 403:
                if hora in horas_actividad:
                    horas_actividad[hora] += 1
                else:
                    horas_actividad[hora] = 1

        return horas_actividad

######################################## GESTIÓN DE BASE DE DATOS   ########################################    
    def inicializarBaseDatos(self):
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
        conexion = sqlite3.connect(self.sqlite_path)
        cursor = conexion.cursor()
        cursor.execute("SELECT ip, last_ban, n_bans, is_banned FROM ips")
        ips_baneadas = cursor.fetchall()
        ip_baneada = {}
        for ip, last_ban, n_bans, is_banned in ips_baneadas:
            ip_baneada[ip] = {'last_ban': last_ban, 'n_bans': n_bans, "is_banned": is_banned}
        return ip_baneada

    def actualizarBaseDatos(self, ip, ban):
        conexion = sqlite3.connect(self.sqlite_path)
        cursor = conexion.cursor()
        cursor.execute("SELECT n_bans FROM ips WHERE ip = ?", (ip,))
        n_bans = cursor.fetchone()

        if ban:
            if n_bans:
                n_bans = n_bans[0] + 1
                cursor.execute("UPDATE ips SET last_ban = ?, n_bans = ?, is_banned = 1 WHERE ip = ?", (datetime.now().timestamp(), n_bans, ip))
            else:
                cursor.execute("INSERT INTO ips (ip, last_ban, n_bans, is_banned) VALUES (?, ?, ?, 1)", (ip, datetime.now().timestamp(), 1))
        else:
            cursor.execute("UPDATE ips SET is_banned = 0 WHERE ip = ?", (ip,)) 
            
        conexion.commit()
        conexion.close()
        
        self.ips_baneadas = self.obtenerBaseDatos()

    def obtenerIpsDesbaneadas(self):
        conexion = sqlite3.connect(self.sqlite_path)
        cursor = conexion.cursor()
        cursor.execute("SELECT ip FROM ips WHERE is_banned = 0")
        ips = cursor.fetchall()

        ips_desbaneadas = []

        for ip in ips:
            ips_desbaneadas.append(ip[0])

        return ips_desbaneadas


######################################## GESTIÓN DE BANEOS   ########################################

    def banearIp(self, ip):
        try:
            with open(self.ban_path, "a") as ban_file:
                esta_baneado = (ip in self.ips_baneadas) and (self.ips_baneadas[ip]["is_banned"])
            
                if (f"Deny from {ip}" not in open(self.ban_path).read()) and not esta_baneado: 

                    if(self.server == "apache"):
                        ban_file.write(f"Deny from {ip}\n")

                    elif(self.server == "nginx"):

                        with open(self.ban_path, "r") as ban_file:
                            lineas = ban_file.readlines()

                        with open(self.ban_path, "w") as ban_file:
                            for linea in lineas:
                                ban_file.write(linea)
                                if "location / {" in linea:
                                    ban_file.write(f"\t\tdeny {ip};\n")

                        os.system("sudo /usr/sbin/nginx -s reload")

                    self.enviarAvisoPorTelegram(ip)

                    self.actualizarBaseDatos(ip,True)
                    print(f"La IP {ip} ha sido baneada")

            return f"La IP {ip} ha sido baneada"
        except Exception as e:
            return f"Error al banear la IP {ip}: {e}"

    def enviarAvisoPorTelegram(self, ip):
        requests.get(f"{config.URL_ENVIAR_MENSAJE}?username={self.telegram_user}&ip={ip}")

    def desbanearIp(self, ip):
        try:
            with open(self.ban_path, "r") as ban_file:
                lineas = ban_file.readlines()

            with open(self.ban_path, "w") as ban_file:
                for linea in lineas:
                    if self.server == "apache":
                        if f"Deny from {ip}" not in linea:
                            ban_file.write(linea)
                    elif self.server == "nginx":
                        if f"deny {ip};" not in linea:
                            ban_file.write(linea)
            if self.server == "nginx":
                os.system("sudo nginx -s reload")
                    
            return f"La IP {ip} ha sido desbaneada"
        except Exception as e:
            return f"Error al desbanear la IP {ip}: {e}"

######################################## MONITORIZACIÓN   ########################################
    def checkDos(self):
        for ip, horas in self.ips_horas.items():

            for hora, peticiones in horas.items():
                if peticiones > config.MAX_REQUESTS_PER_SEG:
                    self.banearIp(ip)

    def checkDisBan(self):
        for ip in self.ips_baneadas:
            tiempo_baneado = 2**(self.ips_baneadas[ip]["n_bans"] - 1) * config.TIEMPO_BANEO
            if self.ips_baneadas[ip]["last_ban"] + tiempo_baneado <= datetime.now().timestamp() and (self.ips_baneadas[ip]["is_banned"]):
                print(f"La IP {ip} ha sido desbaneada")
                self.actualizarBaseDatos(ip, False)
                self.desbanearIp(ip)

    def monitor(self):
        self.monitorizar = True
        while self.monitorizar:
            self.checkDisBan()
            ult_mod_actual = os.stat(self.log_path).st_mtime
            if ult_mod_actual != self.ult_mod:
                self.ult_mod = ult_mod_actual
                self.extraerIpsHoras()
                self.checkDos()
                
    
    def terminarMonitor(self):
        self.monitorizar = False
