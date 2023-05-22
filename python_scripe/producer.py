import pika

conn_param = pika.ConnectionParameters("amqps://b-f4a79703-0e46-4678-b47b-b6612cdd92f5.mq.ap-south-1.amazonaws.com:5671")

conn = pika.BlockingConnection(conn_param)

channel = conn.channel()

channel.queue_declare("test_gaurav")

msg = "Hello this is my first msh"

channel.basic_publish(exchange='',routing_key='test_gaurav',body=msg)

print(f"sent msg --> {msg}")