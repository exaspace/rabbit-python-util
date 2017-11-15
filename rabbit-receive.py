#!/usr/bin/env python3

import pika, sys, time
import argparse, pprint

parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default='localhost')
parser.add_argument('--queue', type=str)
parser.add_argument('--exchange', type=str, help="""
    Create an anonymous queue bound to this exchange and consume (use for pubsub)""")
parser.add_argument('--durable', default=False, action='store_true', help="""
    If specifying --exchange you can specify durability also""")
parser.add_argument('--count', type=int, default=-1, help="""
    Consume specific number of messages then exit""")
parser.add_argument('--delay_ms', type=int, default=-1, help="""
    Delay in milliseconds between each acknowledgement.""")
parser.add_argument('--summary', action='store_true')
parser.add_argument('--routing_key', type=str, default='', help="""
    If binding to an exchange, use this routing key""")

args = parser.parse_args()
if not args.queue and not args.exchange:
    parser.print_help()
    sys.exit(1)

connection = pika.BlockingConnection(pika.ConnectionParameters(args.host))
channel = connection.channel()

if args.exchange is not None and args.queue is not None:
    print("Declaring queue={} durable={}".format(args.queue, args.durable))
    channel.queue_declare(queue=args.queue, durable=args.durable)
    print("Binding queue to exchange {} with routing key {}".format(args.exchange, args.routing_key))
    channel.queue_bind(exchange=args.exchange, queue=args.queue, routing_key=args.routing_key)
    queue_name = args.queue
elif args.exchange is not None:
    print("Declaring exclusive queue")
    result = channel.queue_declare(exclusive=True, auto_delete=True)
    queue_name = result.method.queue
    print("Binding queue to exchange {} with routing key {}".format(args.exchange, args.routing_key))
    channel.queue_bind(exchange=args.exchange, queue=queue_name, routing_key=args.routing_key)
else:
    queue_name = args.queue

consumed_count = 0

def callback(ch, method, properties, body):
    global consumed_count
    consumed_count += 1
    if not args.summary:
         print(body)
    else:
        print("{} {}".format(consumed_count, body), end='\r', flush=True)

    ch.basic_ack(method.delivery_tag)

    if args.count != -1 and consumed_count >= args.count:
        ch.close()
        return
    if args.delay_ms > 0:
        time.sleep(args.delay_ms * 0.001)


channel.basic_consume(callback, queue=queue_name, no_ack=False)
channel.start_consuming()
connection.close()
