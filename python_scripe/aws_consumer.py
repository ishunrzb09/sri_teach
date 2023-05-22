from basicClient import BasicPikaClient

def msg_revcd(ch, method, properties, body):
        print(f"Msg recvd --> {body}")

class BasicMessageReceiver(BasicPikaClient):
    

    def get_message(self):
        self.channel.queue_declare("test_gaurav")
        self.channel.basic_consume(queue='test_gaurav', auto_ack=True,on_message_callback=msg_revcd)
        print("start consuming")

    # def close(self):
    #     self.channel.close()
    #     self.connection.close()


if __name__ == "__main__":

    # Create Basic Message Receiver which creates a connection
    # and channel for consuming messages.
    basic_message_receiver = BasicMessageReceiver()

    # Consume the message that was sent.
    basic_message_receiver.get_message("hello world queue")

    # Close connections.
    basic_message_receiver.close()