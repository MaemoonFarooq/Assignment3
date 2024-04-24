from kafka import KafkaConsumer
import json
from collections import Counter
import time
from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi


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
collection = db['Custom']

# Kafka consumer settings
bootstrap_servers = ['localhost:9092']
topic = 'Custom'

# Parameters for sliding window and decaying factor
window_size = 1000  # Number of recent events to consider in the sliding window
decay_factor = 0.9  # Decaying factor for weighting older events

# Initialize counters and variables for incremental processing
also_buy_counter = Counter()
window_events = []

# Create Kafka consumer
consumer = KafkaConsumer(topic,
                         bootstrap_servers=bootstrap_servers,
                         value_deserializer=lambda x: json.loads(x.decode('utf-8')))

# Main loop to process incoming data
for message in consumer:
    data = message.value
    
    # Extract relevant fields
    asin = data.get('asin')
    title = data.get('title')
    also_buy = data.get('also_buy', [])  # Use get() method to provide a default empty list if 'also_buy' is not present
    timestamp = time.time()  # Get current timestamp

    # Sliding window approach: Maintain a sliding window of recent events
    window_events.append((also_buy, timestamp))
    if len(window_events) > window_size:
        window_events.pop(0)  # Remove oldest event if window size exceeds limit

    # Online algorithm with decaying factor: Adjust counts based on recency
    for event, event_timestamp in window_events:
        for product in event:
            also_buy_counter[product] *= decay_factor ** (time.time() - event_timestamp)

    # Update counter with 'also_buy' products
    also_buy_counter.update(also_buy)

    # Generate product recommendations based on most frequently bought products
    recommendations = {
        'asin': asin,
        'title': title,
        'buy_recommendations': also_buy_counter.most_common(5)
    }

    # Extract ASINs and names of the top 5 recommended products
    top5_products = [(product[0], product_name) for product, product_name in zip(also_buy_counter.most_common(5), data['title'])]
    
    collection.insert_one(recommendations)

    # Print real-time insights
    print(f"Product ASIN: {asin}")
    print(f"Title: {title}")
    print(f"Top 5 Recommended Products:")
    for product_asin, product_name in top5_products:
        print(f"  ASIN: {product_asin}")
    print("-----------------------------------------")

    # Add a short delay to simulate real-time processing
    time.sleep(0.5)
