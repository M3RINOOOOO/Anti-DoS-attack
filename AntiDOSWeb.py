import os
import re
import subprocess


class AntiDOSWeb:
    def __init__(self, filename):
        self.filename = filename
        self.ult_mod = os.stat(filename).st_mtime

    def leer_registros(self):
        try:
            comando = f"tail -n 20 {self.filename}"
            registros = subprocess.check_output(comando, shell=True, universal_newlines=True)
            return registros
        except Exception as e:
            return f"Error al leer los registros: {e}"

    def extraer_ips_y_horas(self):
        ips_horas = {}
        patron = r'(\b(?:\d{1,3}\.){3}\d{1,3}\b) .* \[(.*?)\]'
        registros = self.leer_registros()
        matches = re.findall(patron, registros)
        for match in matches:
            ip = match[0]
            hora = match[1]
            if ip in ips_horas:
                ips_horas[ip].append(hora)
            else:
                ips_horas[ip] = [hora]
        return ips_horas
