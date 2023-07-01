FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src .

CMD [ "uvicorn", "src.main:app", "--host", "0.0.0.0", "--reload"]

