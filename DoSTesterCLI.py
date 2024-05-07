import AntiDOSWeb

if __name__ == "__main__":

    anti_dos = AntiDOSWeb.AntiDOSWeb("/var/log/apache2/access.log")
    ips_peticiones = anti_dos.extraer_ips_y_horas()
    print(ips_peticiones)
