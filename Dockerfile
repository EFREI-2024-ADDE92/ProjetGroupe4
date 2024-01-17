FROM python:3.9-alpine

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["python", "modelApi.py"]