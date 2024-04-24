from kafka import KafkaConsumer
import json 
import subprocess

bootstrap_servers = ['localhost:9092']

#initalizing all topics
topic1 = 'PCY'
topic2 = 'Apriori'
topic3 = 'Custom'

#individual consumers for the topics
consumer1 = KafkaConsumer(topic1, bootstrap_servers=bootstrap_servers,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))


consumer2 = KafkaConsumer(topic2, bootstrap_servers=bootstrap_servers,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))


consumer3 = KafkaConsumer(topic3, bootstrap_servers=bootstrap_servers,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))


#PCY
for message in consumer1:
    data = message.value
    
#Aprioiri
for message in consumer2:
    data = message.value

#Custom
for message in consumer3:
    data = message.value