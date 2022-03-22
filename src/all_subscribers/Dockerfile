FROM python:3.8-alpine

COPY . .

RUN pip install --no-cache-dir -r requirements.txt

ENTRYPOINT [ "python" ]

CMD ["all_message.py"]