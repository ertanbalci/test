from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField 
from wtforms.validators import InputRequired, Email, EqualTo, Length 

class yForm(FlaskForm): #yeni Üye Formu     
     username = StringField("Kullanıcı Adı" ,
                            [InputRequired(),
                             Length(min=3, message="İsim en az 3 karakter olmalı")])
     eposta = StringField("e-posta adresiniz" ,
                          validators=[InputRequired(),
                                      Email(message="Geçersiz E-Posta Adresi")])
     parola = PasswordField("Parolanız",
                            validators=[InputRequired(),
                                        Length(min=8, max=16,
                                               message="Parola 8-16 karakter olmalı")])
     cparola = PasswordField("Parolanız Tekrar",
                             validators=[EqualTo("parola",
                                                 message="Girdiğiniz parolalar farklı")])
     submit = SubmitField("Gönder")
     
class gForm(FlaskForm): # Üye giriş Formu
     username   = StringField("Kullanıcı Adı" ,[InputRequired()])
                                                           
     parola = PasswordField("Parolanız", validators=[InputRequired()])

     submit = SubmitField("Gönder")

