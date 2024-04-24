from pymongo import MongoClient
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

# Now, if you want to connect to a local MongoDB instance, do not create another client. 
# Use the existing client and connect to the local MongoDB instance like this:

# Connect to MongoDB
# client = MongoClient('mongodb://localhost:27017/')  # Commenting out this line as it's not necessary

# Select database
db = client['Frequent_Dataset_Mining']

# Select collection
collection = db['PCY']

# Define the record to insert
record = {
    "firstname": "Maemoon"
}

# Insert a single record into the collection
collection.insert_one(record)

# Confirming successful insertion
print("Record inserted successfully!")
