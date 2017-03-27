
# RabbitMQ send & receive demo in Python


Simple Python utilities to show how to send and receive messages to/from RabbitMQ using the `pika` Python library (code is written for Python 3).


Requirements
============

A Docker image `beniji/rabbit-python-util` is available so you can run directly in Docker:

```
docker run --rm --net host beniji/rabbit-python-util rabbit-send.py  --exchange testexchange --message "hello"
```

Or to install manually (requires Python 3) just do `pip3 install -r requirements.txt`.



Sending messages
================

To send a message "hello" to RabbitMQ (the exchange "testexchange" must have been already setup in the server - see below for how to create exchanges):

```
./rabbit-send.py --exchange testexchange --message "hello"
```

To send a message to RabbitMQ and also declare a queue (durable in this case) and bind it to an exchange in the one step:

```
./rabbit-send.py --exchange testexchange --queue testqueue --durable --message "hello"
```

Same as above but declaring a non-durable queue (just omit the `--durable` argument):

```
./rabbit-send.py --exchange testexchange --queue testqueue --message "hello"
```

To see all options run

```
./rabbit-send.py --help
```


Receiving messages (just prints out each message)
=================================================

Listen for messages from a Rabbit queue

```
./rabbit-receive.py --queue testqueue
```


Sending messages for performance testing
========================================

Use the `--count X` and `--delay_ms Y` arguments to send X messages with a delay of Y milliseconds in between each send call. Note that this will append the index of the current message to the message body itself.


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
curl -o ~/bin/rabbitmqadmin localhost:15672/cli/rabbitmqadmin && chmod +x ~/bin/rabbitmqadmin
```

3. Create an exchange (in this case a topic)

```
rabbitmqadmin declare exchange --vhost=/ name=testexchange type=topic
```

Using git configuration
-----------------------

An alternative way to run a RabbitMQ docker container is to place the Rabbit MQ server definitions JSON in source control and then bind mount that into the container. This way you can ensure the server creates your exchanges etc. at boot up time.


