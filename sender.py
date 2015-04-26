#!/usr/bin/env python
import pika
import uuid
import sys

sid = str(uuid.uuid4())
print sid

def on_response(ch, methon, properties, body):
	print(body)
	channel.close()

connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
channel = connection.channel()
channel.exchange_declare(exchange = 'request_ex', type = 'direct')
channel.basic_publish(exchange = 'request_ex', routing_key = '', body = sid)
connection.close()


connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
channel = connection.channel()

channel.exchange_declare(exchange = 'response_ex', type = 'direct')
result = channel.queue_declare(exclusive = True)
queue_name = result.method.queue
channel.queue_bind(exchange = 'response_ex', queue = queue_name, routing_key = sid)

channel.basic_consume(on_response, queue = queue_name)
channel.start_consuming()