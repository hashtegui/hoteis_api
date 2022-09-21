from sql_alchemy import banco
from flask import request, url_for
from requests import post

MAILGUN_API_KEY = "0ab4048519e4facf0a41635cc2c76498-78651cec-b22e4f62"
MAILGUN_DOMAIN = 'sandbox72aad4cc05e64966935e420edf51019f.mailgun.org'
FROM_TITLE = "no-reply"
FROM_EMAIL= "no-reply@restapi.com"


class UserModel(banco.Model):
    __tablename__ = 'usuarios'

    user_id = banco.Column(banco.Integer, primary_key=True)
    login = banco.Column(banco.String(40), nullable=False, unique=True)
    senha = banco.Column(banco.String(40), nullable=False, unique=True)
    email = banco.Column(banco.String(80), nullable=False, unique=True)
    ativado = banco.Column(banco.Boolean, default=False)

    def __init__(self, login, senha, email, ativado) -> None:
        self.login = login
        self.senha = senha
        self.email = email
        self.ativado = ativado

    def json(self):
        return {
            'user_id': self.user_id,
            'login': self.login,
            'email': self.email,
            'ativado': self.ativado
        }
        
    def send_confirmation_email(self):
        link = request.url_root[:-1] + url_for('userconfirm', user_id=self.user_id)
        print(link)
        
        teste= "teste"
        
        return post(f'https://api.mailgun.net/v3/{MAILGUN_DOMAIN}/messages', auth=('api', MAILGUN_API_KEY),
                    data={'from': f'{FROM_TITLE} <{FROM_EMAIL}>',
                          'to':self.email,
                          'subject':'Confirmação de Cadastro',
                          'text':f'Confirme seu cadastro {teste} clicando no link a seguik: {link}',
                          'html': f'<html><p>Confirme seu cadastro clicando no link a seguir: <a href="{link}"></a></p></html>'
                          },)
        
        

    @classmethod
    def find_user(cls, user_id):
        user = cls.query.filter_by(user_id=user_id).first()
        if user:
            return user
        return None

    @classmethod
    def find_by_login(cls, login):
        user = cls.query.filter_by(login=login).first()
        if user:
            return user
        return None
    
    @classmethod
    def find_by_email(cls, email):
        user = cls.query.filter_by(email=email).first()
        if user:
            return user
        return None

    def save_user(self):
        banco.session.add(self)
        banco.session.commit()

    def delete_user(self):
        banco.session.delete(self)
        banco.session.commit()
