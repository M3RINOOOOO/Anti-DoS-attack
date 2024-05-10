#!/bin/bash


# SERVER
# 	- APACHE
#	- NGINX
# CONFIG_PATH
#	- Dar permisos de lectura y escritura
#	- Para APACHE, en el archivo de configuracion tenemos que modificar AllowOverride de None a All (en /var/www/)
# LOG_PATH
#	- Dar permisos de lectura
# BAN_PATH
#	- Para APACHE será el .htaccess de la raiz de la web
#	- Para NGINX será el mismo archivo de configuracion
#	- Dar permisos de lectura y escritura
# ERROR_PATH
#	- Para NGINX, se necesita que el archivo /var/log/nginx/error.log tenga permisos de lectura y escritura (o el archivo equivalente)
while IFS= read -r line || [[ -n "$line" ]]; do
  export "$line"
done < .env

# Guardamos el nombre del usuario sin privilegios
USER=$USER

# Damos los permisos necesarios SOLO para el usuario que esta ejecutando el script
sudo /usr/bin/setfacl -m u:$USER:rw $CONFIG_PATH
sudo /usr/bin/setfacl -m u:$USER:r $LOG_PATH
sudo /usr/bin/setfacl -m u:$USER:rw $BAN_PATH


if [ "$SERVER" = "APACHE" ]; then
  if [ -f "$CONFIG_PATH" ]; then
    # Agrega las líneas al final del archivo
    echo "<Directory $RAIZ_WEB>" >> $CONFIG_PATH
    echo -e "\tAllowOverride All" >> $CONFIG_PATH
    echo "</Directory>" >> $CONFIG_PATH
      
    sudo /usr/bin/systemctl apache2 reload
  else
    echo -e "\n\n[!] El archivo de configuración $CONFIG_PATH no existe!\n"
    exit 1
  fi
  
  sudo service apache2 reload
  
elif [ "$SERVER" = "NGINX" ]; then
  file_sudoers="/etc/sudoers.d/${USER}_anti-dos_nginx"
  permiso_nginx="$USER ALL=(root) NOPASSWD: /usr/sbin/nginx -s reload"
  sudo echo "$permiso_nginx" | sudo tee "$file_sudoers"
fi

