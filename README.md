
# RabbitMQ send & receive demo in Python


Simple Python utilities to send and receive messages to/from RabbitMQ using the `pika` Python library (written in Python 3).

Useful for basic load testing and verification of RabbitMQ behaviour.


Requirements
============

A Docker image `beniji/rabbit-python-util` is available so you can run directly in Docker:

```
docker run --rm --net host beniji/rabbit-python-util rabbit-send.py  --exchange testexchange --message "hello"
```

To install manually (requires Python 3 with pip) just do `pip3 install -r requirements.txt`.



Sending messages
================

In RabbitMQ parlance, messages are sent to an "exchange". Normally you set an exchange up in the server before sending messages
to it, but for convenience rabbit-send.py can also declare the exchange for you.

To send a message to an existing RabbitMQ exchange "testexchange"

```
./rabbit-send.py --exchange testexchange --message "hello"
```

To send a message to a new RabbitMQ exchange which will be declared automatically use the `--declare` option

```
./rabbit-send.py --exchange testexchange --declare --message "hello"
```

Same as above but declaring a different exchange type ("direct" is the default value, and here we choose "topic" instead)

```
./rabbit-send.py --exchange testexchange --declare --type topic --message "hello"
```

To see all options run

```
./rabbit-send.py --help
```


Receiving messages (just prints out each message)
=================================================

Listen for messages on an existing Rabbit queue "testqueue"

```
./rabbit-receive.py --queue testqueue
```

Listen for messages on an existing exchange "testexchange" (creates an anonymous queue and binds it to the exchange):

```
./rabbit-receive.py --exchange testexchange
```

Create and bind a queue called "testqueue" to an existing exchange "testexchange" and listen for messages on that queue:

```
./rabbit-receive.py --exchange testexchange --queue testqueue
```


Sending messages for performance testing
========================================

Use the `--count X` and `--delay_ms Y` arguments to send/consume X messages with a delay of Y milliseconds in between each message.

Note that when `--count` is used, rabbit-send will append the index of the current message to the message body itself.


Running and administering RabbitMQ server
=========================================

Some tips on easily running and configuring a Rabbit server locally for testing (using Docker).

Manual way
----------

1. Run a rabbit server called `rabbit` and expose the ports you need

```
docker run --name rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

Test it's working by listing exchanges and queues (you'll have none initially):

```
docker exec rabbit rabbitmqctl list_exchanges
docker exec rabbit rabbitmqctl list_queues
```

2. Download the `rabbitmqadmin` python utility which you need to administer the server (you can grab this from your running container). Copy rabbitmqadmin into your local bin directory (your host machine will require python)

```
mkdir -p ~/bin
curl -o ~/bin/rabbitmqadmin localhost:15672/cli/rabbitmqadmin && chmod +x ~/bin/rabbitmqadmin
```

3. Create an exchange (in this case a topic)

```
~/bin/rabbitmqadmin declare exchange --vhost=/ name=testexchange type=topic
```

Using git configuration
-----------------------

An alternative way to run a RabbitMQ docker container is to place the Rabbit MQ server definitions JSON in source control and then bind mount that into the container. This way you can ensure the server creates your exchanges etc. at boot up time.

