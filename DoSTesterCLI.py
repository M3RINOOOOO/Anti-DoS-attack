import AntiDOSWeb
import config
if __name__ == "__main__":

    anti_dos = AntiDOSWeb.AntiDOSWeb("/var/log/apache2/access.log", config.APACHE_BAN_PATH, "%d/%b/%Y:%H:%M:%S %z", "ip_bans.db")

    anti_dos.monitor()

