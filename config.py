# Archivo de configuracion



# Variables globales por defecto
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
MAIN_LOG_PATH = NGINX_LOG_PATHS[0]
MAIN_BAN_PATH = NGINX_BAN_PATH
MAIN_SERVER = "nginx"

def editar_main_info(server, log_path, ban_path):
    global MAIN_LOG_PATH, MAIN_BAN_PATH, MAIN_SERVER
    MAIN_LOG_PATH= log_path
    MAIN_BAN_PATH = ban_path
    MAIN_SERVER = server


################## Número máximo de peticiones ##################
MAX_REQUESTS_PER_SEG = 40
MAX_REQUESTS_PER_MIN = 200

################## Tiempo de baneo ##################
TIEMPO_BANEO = 3


