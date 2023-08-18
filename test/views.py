from rest_framework.views import APIView
import pika
from rest_framework.response import Response

class TestListView(APIView):
    # 1 case
    # def get(self, request, format=None):
    #     try:
    #         # RabbitMQ connection parameters
    #         rabbitmq_host = '172.17.0.1'  # Replace with your RabbitMQ server's hostname or IP address
    #         rabbitmq_port = 5672  # Default port
    #         rabbitmq_virtual_host = '/'  # Default virtual host
    #         rabbitmq_credentials = pika.PlainCredentials('guest', 'guest')  # Replace with your credentials if required

    #         # Establish connection with RabbitMQ
    #         connection_params = pika.ConnectionParameters(
    #             host=rabbitmq_host,
    #             port=rabbitmq_port,
    #             virtual_host=rabbitmq_virtual_host,
    #             credentials=rabbitmq_credentials
    #         )
    #         connection = pika.BlockingConnection(connection_params)
    #         channel = connection.channel()

    #         # Declare queue 'messages' if it doesn't exist
    #         channel.queue_declare(queue='messages')
            
    #         # Add a binding to the queue (example binding to an exchange named 'logs')
    #         exchange_name = 'logs'
    #         channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')
    #         channel.queue_bind(exchange=exchange_name, queue='messages')

    #         # Send a message
    #         message = 'Hello, this is a test message!'
    #         channel.basic_publish(exchange='', routing_key='messages', body=message)

    #         # Close the connection
    #         connection.close()

    #         return Response('Message sent successfully.')

    #     except pika.exceptions.AMQPConnectionError as e:
    #         return Response(f'Error connecting to RabbitMQ: {e}')

    #     except Exception as e:
    #         return Response(f'An error occurred: {e}')
        

    #2 case
    def get(self, request, format=None):
        try:
            # RabbitMQ connection parameters
            connection_string = "amqp://guest:guest@172.17.0.1:5672/"  # Replace with your connection string

            # Parse the connection string
            parameters = pika.URLParameters(connection_string)

            # Establish connection with RabbitMQ
            connection = pika.BlockingConnection(parameters)
            channel = connection.channel()

            # Declare queue 'messages' if it doesn't exist
            channel.queue_declare(queue='messages')
            
            # Add a binding to the queue (example binding to an exchange named 'logs')
            exchange_name = 'logs'
            channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')
            channel.queue_bind(exchange=exchange_name, queue='messages')

            # Send a message
            message = 'Hello, this is a test message!'
            channel.basic_publish(exchange='', routing_key='messages', body=message)

            # Close the connection
            connection.close()

            return Response('Message sent successfully.')

        except pika.exceptions.AMQPConnectionError as e:
            return Response(f'Error connecting to RabbitMQ: {e}')

        except Exception as e:
            return Response(f'An error occurred: {e}')
