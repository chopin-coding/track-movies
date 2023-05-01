FROM python:3.11.3

WORKDIR /app
COPY . .

RUN pip install -r requirements.txt

ENV PORT=8080

EXPOSE 8080

CMD uvicorn --host 0.0.0.0 --port 8080 --factory api.api:create_app
