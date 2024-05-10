import AntiDOSWeb
import config
import sys, signal
import argparse
import os
from dotenv import load_dotenv, set_key


def def_handler(sig, frame):
    print("\n\n[!] Saliendo forzadamente...\n")
    sys.exit(1)


signal.signal(signal.SIGINT, def_handler)


def parseArgs():
    parser = argparse.ArgumentParser(description='Procesamiento de los argumentos.\nSi no se pasa algún argumento se cogerá el valor que hay en el archivo .env')
    group = parser.add_mutually_exclusive_group(required=False)
    group.add_argument('--interactive', action='store_true', help='Modo interactivo. Si está presente, se ignoran los demás argumentos')
    parser.add_argument('--server', help='Servidor en uso (Apache/Nginx)')
    parser.add_argument('--ban-path', help='Ruta de archivo de bans')
    parser.add_argument('--log-path', help='Ruta de archivo de logs')
    parser.add_argument('--config-path', help='Ruta de archivo de configuración del servidor')
    parser.add_argument('--telegram-user', help='Usuario de Telegram')
    parser.add_argument('--database-file', default="ip_bans.db", help='Archivo de base de datos')
    return parser.parse_args()


def main():
    load_dotenv()

    args = parseArgs()

    if args.interactive:
        print("Modo interactivo activado")
    else:
        server = args.server.lower() if args.server else os.getenv("SERVER")
        ban_path = args.ban_path if args.ban_path else os.getenv("BAN_PATH")
        log_path = args.log_path if args.log_path else os.getenv("LOG_PATH")
        config_path = args.config_path if args.config_path else os.getenv("CONFIG_PATH")
        database_file = args.database_file if args.database_file else os.getenv("DATABASE_FILE")
        telegram_user = args.telegram_user if args.telegram_user else os.getenv("TELEGRAM_USER")

        faltan_args_obligatorios = not server or not ban_path or not log_path or not config_path

        print("\n[+] Usando los siguientes datos:")
        print(f"[-] Server: {server if server else 'NO ESPECIFICADO'}")
        print(f"[-] Archivo de baneos: {ban_path if ban_path else 'NO ESPECIFICADO'}")
        print(f"[-] Archivo de logs: {log_path if log_path else 'NO ESPECIFICADO'}")
        print(f"[-] Archivo de configuración: {config_path if config_path else 'NO ESPECIFICADO'}")
        print(f"[-] Archivo de base de datos: {database_file if database_file else 'ip_bans.db'}")
        print(f"[-] Usuario de Telegram: {telegram_user if telegram_user else 'NO ESPECIFICADO'}")

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
            print("[!] os argumentos SERVER, BAN_PATH y LOG_PATH son obligatorios. Asegúrate de asignarles un valor")
            print("[!] Saliendo...")
            sys.exit(1)

        anti_dos = AntiDOSWeb.AntiDOSWeb(server, log_path, ban_path, "%d/%b/%Y:%H:%M:%S %z", database_file, telegram_user)
        print("\n[+] Monitorizando...")
        anti_dos.monitor()

if __name__ == "__main__":
    main()



    # anti_dos = AntiDOSWeb.AntiDOSWeb(config.MAIN_SERVER, config.MAIN_LOG_PATH, config.MAIN_BAN_PATH, "%d/%b/%Y:%H:%M:%S %z", "ip_bans.db", config.TELEGRAM_USERNAME)
    # anti_dos.monitor()

