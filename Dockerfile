FROM python:latest

RUN mkdir -p /atopile/src/atopile

COPY README.md pyproject.toml /atopile/
COPY src/atopile /atopile/src/atopile

RUN pip install /atopile"[dev,test,docs]"
