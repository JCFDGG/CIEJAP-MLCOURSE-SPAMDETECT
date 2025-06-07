from flask import Flask, request
from werkzeug.exceptions import HTTPException, BadRequest, InternalServerError
import json
import pickle
import logging

# Configuração do logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s %(message)s',
    handlers=[logging.StreamHandler()]
)

with open('spam_detect_nb.pkl', 'rb') as f_model:
    modelo = pickle.load(f_model)

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        logging.info("Recebendo requisição para /predict")
        data = request.get_json()
        if not data or 'body' not in data:
            logging.warning("Corpo da requisição inválido ou campo 'body' ausente")
            raise BadRequest("Requisição inválida: campo 'body' é obrigatório.")

        texto_email = data.get('body')
        if not isinstance(texto_email, list):
            logging.warning("O campo 'body' não é uma lista")
            raise BadRequest("O campo 'body' deve ser uma lista de textos.")

        logging.info(f"Textos recebidos para predição: {texto_email}")

        predicao = modelo.predict(texto_email)

        results = [
            {"texto": texto, "spam": True if pred == 1 else False}
            for texto, pred in zip(texto_email, predicao)
        ]

        logging.info(f"Resultado da predição: {results}")

        return json.dumps({'Resultado Modelo': results})
    except BadRequest as e:
        logging.error(f"Erro de requisição: {str(e)}")
        raise HTTPException(description="Erro na requisição: verifique os dados enviados.", response=None)
    except Exception as e:
        logging.exception("Erro interno no servidor")
        raise InternalServerError(description="Erro interno no servidor. Tente novamente mais tarde.")

@app.errorhandler(HTTPException)
def handle_http_exception(e):
    response = e.get_response()
    response.data = json.dumps({
        "erro": e.description
    }, ensure_ascii=False)
    response.content_type = "application/json"
    return response, e.code

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
