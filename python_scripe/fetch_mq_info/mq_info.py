import boto3
import json
import pprint
import sys
import base64
from pprint import pprint

n = len(sys.argv)

# total arguments
n = len(sys.argv)
print("Total arguments passed:", n)
 
# Arguments passed
print("\nName of Python script:", sys.argv[0])
 
print("\nArguments passed:", end = " ")
for i in range(1, n):
    print(sys.argv[i], end = " ")
     
###########################################

client = boto3.client('mq')

response = client.list_brokers(
    MaxResults = 5
)

if response['BrokerSummaries']:
    data_str = str(response['BrokerSummaries'][0]['BrokerArn']).split(':')
    final_url_str = f"amqps://{data_str[-1]}.{data_str[2]}.{data_str[3]}.amazonaws.com:5671"
    json_file_temp = {
  "Inputs": {
    "Request": {
      "Provider": "Sqs",
      "Sqs": {
        "QueueUrl": "https://sqs.us-west-2.amazonaws.com/149911641352/tps-dv1-usw2-assessment-fiposprocessor-request-queue"
      }
    }
  },

  "Sqs": {
    # Wait time in seconds for SQS long polling. Must be smaller than HTTP timeout.
    "WaitTimeSeconds": 3
  },

  "Tps": {
    # Port used for HTTP requests (status, health-check, etc.)
    "HttpPort": 80
  },

  "Processors": {
    "FiPosProcessor": {
      # Timeout in seconds for processor execution. If the parameter is not set, the processor is not controlled.
      "SecondsTimeout": 600.0,

      # Timeout in seconds for processor to start.
      "SecondsToStart": 20.0
    }
  },


  "AWS": {
    "Profile": "default"
  },
  
  "RabbitMQ": {
    # Hostname of the RabbitMQ broker, do not include the protocol or the port.
    "HostName": "",
    # Port used by the RabbitMQ broker
    "Port": 5671,    # TODO: [JLF] Can we keep the following under source control? They did for Kafka SaslSsl in Listener.CommandLine's corresponding Kafka config.
    "Username": "tpservice",
    "Password": "tpservicetpservice",
    "RemoteProcessorRequestQueueName": "fiposprocessor_request_mq"
  },

  "Logging": {
    "LogLevel": {
      "Default": "Debug"
    }
  },

  "Serilog": {
    "MinimumLevel": "Verbose",
    "WriteTo": [
      {
        "Name": "Console",
        "Args": {
          "formatter": "Serilog.Formatting.Compact.RenderedCompactJsonFormatter, Serilog.Formatting.Compact"
        }
      }
    ]
  },

  "HostOptions": {
    # https:#docs.microsoft.com/en-us/aspnet/core/fundamentals/host/generic-host?view=aspnetcore-3.1#shutdowntimeout-1
    "ShutdownTimeout": "00:04:00"
  }
}
    json_file_temp['RabbitMQ']['HostName'] = final_url_str
    with open("appsettingsprodjson.json","w") as json_file:
        json_file.write(f"{json.dumps(json_file_temp,indent=4)}")

    # aws_secret_client = boto3.client("secretsmanager")

    # response = aws_secret_client.create_secret(
    #     Name = "RabbitMQ_secret2",
    #     SecretString = '{"Name":"ishu","URL":"test"}'
    # )
    # print(response)

    ##############################################################################################################################
    final_url_str_keda = f"amqps://{json_file_temp['RabbitMQ']['Username']}:{json_file_temp['RabbitMQ']['Password']}@{data_str[-1]}.{data_str[2]}.{data_str[3]}.amazonaws.com:5671"
    message = final_url_str_keda
    message_bytes = message.encode('ascii')
    base64_bytes = base64.b64encode(message_bytes)
    base64_message = base64_bytes.decode('ascii')

    keda_yaml_file = """
apiVersion: v1
kind: Secret
metadata:
  name: keda-rabbitmq-secret
data:
  host: "{0}"
---
apiVersion: keda.sh/v1alpha1
kind: TriggerAuthentication
metadata:
  name: keda-trigger-auth-rabbitmq-conn
spec:
  secretTargetRef:
    - parameter: host
      name: keda-rabbitmq-secret
      key: host
---
apiVersion: keda.sh/v1alpha1
kind: ScaledObject
metadata:
  name: {{ .Chart.Name }}-keda
spec:
  scaleTargetRef:
    kind: Deployment
    name: {{ template "fiposprocessorservice.deployName" . }}
  minReplicaCount: {{ .Values.replicaCount.min }}
  maxReplicaCount: {{ .Values.replicaCount.max }}
  triggers:
  - type: rabbitmq
    metadata:
      protocol: "amqp"
      queueName: "fiposprocessor_request_mq"
      queueLength: "1"
    authenticationRef:
      name: keda-trigger-auth-rabbitmq-conn

    """.format(base64_message)
    with open("keda_yaml.yml","w") as keda_file:
        keda_file.write(keda_yaml_file)
else:
    print("No mq broker deployed")