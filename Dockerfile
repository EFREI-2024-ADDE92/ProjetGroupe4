FROM python:3.11-slim-bookworm
 
WORKDIR /app
 
COPY iris_model.pkl /app
COPY modelApi.py /app
COPY requirements.txt /app
 
RUN pip install --upgrade pip
RUN pip install --no-cache-dir --requirement requirements.txt
 
 
CMD ["python", "modelApi.py"]