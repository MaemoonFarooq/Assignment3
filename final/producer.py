import json
from kafka import KafkaProducer
from time import sleep

bootstrap_servers = ['localhost:9092']

topics = ['PCY','Apriori','Custom']  # Use a list even if you have only one topic

producer = KafkaProducer(bootstrap_servers=bootstrap_servers, value_serializer=lambda x: json.dumps(x).encode('utf-8'))

# Real-time batch pre-processing
with open('Sampled_Amazon_Meta.json', 'r') as f_read:
    for line in f_read:
        try:
            obj = json.loads(line)
            # Removing other data except
            filtered_obj = {
                'title': obj.get('title'),
                'asin': obj.get('asin'),
                'also_buy': obj.get('also_buy', []),
            }
            # Sending the data to the consumer
            for topic in topics:
                producer.send(topic, filtered_obj)
                print(topic, filtered_obj)
            # time out created so that each algorithm can run completely before sending in new data
            # can be increased based on trial and error
            sleep(15)    

        except json.JSONDecodeError as e:
            print("JSON Decode Error:", e)
            continue  
