import pika
from fastapi import FastAPI, HTTPException, Body

app = FastAPI()


def callback(ch, method, body):
    print(" [x] Received Error Messages {}".format(body))
    ch.basic_ack(delivery_tag=method.delivery_tag)

@app.get("/all")
def all_message():
    queue =  "all_messages"

    credentials = pika.PlainCredentials('user', 'PASSWORD')
    connection = pika.BlockingConnection(
    pika.ConnectionParameters("rabbitmq-headless.keda", 5672, '/', credentials)) 
    channel = connection.channel()

    channel.exchange_declare(exchange='all_message', exchange_type='direct')
    channel.queue_declare(queue=queue, durable=True, arguments={"x-queue-type": "quorum"})
    channel.queue_bind(exchange='all_message', queue=queue, routing_key='error')
    channel.queue_bind(exchange='all_message', queue=queue, routing_key='good')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, callback=callback, auto_ack=True)

    channel.start_consuming()

@app.get("/error")
def error_message():
    queue =  "error_message"

    credentials = pika.PlainCredentials('user', 'PASSWORD')
    connection = pika.BlockingConnection(
    pika.ConnectionParameters("rabbitmq-headless.keda", 5672, '/', credentials)) 
    channel = connection.channel()

    channel.exchange_declare(exchange='all_message', exchange_type='direct')
    channel.queue_declare(queue=queue, durable=True, arguments={"x-queue-type": "quorum"})
    channel.queue_bind(exchange='all_message', queue=queue, routing_key='error')
    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, callback=callback, auto_ack=True)

    channel.start_consuming()

@app.get("/good")
def good_message():
    queue =  "good_message"

    credentials = pika.PlainCredentials('user', 'PASSWORD')
    connection = pika.BlockingConnection(
    pika.ConnectionParameters("rabbitmq-headless.keda", 5672, '/', credentials)) 
    channel = connection.channel()

    channel.exchange_declare(exchange='all_message', exchange_type='direct')
    channel.queue_declare(queue=queue, durable=True, arguments={"x-queue-type": "quorum"})

    channel.queue_bind(exchange='all_message', queue=queue, routing_key='good')

    channel.basic_qos(prefetch_count=1)
    channel.basic_consume(queue=queue, callback=callback, auto_ack=True)

    channel.start_consuming()
