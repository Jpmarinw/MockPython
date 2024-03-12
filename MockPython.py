import requests
import smtplib
import unittest

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from unittest.mock import patch, ANY

def enviar_email(servidor_smtp, porta_smtp, remetente, destinatario, assunto, corpo):

    mensagem = MIMEMultipart()
    mensagem['From'] = remetente  
    mensagem['To'] = destinatario  
    mensagem['Subject'] = assunto  
    mensagem.attach(MIMEText(corpo, 'plain'))  

    
    servidor = smtplib.SMTP(servidor_smtp, porta_smtp)
    servidor.starttls()  
    servidor.login(remetente, "MinhaSenha") 
    texto = mensagem.as_string()  
    servidor.sendmail(remetente, destinatario, texto)  
    servidor.quit()  

class TesteEmail(unittest.TestCase):

    @patch('smtplib.SMTP')  
    def test_enviar_email(self, mock_smtp):
        instancia = mock_smtp.return_value 

        enviar_email("smtp.example.com", 587, "meuemail@example.com", "seuemail@example.com", "Assunto", "Conteúdo do E-mail")

        mock_smtp.assert_called_with("smtp.example.com", 587)

        instancia.starttls.assert_called_with()
        instancia.login.assert_called_with("meuemail@example.com", "MinhaSenha")  
        instancia.sendmail.assert_called_with("meuemail@example.com", "seuemail@example.com", ANY)  
        instancia.quit.assert_called_with()  

if __name__ == '__main__':
    unittest.main() 
