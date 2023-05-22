import pika

def msg_revcd(ch, method, properties, body):
    print(f"Msg recvd --> {body}")

conn_param = pika.ConnectionParameters("amqps://b-f4a79703-0e46-4678-b47b-b6612cdd92f5.mq.ap-south-1.amazonaws.com:5671")

conn = pika.BlockingConnection(conn_param)

channel = conn.channel()

channel.queue_declare("test_gaurav")

channel.basic_consume(queue='test_gaurav', auto_ack=True,on_message_callback=msg_revcd)

print("start conduming")