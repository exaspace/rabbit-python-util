
# RabbitMQ send & receive in Python


Simple Python utilities to send and receive messages to/from RabbitMQ using the `pika` Python library. 

Useful for basic performance testing and demonstrations of RabbitMQ and Pika usage.

Send 100 templated string messages:

    ./rabbit-send.py  --exchange testexchange --message "hello @COUNT@" --count 100

Receive messages:

    ./rabbit-receive.py --exchange testexchange 


## Demo

Install in a new virtualenv

    python3 -m venv venv
    source venv/bin/activate
    pip install -r requirements.txt


Start a local RabbitMQ server (admin site will be accessible at `http://localhost:15672/`)

    docker compose up -d

Sending 100 messages at a rate of one per second to a new durable exchange called 'testexchange':

    ./rabbit-send.py  --exchange testexchange --message "yo @COUNT@" --delay_ms 1000 --declare --durable --count 100

In another window, start consuming from 'testexchange':

    ./rabbit-receive.py --exchange testexchange  --queue testqueue --durable


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

Listen for messages on an existing exchange "testexchange" (creates an anonymous queue and binds it to the exchange so you can use this for pub-sub type messaging):

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



Tips on running and administering a local RabbitMQ server
=========================================================

Run `docker compose up -d` in this project's directory to start a rabbit server.

The RabbitMQ Admin UI is available at `http://localhost:15672/`.

To list exchanges and queues (you'll have none initially) you can run the `rabbitmqctl` tool inside the container:

```
docker compose exec rabbitmq rabbitmqctl list_exchanges
docker compose exec rabbitmq rabbitmqctl list_queues
```

You can also fetch the `rabbitmqadmin` python utility from the running container which you can then use
 to administer the server (your host machine will require python of course).

```
curl -o ./rabbitmqadmin localhost:15672/cli/rabbitmqadmin && chmod +x ./rabbitmqadmin
```

Use the admin utility to create an exchange (in this case with type "topic")

```
./rabbitmqadmin declare exchange --vhost=/ name=testexchange type=topic
```

A way to automate the configuration of a RabbitMQ docker container is to place the Rabbit MQ server
 definitions JSON on your local file system and then bind mount that into the container. This ensures
 the server creates your exchanges etc. at boot up time.

