import json 
from kafka import KafkaConsumer
from itertools import combinations
from collections import defaultdict
import threading

class PCYAlgorithm:
    def __init__(self, support_threshold, hash_buckets):
        self.support_threshold = support_threshold
        self.hash_buckets = hash_buckets
        self.freq_items = defaultdict(int)
        self.hash_table = [0] * hash_buckets
        self.num_buckets = hash_buckets
        self.total_num_items = 0
        self.pcy_done = threading.Event()

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
        also_view = transaction.get('also_view', [])
        also_buy = transaction.get('also_buy', [])
        transaction_set = set([asin] + also_view + also_buy)
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

class AprioriAlgorithm:
    def __init__(self, support_threshold):
        self.support_threshold = support_threshold
        self.freq_items = defaultdict(int)
        self.apriori_done = threading.Event()

    def update_freq_items(self, itemset):
        for item in itemset:
            self.freq_items[item] += 1

    def process_transaction(self, transaction):
        asin = transaction['asin']
        also_view = transaction.get('also_view', [])
        also_buy = transaction.get('also_buy', [])
        transaction_set = set([asin] + also_view + also_buy)
        self.update_freq_items(transaction_set)

    def get_frequent_items(self):
        frequent_items = [item for item, count in self.freq_items.items() if count >= self.support_threshold]
        return frequent_items



def consume_transactions(topic_pcy, topic_apriori, bootstrap_servers, support_threshold, hash_buckets):
    # function for consuming transactions for Apriori
    def consume_apriori():
        consumer_apriori = KafkaConsumer(topic_apriori, bootstrap_servers=bootstrap_servers, group_id="apriori-group", value_deserializer=lambda m: json.loads(m.decode("utf-8")))
        apriori = AprioriAlgorithm(support_threshold)
        
        for message in consumer_apriori:
            transaction = message.value
            apriori.process_transaction(transaction)
            frequent_items_apriori = apriori.get_frequent_items()
            print("***Apriori***")
            # print(frequent_items_apriori)

    # function for consuming transactions for PCY
    def consume_pcy():
        consumer_pcy = KafkaConsumer(topic_pcy, bootstrap_servers=bootstrap_servers, group_id="pcy-group", value_deserializer=lambda m: json.loads(m.decode("utf-8")))
        pcy = PCYAlgorithm(support_threshold, hash_buckets)
        
        for message in consumer_pcy:
            transaction = message.value
            pcy.process_transaction(transaction)
            frequent_items_pcy = pcy.get_frequent_items()
            candidate_pairs = pcy.get_candidate_pairs()
            print("***PCY***")
            # print(frequent_items_pcy)
            # print(candidate_pairs)

      
    # threading for each loop
    thread_apriori = threading.Thread(target=consume_apriori)
    thread_pcy = threading.Thread(target=consume_pcy)

    # Starting the threads
    thread_apriori.start()
    thread_pcy.start()

    # Waiting for both threads to finish
    thread_apriori.join()
    thread_pcy.join()

if __name__ == "__main__":

    bootstrap_servers = ['localhost:9092']
    
    #topics
    topic_pcy = 'PCY'
    topic_apriori = 'Apriori'

    consume_transactions(topic_pcy, topic_apriori, bootstrap_servers, support_threshold=1, hash_buckets=10)