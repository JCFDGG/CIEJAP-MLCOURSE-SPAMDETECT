import requests

# URL local
url = "http://127.0.0.1:3141/predict"


email_textos = [
    "Good evening, I'm here to inform you that your account has been compromised. Please click the link below to reset your password immediately.",
    "I sent you that report you asked for, it's attached to this email.",
    "Congratulations! You've won a free vacation to the Bahamas. Click here to claim your prize.",
    "Unfortunately, we have to inform you that your application has been rejected. We wish you the best of luck in your future endeavors.",
    "As per our previous conversations: no, you have not found a proof that 2+2=44, and yes, you are still wrong. Please stop sending me emails about this.",
    "Your subscription has been renewed successfully. Thank you for being a valued customer."
]

payload = {"body": email_textos}

response = requests.post(url, json=payload)

# Verifica o resultado
if response.status_code == 200:
    lista_resposta = response.json()
    for resposta in lista_resposta['Resultado Modelo']:
        print(f"Texto: {resposta['texto']}\nSpam: {resposta['spam']}\n")

else:
    print(f"Erro: {response.status_code} - {response.text}")