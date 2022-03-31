FROM python:3.8-buster

COPY . .
RUN pip install --upgrade pip
RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT ["python","./post_json_fuzzer.py"]
