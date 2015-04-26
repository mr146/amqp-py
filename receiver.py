#!/usr/bin/env python
import pika
import sys
import time
from contract_pb2 import Request
import subprocess

def on_request(ch, method, properties, body):
	print('got something')
	request = Request()
	request.ParseFromString(body)
	client_id = request.client_id
	print(client_id)
	content = request.content.encode('utf8')
	echo_pr = subprocess.Popen(['echo', content], stdout = subprocess.PIPE)
	result_pr = subprocess.Popen(['mystem', '-gnid'], stdin = echo_pr.stdout, stdout = subprocess.PIPE)
	result = result_pr.communicate()[0]
	time.sleep(5)
	channel.basic_publish(exchange = 'response_ex', routing_key = client_id, body = result)

connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
channel = connection.channel()

channel.exchange_declare(exchange = 'request_ex', type = 'direct')
request_queue = channel.queue_declare(queue = 'request_queue')
channel.queue_bind(exchange = 'request_ex', queue = 'request_queue', routing_key = '')

channel.exchange_declare(exchange = 'response_ex', type = 'direct')

channel.basic_consume(on_request, queue = 'request_queue')
channel.start_consuming()