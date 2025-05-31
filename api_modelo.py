from flask import Flask, request
import json
import pickle

with open('spam_detect_nb.pkl', 'rb') as f_model:
    modelo = pickle.load(f_model)

app = Flask(__name__)

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.get_json()
        texto_email = data.get('body')


        predicao = modelo.predict(texto_email)

        results = [
            {"texto": texto_email, "spam": True if predicao == 1 else False}
            for texto_email, predicao in zip(texto_email, predicao)
        ]

        return json.dumps({'Resultado Modelo': results})
    except Exception as e:
        return json.dumps({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=3141)