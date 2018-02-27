
# RabbitMQ send & receive demo in Python


Simple Python utilities to send and receive messages to/from RabbitMQ using the `pika` Python library (written in Python 3). Docker image available (`docker pull exaspace/rabbit-python-util`).

Try it!

    docker run --rm --net host exaspace/rabbit-python-util rabbit-send.py --help


Sending messages
================

In RabbitMQ parlance, messages are sent to an "exchange". Normally you set an exchange up in the server before sending messages to it, but for convenience rabbit-send.py can also declare the exchange for you.

Send a message to an existing RabbitMQ exchange "testexchange"

```
$ rabbit-send.py --exchange testexchange --message "hello"
```

Send the contents of the file "message.txt" (prefix with "@" for filename)

```
$ rabbit-send.py --exchange testexchange --message @message.txt
```

Send a message to a new RabbitMQ exchange which will be declared automatically use the `--declare` option

```
$ rabbit-send.py --exchange testexchange --declare --message "hello"
```

Use a different exchange type ("direct" is the default value but here we choose "topic" instead)

```
$ rabbit-send.py --exchange testexchange --declare --type topic --message "hello"
```

Send 1000 messages ("hello 1", "hello 2", ...) at the rate of 10 per second

```
$ rabbit-send.py --exchange testexchange --message "hello @COUNT@" --count 1000 --delay_ms 100
```

Use `--routing_key` to specify a routing key.

To see all options run

```
$ rabbit-send.py --help
```


Receiving messages (just prints out each message)
=================================================

Listen for messages on an existing Rabbit queue "testqueue" (use this for round-robin type messaging)

```
./rabbit-receive.py --queue testqueue
```

Listen for messages on an existing exchange "testexchange" (creates an anonymous queue and binds it to the exchange so
use this for pub-sub type messaging):

```
./rabbit-receive.py --exchange testexchange
```

Create and bind a new queue called "testqueue" to an existing exchange "testexchange" and listen for messages on that queue:

```
./rabbit-receive.py --exchange testexchange --queue testqueue
```

Consume 1000 messages at the rate of 10 per second

```
./rabbit-receive.py --exchange testexchange --count 1000 --delay_ms 100
```

Use `--routing_key` to specify a routing key.


Sending messages for performance testing
========================================

Use the `--count X` and `--delay_ms Y` arguments to send/consume X messages with a delay of Y milliseconds in between each message.

Note that if the magic string "@COUNT@" occurs in your message body, it will be replaced by the index of the current message.


Installation (Docker)
=====================

```
    alias rabbit-send.py='docker run --rm --net host exaspace/rabbit-python-util rabbit-send.py'
    alias rabbit-receive.py='docker run --rm --net host exaspace/rabbit-python-util rabbit-receive.py'
```

Then `rabbit-send.py  --help` should work.


Installation (Native)
=====================

To install natively (requires Python 3 with pip), clone this repo then from the top level:

    pip3 install -r requirements.txt
    ./rabbit-send.py --help



Running a local RabbitMQ server
===============================

You can easily run and configure a RabbitMQ server locally for testing using Docker.

```
docker run --name rabbit -p 5672:5672 -p 15672:15672 rabbitmq:3-management
```

Test it's working by listing exchanges and queues (you'll have none initially):

```
docker exec rabbit rabbitmqctl list_exchanges
docker exec rabbit rabbitmqctl list_queues
```

Fetch the `rabbitmqadmin` python utility from the running container which you can then use
 to administer the server (your host machine will require python of course).

```
mkdir -p ~/bin
curl -o ~/bin/rabbitmqadmin localhost:15672/cli/rabbitmqadmin && chmod +x ~/bin/rabbitmqadmin
```

Create an exchange (in this case with type "topic")

```
~/bin/rabbitmqadmin declare exchange --vhost=/ name=testexchange type=topic
```

An way to automate the configuration of a RabbitMQ docker container is to place the Rabbit MQ server
 definitions JSON on your local file system and then bind mount that into the container. This ensures
 the server creates your exchanges etc. at boot up time.

