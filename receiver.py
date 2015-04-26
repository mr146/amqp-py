#!/usr/bin/env python
import pika
import sys
import time

def on_request(ch, method, properties, body):
	print('got something')
	print(body)
	time.sleep(5)
	channel.basic_publish(exchange = 'response_ex', routing_key = body, body = 'Hi, {0}!'.format(body))

connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
channel = connection.channel()

channel.exchange_declare(exchange = 'request_ex', type = 'direct')
request_queue = channel.queue_declare(queue = 'request_queue')
channel.queue_bind(exchange = 'request_ex', queue = 'request_queue', routing_key = '')

channel.exchange_declare(exchange = 'response_ex', type = 'direct')

channel.basic_consume(on_request, queue = 'request_queue')
channel.start_consuming()