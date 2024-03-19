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

    @patch('smtplib.SMTP')  #substituindo a classe SMTP pelo Mock
    def test_enviar_email(self, mock_smtp):
        instancia = mock_smtp.return_value 

        enviar_email("smtp.example.com", 587, "meuemail@example.com", "seuemail@example.com", "Assunto", "Conteúdo do E-mail")

        mock_smtp.assert_called_with("smtp.example.com", 587)

        #verificando se os métodos de instancia foram chamados corretamente
        instancia.starttls.assert_called_with()
        instancia.login.assert_called_with("meuemail@example.com", "MinhaSenha")  
        instancia.sendmail.assert_called_with("meuemail@example.com", "seuemail@example.com", ANY)  
        instancia.quit.assert_called_with() 

class TesteFalhaNaAutenticacao(unittest.TestCase): #criando a função mock pra simular o modelo

    # Teste para a função de envio de e-mail
    @patch('smtplib.SMTP') #substituindo a classe pelo Mock
    def test_enviar_email_falha_autenticacao(self, mock_smtp):
        instancia = mock_smtp.return_value
        instancia.login.side_effect = smtplib.SMTPAuthenticationError(535, b'Authentication failed') #simula uma falha na autenticação

        # Chamando a função de envio de e-mail
        with self.assertRaises(smtplib.SMTPAuthenticationError): #Verifica se há uma exceção lançada durante a chamada da função
            enviar_email("smtp.example.com", 587, "meuemail@example.com", "seuemail@example.com", "Assunto", "Conteúdo do E-mail")

        # Verificando se a função foi chamada com os argumentos corretos
        mock_smtp.assert_called_with("smtp.example.com", 587)
        instancia.starttls.assert_called_with()
        instancia.login.assert_called_with("meuemail@example.com", "MinhaSenha")
        instancia.quit.assert_not_called()

if __name__ == '__main__': #executando os testes
    unittest.main() 
