import imaplib
import email
from email.header import decode_header
from flask import Flask, send_file
import os

app = Flask(__name__)

def get_unread_emails(username, password, imap_server):
    emails = []
    try:
        # Conecta ao servidor IMAP e autentica
        mail = imaplib.IMAP4_SSL(imap_server)
        mail.login(username, password)
        
        # Seleciona a caixa de entrada
        mail.select("inbox")
        
        # Procura os e-mails não lidos
        status, messages = mail.search(None, 'UNSEEN')
        email_ids = messages[0].split()
        
        for email_id in email_ids:
            # Busca o conteúdo do e-mail
            status, msg_data = mail.fetch(email_id, '(RFC822)')
            for response_part in msg_data:
                if isinstance(response_part, tuple):
                    # Decodifica o e-mail
                    msg = email.message_from_bytes(response_part[1])
                    
                    # Pega o remetente e assunto
                    from_ = msg.get("From")
                    subject, encoding = decode_header(msg.get("Subject"))[0]
                    if isinstance(subject, bytes):
                        subject = subject.decode(encoding if encoding else "utf-8")
                    
                    # Concatena remetente, assunto e conteúdo simplificado
                    body = ""
                    if msg.is_multipart():
                        for part in msg.walk():
                            if part.get_content_type() == "text/plain":
                                body = part.get_payload(decode=True).decode("utf-8", errors="ignore")
                                break
                    else:
                        body = msg.get_payload(decode=True).decode("utf-8", errors="ignore")
                    
                    emails.append(f"From: {from_}\nSubject: {subject}\n\n{body}\n{'='*50}")
        
        mail.logout()
    except Exception as e:
        emails.append(f"Erro ao acessar os e-mails: {e}")
    
    return emails

@app.route("/get_unread_emails")
def download_unread_emails():
    username = "augustosaboiaestudos@gmail.com"  # Substitua pelo seu e-mail
    password = "uwll zpxy pden wluh"  # Substitua pela sua senha de aplicativo
    imap_server = "imap.gmail.com"  # Altere conforme seu provedor

    emails = get_unread_emails(username, password, imap_server)
    
    file_path = "unread_emails.txt"
    with open(file_path, "w") as file:
        for email_content in emails:
            file.write(email_content + "\n")
    
    return send_file(file_path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
