import requests #biblioteca usada pra fazer requisições HTTP
import smtplib #biblioteca usada para enviar emails usando SMTP
import unittest #frameWork padrão em Python para testes

from email.mime.multipart import MIMEMultipart #usada para criar mensagens de e-mail com diferentes tipos de conteudo
from email.mime.text import MIMEText #usada para usar partes de texto
from unittest.mock import patch, ANY #usada para substituir objetos

def enviar_email(servidor_smtp, porta_smtp, remetente, destinatario, assunto, corpo): #criando a função modelo pra enviar email

    #criando os objetos de mensagem
    mensagem = MIMEMultipart()
    mensagem['From'] = remetente  
    mensagem['To'] = destinatario  
    mensagem['Subject'] = assunto  
    mensagem.attach(MIMEText(corpo, 'plain'))

    
    servidor = smtplib.SMTP(servidor_smtp, porta_smtp) #iniciando o servidor SMTP
    servidor.starttls() #iniciando conexão TLS
    servidor.login(remetente, "MinhaSenha") 
    texto = mensagem.as_string()  
    servidor.sendmail(remetente, destinatario, texto)  
    servidor.quit()  

class TesteEmail(unittest.TestCase): #criando a função mock pra simular a função modelo

    @patch('smtplib.SMTP')  #Substituindo a classe SMTP pelo Mock
    def test_enviar_email(self, mock_smtp):
        instancia = mock_smtp.return_value 

        enviar_email("smtp.example.com", 587, "meuemail@example.com", "seuemail@example.com", "Assunto", "Conteúdo do E-mail")

        mock_smtp.assert_called_with("smtp.example.com", 587)

        #verificando se os métodos de instancia foram chamados corretamente
        instancia.starttls.assert_called_with()
        instancia.login.assert_called_with("meuemail@example.com", "MinhaSenha")  
        instancia.sendmail.assert_called_with("meuemail@example.com", "seuemail@example.com", ANY)  
        instancia.quit.assert_called_with()  

if __name__ == '__main__':
    unittest.main() 
