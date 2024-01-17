FROM python:3.9-alpine

WORKDIR /app

COPY modelApi.py requirements.txt iris_model.pkl ./

RUN pip install --no-cache-dir -r requirements.txt

CMD ["python", "modelApi.py"]