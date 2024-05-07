import requests

def enviarAvisoDos(username,ip):
    TOKEN = "6831206350:AAEiBtWC_phGRl90D0vKI6FmAsNt0E5FeQE"
    url = f"https://api.telegram.org/bot{TOKEN}/getUpdates"
    request = requests.get(url).json()

    for result in request['result']:
        message = result['message']
        if 'from' in message and 'username' in message['from'] and message['from']['username'] == username:
            chat_id = message['chat']['id']

    message = "Se ha detectado un ataque DOS proveniente de la IP: " + ip
    url = f"https://api.telegram.org/bot{TOKEN}/sendMessage?chat_id={chat_id}&text={message}"
    requests.get(url).json()
