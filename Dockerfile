from python:3.13.11-bookworm
RUN apt-get install -f

WORKDIR /fast_flat

COPY ./pyproject.toml /fast_flat/pyproject.toml
COPY ./uv.lock /fast_flat/uv.lock

RUN pip install uv
RUN uv pip install -r pyproject.toml --system
COPY ./entrypoint.sh .
RUN sed -i 's/\r$//g' entrypoint.sh
RUN chmod +x entrypoint.sh
COPY . .