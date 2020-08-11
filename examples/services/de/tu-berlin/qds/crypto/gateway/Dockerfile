FROM python:3.8-alpine

# Set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

# Install Poetry
# RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
# ENV PATH "/root/.poetry/bin:/opt/venv/bin:${PATH}"

# Install dependencies
RUN apk add --virtual build-dependencies g++ libffi-dev openssl-dev

RUN pip install --no-cache poetry

# Create code directory and copy code
RUN mkdir /code
WORKDIR /code
ADD . /code/

# Install only runtime dependencies (no dev dependencies)
RUN poetry install --no-dev

# Remove build dependencies
RUN apk del build-dependencies

EXPOSE 50000

CMD poetry run python main.py --register --registrar-url ${REGISTRAR_URL}