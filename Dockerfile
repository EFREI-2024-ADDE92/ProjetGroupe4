FROM python:3.8-slim

WORKDIR /app

COPY modelApi.py  ./
COPY requirements.txt ./
COPY iris_model.pkl ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "modelApi.py"]