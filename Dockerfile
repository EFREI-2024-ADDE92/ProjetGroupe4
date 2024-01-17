FROM python:3.9-alpine

WORKDIR /app

COPY modelApi.py ./
COPY requirements.txt ./
COPY iris_model ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "modelApi.py"]