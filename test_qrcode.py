import smtplib
import os
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

# Paramètres de connexion 
from_email = "matheothedon@gmail.com"
password =  "gopu zgei jvjy msrh" # Utilise le mot de passe d'application ici
to_email = "mathieuakoubia@gmail.com"

# Configuration du message
subject = "Test d'envoi d'e-mail via Python"
body = "Ceci est un test pour vérifier l'envoi d'e-mail via SMTP."

message = MIMEMultipart()
message["From"] = from_email
message["To"] = to_email
message["Subject"] = subject

message.attach(MIMEText(body, "plain"))

# Envoi de l'e-mail
try:
    server = smtplib.SMTP("smtp.gmail.com", 587)
    server.starttls()  # Démarre une connexion sécurisée
    server.login(from_email, password)
    server.send_message(message)
    server.quit()
    print("E-mail envoyé avec succès!")
except Exception as e:
    print(f"Erreur lors de l'envoi de l'e-mail : {e}")
