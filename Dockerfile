ARG PYTHON_VERSION=3.8

FROM tiangolo/uvicorn-gunicorn:python${PYTHON_VERSION}

LABEL maintainer="Shinuk Yi<wook3024@gmail.com>"

RUN groupadd -r appuser -g 1000 && \
    useradd -u 1000 -r -g appuser -s /sbin/nologin -c "Docker image user" appuser

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PYTHONPATH /workspace

COPY . /workspace

WORKDIR /workspace
RUN pip install --upgrade pip

RUN pip install pip-tools && \
    pip-sync requirements/dev.txt

USER appuser

ENTRYPOINT [ "sh", "run_server.sh"]
