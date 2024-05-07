import os
import re
import config
import TelegramBot
from datetime import datetime
import sqlite3

class AntiDOSWeb:
    def __init__(self, log_path, ban_path, formato_fecha, sqlite_path):
        self.log_path = log_path
        self.formato_fecha = formato_fecha
        self.ult_mod = os.stat(log_path).st_mtime
        self.ban_path = ban_path
        self.sqlite_path = sqlite_path
        self.ips_horas = {}
        self.inicializarBaseDatos()

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

    def obtenerBaseDatos(self):
        conexion = sqlite3.connect(self.sqlite_path)
        cursor = conexion.cursor()
        cursor.execute("SELECT ip, last_ban, n_bans, is_banned FROM ips")
        ips_baneadas = cursor.fetchall()
        ip_baneada = {}
        for ip, last_ban, n_bans, is_banned in ips_baneadas:
            ip_baneada[ip] = {'last_ban': last_ban, 'n_bans': n_bans, "is_banned": is_banned}
        
        print(ip_baneada)
        return ip_baneada

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
        for match in matches:
            ip = match[0]
            hora = datetime.strptime(match[1], self.formato_fecha).timestamp()

            if ip in ips_horas:
                if hora in ips_horas[ip]:
                    ips_horas[ip][hora] += 1
                else:
                    ips_horas[ip][hora] = 1
            else:
                ips_horas[ip] = {hora: 1}

        self.ips_horas = ips_horas

    def banearIp(self, ip):
        try:
            with open(self.ban_path, "a") as ban_file:
                esta_baneado = (ip in self.ips_baneadas) and (self.ips_baneadas[ip]["is_banned"])
            
                if (f"Deny from {ip}" not in open(self.ban_path).read()) and not esta_baneado: 
                    ban_file.write(f"Deny from {ip}\n")
                    TelegramBot.enviarAvisoDos("M3RINOOOOO", ip)
                    self.actualizarBaseDatos(ip,True)
            return f"La IP {ip} ha sido baneada"
        except Exception as e:
            return f"Error al banear la IP {ip}: {e}"

    def desbanearIp(self, ip):
        try:
            with open(self.ban_path, "r") as ban_file:
                lineas = ban_file.readlines()

            with open(self.ban_path, "w") as ban_file:
                for linea in lineas:
                    if f"Deny from {ip}" not in linea:
                        ban_file.write(linea)

            return f"La IP {ip} ha sido desbaneada"
        except Exception as e:
            return f"Error al desbanear la IP {ip}: {e}"

    def checkDos(self):
        for ip, horas in self.ips_horas.items():
            for hora, peticiones in horas.items():
                if peticiones > config.MAX_REQUESTS_PER_SEG:
                    self.banearIp(ip)

    def checkDisBan(self):
        for ip in self.ips_baneadas:
            tiempo_baneado = 2**(self.ips_baneadas[ip]["n_bans"] - 1) * config.TIEMPO_BANEO
            # print(f"Tiempo baneado: {tiempo_baneado}")
            # print(f"Baneado hasta: {self.ips_baneadas[ip]['last_ban'] + tiempo_baneado}")
            # print(f"Ahora son las: {datetime.now().timestamp()}")
            if self.ips_baneadas[ip]["last_ban"] + tiempo_baneado <= datetime.now().timestamp() and (self.ips_baneadas[ip]["is_banned"]):
                print(f"La IP {ip} ha sido desbaneada")
                self.actualizarBaseDatos(ip, False)
                self.desbanearIp(ip)


    def monitor(self):
        while True:
            self.checkDisBan()

            ult_mod_actual = os.stat(self.log_path).st_mtime
            if ult_mod_actual != self.ult_mod:
                self.ult_mod = ult_mod_actual
                self.extraerIpsHoras()
                self.checkDos()
