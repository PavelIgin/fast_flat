from python:3.9.6-buster
RUN apt-get update -y

WORKDIR /fast_flat

COPY ./pyproject.toml /fast_flat/pyproject.toml
COPY ./poetry.lock /fast_flat/poetry.lock

RUN pip install "poetry==1.4.2"
run poetry config virtualenvs.create false
run poetry install --no-interaction --no-ansi

COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' entrypoint.sh
RUN chmod +x entrypoint.sh
COPY . .