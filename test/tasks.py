from celery import shared_task
from core.celery import app
import json
from time import sleep
import time
import pika
@shared_task(bind=True,default_retry_delay=5*60)
def add(self,x, y):
    try:
        print('Hello it is  a celery')
        print(x)
        print(y)
        return x + y
    except Exception as e:
        raise self.retry(exc=e, countdown=60)
    
@shared_task
def mul(id):
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
    time.sleep(30)
    print('Start check message to receive LBS')
    while True:
        method_frame, header_frame, body = channel.basic_get(queue="messages", auto_ack=False)
    
        # Если есть сообщение, обработаем его
        if method_frame:
            data = json.loads(body)
            task_id_in_queue = data['task_id']
            if task_id_in_queue == id:
                print('NO!!!!!!!!!!!!!')
            # Вывести значение task_id
            print(f"Received message for task_id: {task_id_in_queue}")
            print(f"Received message: {body}")

        else:
            # Если нет доступных сообщений, выйти из цикла
            break

    connection.close()
    return id