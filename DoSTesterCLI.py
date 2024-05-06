import subprocess
import re

def leer_registros_apache():
    try:
        comando = "tail -n 20 /var/log/apache2/access.log"  
        registros = subprocess.check_output(comando, shell=True, universal_newlines=True)
        return registros
    except Exception as e:
        return f"Error al leer los registros de Apache2: {e}"

def extraer_ips_y_horas(registros):
    ips_horas = {}
    patron = r'(\b(?:\d{1,3}\.){3}\d{1,3}\b) .* \[(.*?)\]'
    matches = re.findall(patron, registros)
    for match in matches:
        ip = match[0]
        hora = match[1]
        if ip in ips_horas:
            ips_horas[ip].append(hora)
        else:
            ips_horas[ip] = [hora]
    return ips_horas


if __name__ == "__main__":
    registros = leer_registros_apache()
    ips_peticiones = extraer_ips_y_horas(registros)
    print(ips_peticiones)
