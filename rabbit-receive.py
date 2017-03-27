#!/usr/bin/env python3

import pika, sys, time
import argparse

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default='localhost')
parser.add_argument('--queue', type=str)

args = parser.parse_args()
if not args.queue or not args.host:
    parser.print_help()
else:

	def callback(ch, method, properties, body):
	    print(body)

	connection = pika.BlockingConnection(pika.ConnectionParameters(args.host))
	channel = connection.channel()
	channel.basic_consume(callback, queue=args.queue, no_ack=True)
	channel.start_consuming()
	connection.close()
