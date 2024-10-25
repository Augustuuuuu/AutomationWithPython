from imap_tools import MailBox, AND


usuario = 'augustosaboiaestudos@gmail.com'
senha = 'uwll zpxy pden wluh'

meu_email = MailBox('imap.gmail.com').login(usuario,senha)

# Pegar email que foram enviados para um remetente específico

lista_emails = meu_email.fetch(AND(from_="processoseletivo@sistemafibra.org.br"))

print(len(list(lista_emails)))