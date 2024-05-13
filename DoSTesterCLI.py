import AntiDOSWeb
import config
import sys, signal
import argparse
import os
from dotenv import load_dotenv, set_key
from simple_term_menu import TerminalMenu


def def_handler(sig, frame):
    print("\n\n[!] Saliendo forzadamente...\n")
    sys.exit(1)


signal.signal(signal.SIGINT, def_handler)

def banner():
    print()
    print(" █████╗ ███╗   ██╗████████╗██╗      ██████╗  ██████╗ ███████╗")
    print("██╔══██╗████╗  ██║╚══██╔══╝██║      ██╔══██╗██╔═══██╗██╔════╝")
    print("███████║██╔██╗ ██║   ██║   ██║█████╗██║  ██║██║   ██║███████╗")
    print("██╔══██║██║╚██╗██║   ██║   ██║╚════╝██║  ██║██║   ██║╚════██║")
    print("██║  ██║██║ ╚████║   ██║   ██║      ██████╔╝╚██████╔╝███████║")
    print("╚═╝  ╚═╝╚═╝  ╚═══╝   ╚═╝   ╚═╝      ╚═════╝  ╚═════╝ ╚══════╝")
    print()
    print("Creado por:")
    print("    @M3RINOOOOO")
    print("    @manbolq")
    print("-- KakiTeam --")


def parseArgs():
    parser = argparse.ArgumentParser(
        description=
        'Procesamiento de los argumentos.\nSi no se pasa algún argumento se cogerá el valor que hay en el archivo .env'
    )
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument(
        '--interactive',
        action='store_true',
        help=
        'Modo interactivo. Si está presente, se ignoran los demás argumentos')
    parser.add_argument('--server', help='Servidor en uso (Apache/Nginx)')
    parser.add_argument('--ban-path', help='Ruta de archivo de bans')
    parser.add_argument('--log-path', help='Ruta de archivo de logs')
    parser.add_argument('--config-path',
                        help='Ruta de archivo de configuración del servidor')
    parser.add_argument('--telegram-user', help='Usuario de Telegram')
    parser.add_argument('--database-file',
                        default="ip_bans.db",
                        help='Archivo de base de datos')
    return parser.parse_args()


def main():
    banner()

    load_dotenv()

    args = parseArgs()

    if args.interactive:
        try:
            menu = TerminalMenu(config.SERVERS,
                                title="[+] Selecciona el servidor:")
            indice = menu.show()
            server = config.SERVERS[indice]
            print(f"[-] SERVER: {server}")
            set_key(".env", "SERVER", server)

            if config.SERVERS[indice] == "APACHE":
                ## PEDIR ARCHIVO DE LOGS
                menu = TerminalMenu(
                    config.APACHE_LOG_PATHS + ["Ruta personalizada"],
                    title=
                    "[+] Selecciona el archivo de logs\n[*] Las rutas de logs más comunes son:"
                )
                indice = menu.show()

                if indice == len(config.APACHE_LOG_PATHS):
                    log_path = input("Introduce la ruta del log: ")
                else:
                    log_path = config.APACHE_LOG_PATHS[indice]

                print(f"[-] Archivo de logs: {log_path}")
                set_key(".env", "LOG_PATH", log_path)

                ## PEDIR ARCHIVO DE BANS

                menu = TerminalMenu(
                    [config.APACHE_BAN_PATH, "Ruta personalizada"],
                    title=
                    "[+] Selecciona el archivo de baneos de Apache\n[*] Debe ser el archivo .htaccess de la ruta principal del servidor"
                )
                indice = menu.show()

                if indice == 1:
                    ban_path = input(
                        "Introduce la ruta del archivo de baneos: ")
                else:
                    ban_path = config.APACHE_BAN_PATH

                print(f"[-] Archivo de baneos: {ban_path}")
                set_key(".env", "BAN_PATH", ban_path)

                ## PEDIR ARCHIVO DE CONFIGURACION

                menu = TerminalMenu(
                    [config.APACHE_CONFIG_PATH, "Ruta personalizada"],
                    title=
                    "[+] Selecciona el archivo de configuración de Apache\n[*] Suele estar en la ruta:"
                )
                indice = menu.show()

                if indice == 1:
                    config_path = input(
                        "Introduce la ruta del archivo de configuración: ")
                else:
                    config_path = config.APACHE_CONFIG_PATH

                print(f"[-] Archivo de configuración: {config_path}")
                set_key(".env", "CONFIG_PATH", config_path)

            else:
                ## PEDIR ARCHIVO DE LOGS
                menu = TerminalMenu(
                    config.NGINX_LOG_PATHS + ["Ruta personalizada"],
                    title=
                    "[+] Selecciona el archivo de logs\n[*] Las rutas de logs más comunes son:"
                )
                indice = menu.show()

                if indice == len(config.NGINX_LOG_PATHS):
                    log_path = input("Introduce la ruta del log: ")
                else:
                    log_path = config.NGINX_LOG_PATHS[indice]

                print(f"[-] Archivo de logs: {log_path}")
                set_key(".env", "LOG_PATH", log_path)

                ## PEDIR ARCHIVO DE BANS

                menu = TerminalMenu(
                    config.NGINX_BAN_PATH + ["Ruta personalizada"],
                    title=
                    "[+] Selecciona el archivo de baneos de Nginx\n[*] Es el mismo que el archivo de configuración"
                )
                indice = menu.show()

                if indice == len(config.NGINX_BAN_PATH):
                    ban_path = input(
                        "Introduce la ruta del archivo de baneos: ")
                else:
                    ban_path = config.NGINX_BAN_PATH[indice]

                print(f"[-] Archivo de baneos: {ban_path}")
                set_key(".env", "BAN_PATH", ban_path)

                ## ARCHIVO DE CONFIGURACION (Es el mismo que el de baneos)

                config_path = ban_path
                print(f"[-] Archivo de configuración de Nginx: {config_path}")
                set_key(".env", "CONFIG_PATH", config_path)

            ## PEDIR ARCHIVO DE BASE DE DATOS

            menu = TerminalMenu(
                [config.DATABASE_FILE, "Ruta personalizada"],
                title=
                "[+] Selecciona el archivo de base de datos\n[*] Sugerencia:")
            indice = menu.show()

            if indice == 1:
                database_file = input(
                    "Introduce el nombre del archivo de base de datos: ")
            else:
                database_file = config.DATABASE_FILE

            print(f"[-] Archivo de base de datos: {database_file}")
            set_key(".env", "DATABASE_FILE", database_file)

            ## PEDIR USUARIO DE TELEGRAM

            menu = TerminalMenu(
                ["Saltar", "Introducir usuario"],
                title=
                "[+] Introduce tu usuario de Telegram si quieres recibir notificaciones"
            )
            indice = menu.show()

            telegram_user = None
            if indice == 1:
                telegram_user = input("Introduce tu usuario de Telegram: ")

            if telegram_user:
                print(f"[-] Usuario de Telegram: {telegram_user}")
                set_key(".env", "TELEGRAM_USER", telegram_user)

            anti_dos = AntiDOSWeb.AntiDOSWeb(server, config_path, log_path,
                                             ban_path, "%d/%b/%Y:%H:%M:%S %z",
                                             database_file, telegram_user)
            print("\n[+] Monitorizando...")
            anti_dos.monitor()

        except Exception as e:
            print("\n[!] Saliendo...")
            sys.exit(1)
    else:
        server = args.server.lower() if args.server else os.getenv("SERVER")
        ban_path = args.ban_path if args.ban_path else os.getenv("BAN_PATH")
        log_path = args.log_path if args.log_path else os.getenv("LOG_PATH")
        config_path = args.config_path if args.config_path else os.getenv(
            "CONFIG_PATH")
        database_file = args.database_file if args.database_file else os.getenv(
            "DATABASE_FILE")
        telegram_user = args.telegram_user if args.telegram_user else os.getenv(
            "TELEGRAM_USER")

        faltan_args_obligatorios = not server or not ban_path or not log_path or not config_path

        print("\n[+] Usando los siguientes datos:")
        print(f"[-] Server: {server if server else 'NO ESPECIFICADO'}")
        print(
            f"[-] Archivo de baneos: {ban_path if ban_path else 'NO ESPECIFICADO'}"
        )
        print(
            f"[-] Archivo de logs: {log_path if log_path else 'NO ESPECIFICADO'}"
        )
        print(
            f"[-] Archivo de configuración: {config_path if config_path else 'NO ESPECIFICADO'}"
        )
        print(
            f"[-] Archivo de base de datos: {database_file if database_file else 'ip_bans.db'}"
        )
        print(
            f"[-] Usuario de Telegram: {telegram_user if telegram_user else 'NO ESPECIFICADO'}"
        )

        if server:
            set_key(".env", "SERVER", server)
        if ban_path:
            set_key(".env", "BAN_PATH", ban_path)
        if log_path:
            set_key(".env", "LOG_PATH", log_path)
        if database_file:
            set_key(".env", "DATABASE_FILE", database_file)
        if config_path:
            set_key(".env", "CONFIG_PATH", config_path)
        if telegram_user:
            set_key(".env", "TELEGRAM_USER", telegram_user)

        if faltan_args_obligatorios:
            print("\n[!] ATENCION")
            print(
                "[!] os argumentos SERVER, BAN_PATH, LOG_PATH y CONFIG_PATH son obligatorios. Asegúrate de asignarles un valor"
            )
            print("[!] Saliendo...")
            sys.exit(1)

        anti_dos = AntiDOSWeb.AntiDOSWeb(server, log_path, config_path,
                                         ban_path, "%d/%b/%Y:%H:%M:%S %z",
                                         database_file, telegram_user)
        print("\n[+] Monitorizando...")
        anti_dos.monitor()


if __name__ == "__main__":
    main()

    # anti_dos = AntiDOSWeb.AntiDOSWeb(config.MAIN_SERVER, config.MAIN_LOG_PATH, config.MAIN_BAN_PATH, "%d/%b/%Y:%H:%M:%S %z", "ip_bans.db", config.TELEGRAM_USERNAME)
    # anti_dos.monitor()
