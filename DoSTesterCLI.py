import AntiDOSWeb
import config
import sys, signal

def def_handler(sig, frame):
	print("\n\n[!] Saliendo forzadamente...\n")
	sys.exit(1)
      
signal.signal(signal.SIGINT, def_handler)
      
if __name__ == "__main__":

    anti_dos = AntiDOSWeb.AntiDOSWeb("/var/log/apache2/access.log", config.APACHE_BAN_PATH, "%d/%b/%Y:%H:%M:%S %z", "ip_bans.db")

    anti_dos.monitor()

