import json 
from kafka import KafkaConsumer
from itertools import combinations
from collections import defaultdict
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from time import sleep

class PCYAlgorithm:
    def __init__(self, support_threshold, hash_buckets):
        self.support_threshold = support_threshold
        self.hash_buckets = hash_buckets
        self.freq_items = defaultdict(int)
        self.hash_table = [0] * hash_buckets
        self.num_buckets = hash_buckets
        self.total_num_items = 0

    def hash_function(self, itemset):
        return sum(hash(item.encode()) % self.num_buckets for item in itemset) % self.num_buckets

    def update_hash_table(self, itemset):
        for pair in combinations(itemset, 2):
            hash_value = self.hash_function(pair)
            self.hash_table[hash_value] += 1

    def update_freq_items(self, itemset):
        for item in itemset:
            self.freq_items[item] += 1

    def process_transaction(self, transaction):
        asin = transaction['asin']
        also_buy = transaction.get('also_buy', [])
        transaction_set = set([asin] + also_buy)
        self.update_freq_items(transaction_set)
        self.update_hash_table(transaction_set)
        self.total_num_items += 1

    def get_frequent_items(self):
        frequent_items = [item for item, count in self.freq_items.items() if count >= self.support_threshold]
        return frequent_items

    def get_candidate_pairs(self):
        candidate_pairs = []
        for pair in combinations(self.get_frequent_items(), 2):
            hash_value = self.hash_function(pair)
            if self.hash_table[hash_value] >= self.support_threshold:
                candidate_pairs.append(pair)
        return candidate_pairs

def consume_transactions(topic_pcy, bootstrap_servers, support_threshold, hash_buckets):
    consumer_pcy = KafkaConsumer(topic_pcy, bootstrap_servers=bootstrap_servers, group_id="pcy-group", value_deserializer=lambda m: json.loads(m.decode("utf-8")))
    pcy = PCYAlgorithm(support_threshold, hash_buckets)
    
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
    
    # Select database
    db = client['Frequent_Dataset_Mining']

    # Select collection
    collection = db['PCY']

    for message in consumer_pcy:
        transaction = message.value
        pcy.process_transaction(transaction)
        
        frequent_items_pcy = pcy.get_frequent_items()
        candidate_pairs = pcy.get_candidate_pairs()
        
        try:
            # Insert data into MongoDB
            data = {"Data": frequent_items_pcy}
            collection.insert_one(data)
        except Exception as e:
            print("Error inserting data into MongoDB:", e)
        
        print("***PCY***")
        print(frequent_items_pcy)
        sleep(15)
        
if __name__ == "__main__":
    bootstrap_servers = ['localhost:9092']
    topic_pcy = 'PCY'

    consume_transactions(topic_pcy, bootstrap_servers, support_threshold=1, hash_buckets=10)
