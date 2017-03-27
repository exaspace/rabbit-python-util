#!/usr/bin/env python3

import argparse, pika, sys, time

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default='localhost')
parser.add_argument('--queue', type=str)
parser.add_argument('--exchange', type=str)
parser.add_argument('--routing_key', type=str, default='')
parser.add_argument('--message', type=str)
parser.add_argument('--durable', default=False, action='store_true')
parser.add_argument('--count', type=int, default=1)
parser.add_argument('--delay_ms', type=int, default=0)

args = parser.parse_args()
if args.message is None or args.exchange is None:
    parser.print_help()
    exit(1)

connection = pika.BlockingConnection(pika.ConnectionParameters(args.host))
channel = connection.channel()

if args.queue is not None and args.durable is not None:
    print("Declaring queue and binding to exchange")
    channel.queue_declare(queue=args.queue, durable=args.durable)
    channel.queue_bind(exchange=args.exchange, queue=args.queue, routing_key=args.routing_key)

for i in range(1, args.count + 1):
    if args.count == 1:
        body = args.message
    else:
        body = "{}{}".format(args.message, i)
    channel.basic_publish(exchange=args.exchange, routing_key=args.routing_key, body=body)
    print("Sent {}".format(body))
    if args.delay_ms > 0:
        time.sleep(args.delay_ms/1000.0)
connection.close()
