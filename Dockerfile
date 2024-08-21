FROM python:3.12

WORKDIR /app

COPY . /app/

RUN pip install --upgrade pip && \
    pip install poetry && \
    poetry config virtualenvs.create false --local

RUN poetry install --no-root
EXPOSE 8080