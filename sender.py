#!/usr/bin/env python
import pika
import uuid
import sys
reload(sys)
sys.setdefaultencoding("utf-8")
from contract_pb2 import Request


def on_response(ch, methon, properties, body):
	print(body)
	channel.close()

request = Request()
client_id = str(uuid.uuid4())
request.client_id = client_id
print(request.client_id)
filename = sys.argv[1]
f = open(filename, "r")
request.content = f.read().decode('utf8')

connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
channel = connection.channel()
channel.exchange_declare(exchange = 'request_ex', type = 'direct')
channel.basic_publish(exchange = 'request_ex', routing_key = '', body = request.SerializeToString())
connection.close()


connection = pika.BlockingConnection(pika.ConnectionParameters(host = 'localhost'))
channel = connection.channel()

channel.exchange_declare(exchange = 'response_ex', type = 'direct')
result = channel.queue_declare(exclusive = True)
queue_name = result.method.queue
channel.queue_bind(exchange = 'response_ex', queue = queue_name, routing_key = client_id)

channel.basic_consume(on_response, queue = queue_name)
channel.start_consuming()