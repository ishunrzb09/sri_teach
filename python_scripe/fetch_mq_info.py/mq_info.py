import boto3
import json
import pprint

client = boto3.client('mq')

response = client.list_brokers(
    MaxResults = 5
)

#response = json.dumps(response , indent=4)

pprint.pprint(response['BrokerSummaries'][0]['BrokerArn'])

data_str = str(response['BrokerSummaries'][0]['BrokerArn']).split(':')

print(data_str[3],data_str[-1])