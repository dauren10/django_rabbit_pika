from rest_framework.views import APIView
import pika
from .tasks import add, mul
from rest_framework.response import Response
import time
import json
class TestListView(APIView):
    # 1 case

    
    
       
   
    def get(self, request, format=None):
        try:
            # RabbitMQ connection parameters
            rabbitmq_host = '172.17.0.1'  # Replace with your RabbitMQ server's hostname or IP address
            rabbitmq_port = 5672  # Default port
            rabbitmq_virtual_host = '/'  # Default virtual host
            rabbitmq_credentials = pika.PlainCredentials('guest', 'guest')  # Replace with your credentials if required

            # Establish connection with RabbitMQ
            connection_params = pika.ConnectionParameters(
                host=rabbitmq_host,
                port=rabbitmq_port,
                virtual_host=rabbitmq_virtual_host,
                credentials=rabbitmq_credentials
            )
            connection = pika.BlockingConnection(connection_params)
            channel = connection.channel()

            # Declare queue 'messages' if it doesn't exist
            channel.queue_declare(queue='messages')
            
            # Add a binding to the queue (example binding to an exchange named 'logs')
            exchange_name = 'logs'
            channel.exchange_declare(exchange=exchange_name, exchange_type='fanout')
            channel.queue_bind(exchange=exchange_name, queue='messages')
           
            # Send a message
            message = {
                'task_id': 344,
                'services': [1],  # Convert set to a list
                'locations': [
                    {'lac': 1}
                ],
                'command': 'LD',
                'whitelists': [
                    {'lac': 1}
                ]
            }
            channel.basic_publish(exchange='', routing_key='messages', body=json.dumps(message))
            
            result = mul.delay(344)
            # method_frame, header_frame, body = channel.basic_get(queue='messages', auto_ack=False)
            
            # while True:
            #     time.sleep(1)
            #     if method_frame:
            #         print(f"Received message: {body}")
            #     else:
            #         print("No message available")

            connection.close()

            # Check if an acknowledgment was received
        
            return Response('Message sent, but no acknowledgment received within the timeout.')

        except pika.exceptions.AMQPConnectionError as e:
            return Response(f'Error connecting to RabbitMQ: {e}')

        except Exception as e:
            return Response(f'An error occurred: {e}')
        

class ConsListView(APIView):

    async def callback(self, channel, body, envelope, properties):
        print(f"Received message: {body}")
        await channel.basic_client_ack(delivery_tag=envelope.delivery_tag)

    async def get(self, request, format=None):
        rabbitmq_host = '172.17.0.1'  # Replace with your RabbitMQ server's hostname or IP address
        rabbitmq_port = 5672  # Default port
        rabbitmq_virtual_host = '/'  # Default virtual host
        rabbitmq_credentials = pika.PlainCredentials('guest', 'guest')  # Replace with your credentials if required

        # Establish connection with RabbitMQ
        connection_params = pika.ConnectionParameters(
            host=rabbitmq_host,
            port=rabbitmq_port,
            virtual_host=rabbitmq_virtual_host,
            credentials=rabbitmq_credentials
        )
        connection = pika.BlockingConnection(connection_params)
        channel = connection.channel()
        
        # Объявляем очередь 'messages', если она не существует
        await channel.queue_declare(queue='messages')

        # Устанавливаем функцию обратного вызова для обработки сообщений из очереди 'messages'
        await channel.basic_consume(queue='messages', on_message_callback=self.callback)

        print("Consumer started. Waiting for messages.")

      

        return Response('An error occurred:')



class SampleListView(APIView):
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