FROM python:3-alpine
WORKDIR /usr/src/app
EXPOSE 8000

RUN apk --update add --no-cache g++

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY dbutils.py .
COPY main.py .
COPY utils.py .

CMD ["python3","./main.py"] 
