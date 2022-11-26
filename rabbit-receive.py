#!/usr/bin/env python3

import pika, sys, time
import argparse, pprint
import ssl
import logging

logging.basicConfig(level=logging.WARNING)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--host', type=str, default='localhost')
    parser.add_argument('--port', type=int, default=5672)
    parser.add_argument('--vhost', type=str, default='/')

    parser.add_argument('--username', type=str, default="guest")
    parser.add_argument('--password', type=str, default="guest")
    parser.add_argument('--cacert', type=str, default=None)

    parser.add_argument('--queue', type=str)

    parser.add_argument('--exchange', type=str, help="""

        Create an anonymous queue bound to this exchange and consume (use for pubsub)""")

    parser.add_argument('--durable', default=False, action='store_true', help="""

        If specifying --exchange you can specify durability also""")

    parser.add_argument('--count', type=int, default=-1, help="""

        Consume specific number of messages then exit""")

    parser.add_argument('--delay_ms', type=int, default=-1, help="""

        Delay in milliseconds between each acknowledgement.""")

    parser.add_argument('--summary', action='store_true', help="""

        Print only a single line summary of progress (instead of printing each message)""")

    parser.add_argument('--routing_key', type=str, default='', help="""

        If binding to an exchange, use this routing key""")

    args = parser.parse_args()
    if not args.queue and not args.exchange:
        parser.print_help()
        sys.exit(1)
    return args

args = parse_args()
if args.cacert:
    ssl_options= dict(
            ssl_version=ssl.PROTOCOL_TLSv1_2,
            ca_certs=args.cacert,
            cert_reqs=ssl.CERT_NONE) # TODO allow cert validation
else:
    ssl_options = None

credentials = pika.credentials.PlainCredentials(args.username, args.password)

connect_dict = {}
connect_dict['host'] = args.host
connect_dict['port'] = args.port
connect_dict['virtual_host'] = args.vhost
connect_dict['ssl_options'] = ssl_options
connect_dict['credentials'] = credentials

connection_params = pika.ConnectionParameters(**connect_dict)
connection = pika.BlockingConnection(connection_params)
channel = connection.channel()

if args.exchange is not None and args.queue is not None:
    print("Declaring queue={} durable={}".format(args.queue, args.durable))
    channel.queue_declare(queue=args.queue, durable=args.durable)
    print("Binding queue to exchange {} with routing key {}".format(args.exchange, args.routing_key))
    channel.queue_bind(exchange=args.exchange, queue=args.queue, routing_key=args.routing_key)
    queue_name = args.queue
elif args.exchange is not None:
    print("Declaring exclusive queue")
    result = channel.queue_declare(queue="", exclusive=True, auto_delete=True)
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

print("Starting rabbit consume from queue '{}'...".format(queue_name))
channel.basic_consume(on_message_callback=callback, queue=queue_name)
channel.start_consuming()
connection.close()
