import imaplib
import email
from twilio.rest import Client

# Configurações do servidor de e-mail
imap_server = 'imap.example.com'
username = 'seu_email@example.com'
password = 'sua_senha'

# Configurações do Twilio
account_sid = 'seu_account_sid'
auth_token = 'seu_auth_token'
twilio_number = 'seu_numero_twilio'
receiver_number = 'numero_whatsapp_destinatario'

# Conectar ao servidor de e-mail
mail = imaplib.IMAP4_SSL(imap_server)
mail.login(username, password)
mail.select('inbox')

# Procurar por e-mails não lidos
status, response = mail.search(None, '(UNSEEN)')

if status == 'OK':
    email_ids = response[0].split()

    for email_id in email_ids:
        # Obter o e-mail
        status, response = mail.fetch(email_id, '(RFC822)')
        if status == 'OK':
            raw_email = response[0][1]
            msg = email.message_from_bytes(raw_email)

            # Verificar se o e-mail é de interesse
            if 'assunto_de_interesse' in msg['Subject']:
                # Enviar notificação pelo WhatsApp
                client = Client(account_sid, auth_token)
                message = client.messages.create(
                    body="Você recebeu um e-mail importante!",
                    from_=twilio_number,
                    to=receiver_number
                )
                print("Notificação enviada para o WhatsApp.")
else:
    print("Erro ao conectar ao servidor de e-mail.")

# Fechar a conexão com o servidor de e-mail
mail.logout()
