#!/usr/bin/env python3

import argparse, pika, sys, time

# TODO Fix required args display
parser = argparse.ArgumentParser()
parser.add_argument('--host', type=str, default='localhost')
parser.add_argument('--exchange', type=str)
parser.add_argument('--routing_key', type=str, default='')
parser.add_argument('--message', type=str)
parser.add_argument('--count', type=int, default=1, help="""
    Number of messages to send. Will append an incrementing integer to each message""")
parser.add_argument('--delay_ms', type=int, default=0, help="""
    Delay this amount in milliseconds between each publish call.""")
parser.add_argument('--summary', action='store_true', help="""
    Print only a single line summary of progress""")
parser.add_argument('--declare', action='store_true', help="""
    Declare the exchange""")
parser.add_argument('--type', type=str, default="direct", help="The exchange type (used when declaring)")
parser.add_argument('--durable', default=False, action='store_true', help="""
    Sets durability needed for the exchange""")


args = parser.parse_args()
if args.message is None or args.exchange is None:
    parser.print_help()
    exit(1)
if args.durable and not args.declare:
    parser.print_help()
    exit(1)

connection = pika.BlockingConnection(pika.ConnectionParameters(args.host))
channel = connection.channel()

if args.declare:
    channel.exchange_declare(exchange=args.exchange, exchange_type=args.type, durable=args.durable)
else:
    channel.exchange_declare(exchange=args.exchange, passive=True)

for i in range(1, args.count + 1):

    if args.count == 1:
        body = args.message
    else:
        body = "{}{}".format(args.message, i)

    channel.basic_publish(
        exchange=args.exchange,
        routing_key=args.routing_key,
        body=body,
        properties=pika.BasicProperties(delivery_mode = 2)) # persistent

    if args.summary:
        print("{} {}".format(i, body), end='\r', flush=True)
    else:
        print("{} {}".format(i, body))

    if args.delay_ms > 0:
        time.sleep(args.delay_ms/1000.0)

connection.close()
