# Archivo de configuracion



# Variables globales por defecto
################## RUTA PARA ENVIAR LOS MENSAJES DESDE EL BOT DE TELEGRAM ##################
URL_ENVIAR_MENSAJE = "https://anti-dos-cbc627e45bd1.herokuapp.com/enviarMensaje/"
TELEGRAM_USERNAME = "M3RINOOOOO"

################## RUTA SERVIDOR WEB ##################
WEB_SERVER_PATH = "/var/www/html/"

################## APACHE ##################
APACHE_LOG_PATHS = ["/var/log/apache2/access.log",
                    "/var/log/apache/access.log",
                    "/var/log/httpd/access.log",
                    "/var/log/httpd/access_log",
                    "/var/log/httpd-access.log"]
APACHE_BAN_PATH = WEB_SERVER_PATH + ".htaccess"

################## NGINX ##################
NGINX_LOG_PATHS = ["/var/log/nginx/access.log"]
NGINX_BAN_PATH = "/etc/nginx/sites-available/default"

################## MAIN ##################
MAIN_SERVER = "apache"
MAIN_LOG_PATH = APACHE_LOG_PATHS[0]
MAIN_BAN_PATH = APACHE_BAN_PATH


def editar_main_info(server, log_path, ban_path):
    global MAIN_LOG_PATH, MAIN_BAN_PATH, MAIN_SERVER
    MAIN_SERVER = server
    MAIN_LOG_PATH= log_path
    MAIN_BAN_PATH = ban_path
    


################## Número máximo de peticiones ##################
MAX_REQUESTS_PER_SEG = 40
MAX_REQUESTS_PER_MIN = 200

################## Tiempo de baneo ##################
TIEMPO_BANEO = 3


