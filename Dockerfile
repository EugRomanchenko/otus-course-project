FROM python:3.12-bookworm as requirements-stage

WORKDIR /tmp

RUN pip install "poetry==1.6.1"
COPY ./poetry.lock* ./pyproject.toml /tmp/
RUN poetry export -f requirements.txt --output requirements.txt --without-hashes

FROM python:3.12-bookworm

ENV PYTHONUNBUFFERED=1

WORKDIR /code

COPY --from=requirements-stage /tmp/requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt