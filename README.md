# Anti-DOS

Anti-DOS es una herramienta para mejorar la resistencia de los servidores web contra ataques de denegación de servicio (DoS), tanto a través de una interfaz de línea de comandos como de una interfaz gráfica de usuario (GUI).

## Principal contenido del repositorio

- **AntiDOSWeb.py**: Este módulo contiene la implementación de funcionalidades para prevenir ataques DoS en una aplicación web.
- **config.py**: Aquí se almacena la configuración de la aplicación, como URL, rutas de archivos y otros parámetros importantes.
- **DoSTesterCLI.py**: Archivo que proporciona una interfaz de línea de comandos para ejecutar el programa Anti-DOS
- **DoSTesterGUI.py**: Archivo que implementa la interfaz gráfica de usuario (GUI) para ejecutar el programa Anti-DOS de manera más visual e interactiva.
- **GraphPage.py**: Contiene la implementación de una página de gráficos para mostrar datos relacionados con ataques DoS.
- **requirements.txt**: Archivo que enumera todas las dependencias y bibliotecas de Python necesarias para ejecutar la aplicación.
- **setup.sh**: Script de configuración para configurar la aplicación.

## Instalación

Para instalar la herramienta, podemos seguir estos pasos
1. Primero nos clonaremos el repositorio:

    ```bash
    git clone https://github.com/M3RINOOOOO/Anti-DoS-attack.git
   ```

2. Entramos a la carpeta del proyecto e instalamos las dependencias

    ```bash
   cd Anti-DoS-attack && pip3 install -r requirements.txt
   ```
3. Ahora le damos permisos de ejecución a los archivos necesarios
    ```bash
    chmod +x AntiDoSCLI.py AntiDoSGUI.py setup.sh
   ```
3. Ya estás listo para ejecutar la herramienta para mejorar la seguridad de tu servidor!


## Uso

La herramienta Anti-DOS se puede utilizar tanto desde la línea de comandos como a través de su interfaz gráfica de usuario.

### Interfaz de línea de comandos (CLI)

En el repositorio recién clonado hay un script `AntiDoSCLI.py` que proporciona una interfaz para manejar la aplicación desde la consola.

Podemos ejecutar este script de dos formas:

- **Forma interactiva**. Para ejecutar la CLI de forma interactiva, podemos hacerlo de la siguiente forma:
    ```bash
    ./AntiDoSCLI.py --interactive
    ```
  De esta forma, el script nos pedirá, de manera interactiva, los datos necesarios para montar la aplicación (Servidor a usar, rutas de los logs, archivo de configuración, etc.)

    Para más información acerca del almacenamiento y modificación de variables globales, consulta [este apartado](#almacenamiento-y-modificacióin-de-las-variables-globales).
- **Tomando argumentos**. También podemos pasar las variables necesarias mediante argumentos. Los argumentos disponibles de la herramienta se pueden consultar ejecutando:
    ```./AntiDoSCLI.py --help```:

    ```txt
      --server SERVER       Servidor en uso (Apache/Nginx)
      --ban-path BAN_PATH   Ruta de archivo de bans
      --log-path LOG_PATH   Ruta de archivo de logs
      --config-path CONFIG_PATH
                            Ruta de archivo de configuración del servidor
      --telegram-user TELEGRAM_USER
                            Usuario de Telegram
      --database-file DATABASE_FILE
                            Archivo de base de datos
  ```
  Si no se pasa alguno de esos argumentos, el valor para la respectiva variable se intentará tomar del archivo `.env`. En caso de que alguna variable necesaria no se haya proporcionado, el programa mostrará un mensaje de error y se cerrará. Para más información acerca del almacenamiento y modificación de variables globales, consulta [este apartado](#almacenamiento-y-modificacióin-de-las-variables-globales).

    A modo de ejemplo, si queremos ejecutar el programa proporcionando: servidor a usar, archivo de baneos, archivo de configuración y archivo de logs (en el ejemplo, para Apache), podríamos ejeuctar:

    ```bash
    ./AntiDoSCLI.py --server apache --ban-path /var/www/html/.htaccess --config-path /etc/apache2/apache2.conf --log-path /var/log/apache2/access.log
  ```

  
### Interfaz Gráfica (GUI)

## Conexión por Telegram

## Almacenamiento y modificacióin de las variables globales

Anti-DOS trabaja principalmente con estas variables:

- **SERVER**. Indica el servidor que se va a usar. En la versión actual, sólo se aceptan APACHE y NGINX
- **BAN_PATH**. Indica la ruta al archivo que usa el servidor para realizar los baneos a la IPs que estén atacando el servicio
- **CONFIG_PATH**. Indica la ruta al archivo de configuración del servidor
- **LOG_PATH**. Indica la ruta al archivo de logs de la web (access.log)
- **DATABASE_FILE**. Para implementar persistencia en el programa, este trabaja con **SQLite**. Por defecto, se crea un archivo llamado `ip_bans.db`, pero puede modificarse.
- **TELEGRAM_USER**. Si has seguido las instrucciones de [Conexión con Telegram](#conexión-por-telegram) y has configurado tu nombre de usuario, se almacenará en esta variable.

Cuando se modifican algunas de estas variables **desde la aplicación**, se ejecuta el script `setup.sh`. Lo que hace este script es asignar los permisos correspondientes a los archivos que lo necesiten.

> [!WARNING]
> Si vas a modificar alguna de estas variables del `.env` modificando el archivo en sí, asegúrate de ejecutar el script `setup.sh`.



## Contribución

Las contribuciones son bienvenidas! Si deseas mejorar esta herramienta, abre un issue o crea un pull request.

## Licencia

Este proyecto está bajo la [Licencia MIT](LICENSE).
