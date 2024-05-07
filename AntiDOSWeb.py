import os
import re
import config
from datetime import datetime


class AntiDOSWeb:
    def __init__(self, log_path, ban_path, formato_fecha, sqlite_path):
        self.log_path = log_path
        self.formato_fecha = formato_fecha
        self.ult_mod = os.stat(log_path).st_mtime
        self.ban_path = ban_path
        self.ips_horas = {}
        self.ip_baneadas = []

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
                if not f"Deny from {ip}" in open(self.ban_path).read():
                    ban_file.write(f"Deny from {ip}\n")
            return f"La IP {ip} ha sido baneada"
        except Exception as e:
            return f"Error al banear la IP {ip}: {e}"

    def checkDos(self):
        for ip, horas in self.ips_horas.items():
            for hora, peticiones in horas.items():
                if peticiones > config.MAX_REQUESTS_PER_SEG:
                    self.banearIp(ip)

    def monitor(self):
        while True:
            ult_mod_actual = os.stat(self.log_path).st_mtime
            if ult_mod_actual != self.ult_mod:
                self.ult_mod = ult_mod_actual
                self.extraerIpsHoras()
                self.checkDos()
