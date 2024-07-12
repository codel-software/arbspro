import requests
def enviar_mensagem_telegram(message):
    #Token do bot
    TOKEN = '6618204024:AAEsg24VzAY_7SMXldYf09WZxN0_0NO3FQ4'
    # Chat ID TESTE PARTICULAR
    CHAT_ID = '-4265272042'

    # Chat ID TESTE Nicolas
    # CHAT_ID = '-4191607643'
   

    url = f'https://api.telegram.org/bot{TOKEN}/sendMessage'

    data = {
        'chat_id': CHAT_ID,
        'text': message,
        'parse_mode': 'Markdown'
    }

    response = requests.post(url, data=data)
    if response.status_code == 200:
        print('Mensagem enviada com sucesso!')
    else:
        print('Falha ao enviar mensagem:', response.text)
