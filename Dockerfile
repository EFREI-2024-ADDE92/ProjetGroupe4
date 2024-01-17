FROM python:3.9-alpine

WORKDIR /app

COPY modelApi.py  ./
COPY requirements.txt ./
COPY iris_model.pkl ./

RUN apk add --no-cache build-base

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "modelApi.py"]