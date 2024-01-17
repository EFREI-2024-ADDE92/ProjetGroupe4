FROM python:3.9-alpine

WORKDIR /app

COPY modelApi.py  ./
COPY requirements.txt ./
COPY iris_model.pkl ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python3", "modelApi.py"]