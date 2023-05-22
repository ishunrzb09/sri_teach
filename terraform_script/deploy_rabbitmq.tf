#fetching SG information from data block
data "aws_security_group" "rabbitMQ_data" {
  name = "rabbitMQ_SG"
}

#creating Rabbit mq engin
resource "aws_mq_broker" "rabbitmq_dv1" {
  broker_name = "Test"

  engine_type        = "RabbitMQ"
  engine_version     = "3.10.20"
  storage_type       = "ebs"
  host_instance_type = "mq.t3.micro"
  security_groups     = [data.aws_security_group.rabbitMQ_data.id]

  user {
    username = "gaurav"
    password = "gaurv@12345678"
  }

}
