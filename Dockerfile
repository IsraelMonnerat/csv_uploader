FROM python:3.10.11-slim

WORKDIR /backend

RUN apt-get update && apt-get install -y postgresql-client libpq-dev

COPY ./backend .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8150

CMD ["uvicorn", "src.app:app", "--host", "0.0.0.0", "--port", "8150"]