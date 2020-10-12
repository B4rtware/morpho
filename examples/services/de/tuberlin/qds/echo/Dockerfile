FROM b4rtware/morpho:latest

COPY . /service
WORKDIR /service

RUN poetry install --no-dev

EXPOSE 50000
CMD poetry run python -O main.py --register --registrar-url ${REGISTRAR_URL}