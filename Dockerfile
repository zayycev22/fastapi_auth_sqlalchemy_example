FROM python:3.10-slim
ENV PYTHONUNBUFFERED=1

WORKDIR /app
COPY requirements.txt requirements.txt

RUN pip3 install -r requirements.txt


CMD ["python3", "-u", "main.py"]
