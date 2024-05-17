FROM python:3-alpine

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY hash_importer.py /usr/src/app

ENTRYPOINT [ "python", "./hash_importer.py" ]