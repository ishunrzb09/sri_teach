from aws_publisher import BasicMessageSender

obj = BasicMessageSender()
obj.declare_queue()
obj.send_message("Hello from swathi")