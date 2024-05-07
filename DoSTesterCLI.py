import AntiDOSWeb
import config
if __name__ == "__main__":

    anti_dos = AntiDOSWeb.AntiDOSWeb("/var/log/apache2/access.log", "%d/%b/%Y:%H:%M:%S %z",config.APACHE_BAN_PATH)
    #ips_peticiones = anti_dos.extraer_ips_y_horas()
    #print(ips_peticiones)

    anti_dos.monitor()

