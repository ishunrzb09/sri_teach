from basicClient import BasicPikaClient

class BasicMessageSender(BasicPikaClient):

    def declare_queue(self):
        self.channel.queue_declare(queue="swathi_que")

    def send_message(self,body):
        channel = self.connection.channel()
        channel.basic_publish(exchange='',
                              routing_key='gaurav_test',
                              body=body)
        print(f"Sent message.  Body: {body}")

    def close(self):
        self.channel.close()
        self.connection.close()

if __name__ == "__main__":

    # Initialize Basic Message Sender which creates a connection
    # and channel for sending messages.
    basic_message_sender = BasicMessageSender()
