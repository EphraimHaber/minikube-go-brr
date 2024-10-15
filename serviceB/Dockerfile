FROM python:3.12.3-alpine

WORKDIR /app

COPY requirements.txt ./requirements.txt

RUN pip install -r requirements.txt --no-cache-dir

COPY . .

ENV PYTHONUNBUFFERED=1

CMD [ "python", "t.py" ]