FROM python:3.8-alpine

# Set default environment variables
ENV PYTHONUNBUFFERED 1
ENV LANG C.UTF-8

# Arguments for SSH setup
ARG ssh_prv_key
ARG ssh_pub_key

# Install dependencies
RUN apk add  postgresql-libs && \
    apk add --virtual build-dependencies g++ curl git openssh-client musl-dev libffi-dev openssl-dev postgresql-dev make
# RUN apk add --virtual build-dependencies curl git

# Install Poetry
RUN curl -sSL https://raw.githubusercontent.com/sdispater/poetry/master/get-poetry.py | python
ENV PATH "/root/.poetry/bin:/opt/venv/bin:${PATH}"

# Authorize SSH Host
RUN mkdir -p /root/.ssh && \
    chmod 0700 /root/.ssh && \
    ssh-keyscan github.com > /root/.ssh/known_hosts

# Add the keys and set permissions
RUN printf "$ssh_prv_key" > /root/.ssh/id_rsa && \
    printf "$ssh_pub_key" > /root/.ssh/id_rsa.pub && \
    chmod 600 /root/.ssh/id_rsa && \
    chmod 600 /root/.ssh/id_rsa.pub

# Convert windows newline to unix newline
RUN sed -i 's/\r$//g' /root/.ssh/id_rsa

RUN printf "host github.com\n\tHostName github.com\n\tIdentityFile ~/.ssh/id_rsa\n\tUser git\n\tIdentitiesOnly yes\n" > /root/.ssh/config

# Create code directory and copy code
RUN mkdir /code
WORKDIR /code
ADD . /code/

# Install only runtime dependencies (no dev dependencies)
RUN poetry install --no-dev

# Remove build dependencies
RUN apk del build-dependencies

EXPOSE 50000

CMD poetry run python main.py --register --registrar-url "http://morpho-crypto-eureka:8761/eureka"