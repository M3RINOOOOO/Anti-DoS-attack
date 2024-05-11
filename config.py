# Archivo de configuracion



# Variables globales por defecto
################## RUTA PARA ENVIAR LOS MENSAJES DESDE EL BOT DE TELEGRAM ##################
URL_ENVIAR_MENSAJE = "https://anti-dos-cbc627e45bd1.herokuapp.com/enviarMensaje/"

################## RUTA SERVIDOR WEB ##################
WEB_SERVER_PATH = "/var/www/html/"

################## SERVIDORES DISPONIBLES ##################
SERVERS = ["nginx", "apache"]

################## APACHE ##################
APACHE_LOG_PATHS = ["/var/log/apache2/access.log",
                    "/var/log/apache/access.log",
                    "/var/log/httpd/access.log",
                    "/var/log/httpd/access_log",
                    "/var/log/httpd-access.log"]
APACHE_BAN_PATH = [WEB_SERVER_PATH + ".htaccess"]
APACHE_CONFIG_PATH = ["/etc/apache2/apache2.conf"]

################## NGINX ##################
NGINX_LOG_PATHS = ["/var/log/nginx/access.log"]
NGINX_BAN_PATH = ["/etc/nginx/sites-available/default"]
NGINX_CONFIG_PATH = ["/etc/nginx/sites-available/default"]

################## MAIN ##################
MAIN_SERVER = "apache"
MAIN_CONFIG_PATH = APACHE_CONFIG_PATH
MAIN_LOG_PATH = APACHE_LOG_PATHS[0]
MAIN_BAN_PATH = APACHE_BAN_PATH
DATABASE_FILE = "ip_bans.db"
TELEGRAM_USERNAME = "M3RINOOOOO"

################## Número máximo de peticiones ##################
MAX_REQUESTS_PER_SEG = 40
MAX_REQUESTS_PER_MIN = 200

################## Tiempo de baneo ##################
TIEMPO_BANEO = 3


