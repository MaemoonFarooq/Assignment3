import json 
from kafka import KafkaConsumer
from collections import defaultdict
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from time import sleep


class AprioriAlgorithm:
    def __init__(self, support_threshold):
        self.support_threshold = support_threshold
        self.freq_items = defaultdict(int)

    def update_freq_items(self, itemset):
        for item in itemset:
            self.freq_items[item] += 1

    def process_transaction(self, transaction):
        asin = transaction['asin']
        also_buy = transaction.get('also_buy', [])
        transaction_set = set([asin] + also_buy)
        self.update_freq_items(transaction_set)

    def get_frequent_items(self):
        frequent_items = [item for item, count in self.freq_items.items() if count >= self.support_threshold]
        return frequent_items

def consume_transactions(topic_apriori, bootstrap_servers, support_threshold):
    consumer_apriori = KafkaConsumer(topic_apriori, bootstrap_servers=bootstrap_servers, group_id="apriori-group", value_deserializer=lambda m: json.loads(m.decode("utf-8")))
    apriori = AprioriAlgorithm(support_threshold)
    
    # MongoDB Atlas connection URI
    uri = "mongodb+srv://user:1234@cluster0.sserygh.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0"

    # Create a new client and connect to the server using the specified Server API version
    client = MongoClient(uri, server_api=ServerApi('1'))

    # Send a ping to confirm a successful connection
    try:
        client.admin.command('ping')
        print("Pinged your deployment. You successfully connected to MongoDB Atlas!")
    except Exception as e:
        print(e)

    #selecting database
    db = client['Frequent_Dataset_Mining']

    # Select collection
    collection = db['Apriori']
    
    for message in consumer_apriori:
        transaction = message.value
        apriori.process_transaction(transaction)
        frequent_items_apriori = apriori.get_frequent_items()

        try:
        # Insert data
            data={"Data":frequent_items_apriori}
            result = collection.insert_one(data)
        except Exception as e:
            print("Error inserting data into MongoDB:", e)

        print("***Apriori***")
        print(frequent_items_apriori)
        sleep(15)
        



if __name__ == "__main__":
    bootstrap_servers = ['localhost:9092']
    topic_apriori = 'Apriori'

    consume_transactions(topic_apriori, bootstrap_servers, support_threshold=1)
