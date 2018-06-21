FROM python:3-alpine3.6
WORKDIR /usr/src/app

RUN apk update && apk add \
    bash \
    gcc \
    musl-dev \
    libffi-dev \
    openssl \
    openssl-dev \
    libxml2-dev \
    libxslt-dev \
    zip


# Copy requirements.txt and run pip install as a separate step so that
# it doesn't get re-run every time the code changes.
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt

COPY . .

CMD ["python3", "check_workers.py"]
