FROM python:3.12.6-slim AS base
SHELL ["/bin/bash", "-c"]

# Set JWT_SECRET to something thats super secure
ENV JWT_SECRET SUPERSECUREJWTSECRETDONOTEXPOSE

# Use /usr/src/app as the working directory of the container
WORKDIR /usr/src/app
COPY . /usr/src/app

# Download a C compiler for uWSGI
RUN apt-get -y update && apt-get install -y gcc

# Create and use python venv
RUN python3 -m venv .venv
RUN source .venv/bin/activate

# Install deps
RUN pip install -r requirements.txt

EXPOSE 5000
CMD ["uwsgi", "--ini", "/usr/src/app/uwsgi.ini"]
