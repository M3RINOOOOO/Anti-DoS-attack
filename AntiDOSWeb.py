import os
import re
import subprocess
from datetime import datetime


class AntiDOSWeb:
    def __init__(self, filename, formato_fecha):
        self.filename = filename
        self.formato_fecha = formato_fecha
        self.ult_mod = os.stat(filename).st_mtime

    def leer_registros(self):
        try:
            with open(self.filename, "r") as log:
                registros = log.read()

            # comando = f"tail -n 20 {self.filename}"
            # registros = subprocess.check_output(comando, shell=True, universal_newlines=True)
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
            #hora = match[1]
            hora = datetime.strptime(match[1], self.formato_fecha).timestamp()
            # if ip in ips_horas:
            #     ips_horas[ip].append(hora)
            # else:
            #     ips_horas[ip] = [hora]

            if ip in ips_horas:
                if hora in ips_horas[ip]:
                    ips_horas[ip][hora] += 1
                else:
                    ips_horas[ip][hora] = 1
            else:
                ips_horas[ip] = {hora: 1}

        return ips_horas

    def monitor(self):
        while True:
            ult_mod_actual = os.stat(self.filename).st_mtime
            if ult_mod_actual != self.ult_mod:
                self.ult_mod = ult_mod_actual
                print(self.extraer_ips_y_horas())
