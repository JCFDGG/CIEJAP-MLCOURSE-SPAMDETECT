FROM python:latest

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY api_modelo.py .

COPY spam_detect_nb.pkl .


EXPOSE 3141

CMD ["python", "api_modelo.py"]