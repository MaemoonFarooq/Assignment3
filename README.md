**Assignment # 3 Frequent      Dataset Mining**

# **Introduction**

In this assignment, we embark on a journey of frequent dataset mining using Apache Kafka, focusing on the extensive Amazon dataset. Our goal is to employ two powerful algorithms, Apriori and PCY, renowned for their efficacy in mining frequent itemsets. By leveraging the distributed nature of Apache Kafka, we aim to efficiently process and analyze vast volumes of data, uncovering valuable insights and patterns within the Amazon dataset.
To download the  Amazon meta data you can access the link below which directly downloads a 12 GB compressed file which after extraction converts to 105 GB.

**Download Link**: https://datarepo.eng.ucsd.edu/mcauley_group/data/amazon_v2/metaFiles/All_Amazon_Meta.json.gz


# **Analysis**

Upon delving into the Amazon dataset, a distinct pattern emerges, revealing three key columns associated with each product: ASIN, also\_view, and also\_buy. The ASIN serves as a unique identifier for individual products, while the also\_view and also\_buy columns encapsulate related ASIN IDs. These relationships offer invaluable opportunities for understanding customer behavior, product associations, and potential recommendation strategies. By discerning these patterns, we lay the groundwork for subsequent preprocessing and algorithmic analysis.



# **Pre-Processing**

After examining the data closely, we took steps to prepare it for analysis. We focused on keeping only the most important information: the ASIN and also\_buy columns. These columns help us understand which products are related to each other.

Additionally, we made our data processing more efficient. In the producer section, we set up batch processing. This means that data is processed in groups, which allows us to send it directly to three different consumer files in real-time. This streamlined approach makes our data analysis faster and more effective, laying the groundwork for further analysis and insights.



# **Data Pipeline**

In the producer file, a straightforward data pipeline is established to transmit information to the consumer files, enabling the application of various dataset mining algorithms. The setup includes three predefined topics, aptly named PCY, Apriori, and Custom, serving as designated channels for data dissemination.

Each piece of product data is routed to all three topics, ensuring a comprehensive and thorough analysis process. To optimize the transmission efficiency, a thoughtful timeout mechanism of 10 seconds is implemented, balancing swift data delivery with system resource management which could be changed later on based on how much time the algorithms take to process the data and give insights.


# **Frequent Dataset Mining Algorithms**

In the consumer files two classic techniques are used for the dataset mining Apriori and PCY. Both running on their individual consumers and data provided by the producer.

Threading is used to ensure that algorithms run simultaneously one by one but sometimes one algorithm runs before the other as Apriori is known to run more efficiently on small datasets while PCY due to its hash mapping capabilities runs much better on big data as the data continues to grow by time.

But instead of doing all of this in a single file we created three different consumer files as that would make the code more readable and the make the GUI more user friendly as the the frequent items increase with time.

Also, we used the technique of incremental data as it is a more optimized approach.


**PCY Algorithm**

The code is an implementation of the PCY (Park-Chen-Yu) algorithm to find frequent item sets and candidate pairs from a stream of transactions coming from a Kafka topic. The goal is to identify patterns in the data and store them in a MongoDB database for further analysis.

The code defines the PCY Algorithm class to handle the PCY algorithm, including functions for hashing, updating frequency counts and hash tables, and retrieving frequent items and candidate pairs. It consumes messages from the Kafka topic and processes each transaction using the PCY algorithm. The frequent item sets are stored in a MongoDB database, and potential errors during insertion are handled gracefully.

This approach leverages Kafka for data streaming, the PCY algorithm for efficient frequent itemset mining, and MongoDB for data storage, resulting in a streamlined process for analyzing and storing patterns from large transaction datasets.

![PCY](https://github.com/MaemoonFarooq/Assignment3/assets/128331365/e622c2e0-0b25-4a85-83f7-09dd338f8093)



**Apriori Algorithm**

The code implements the Apriori algorithm to identify frequent item sets from a stream of transactions received through a Kafka topic. The main objective is to determine patterns in the data and store them in a MongoDB database for further analysis.

The Apriori Algorithm class is designed to handle the Apriori algorithm, including functions for updating frequency counts and retrieving frequent items based on a specified support threshold. The code consumes messages from the Kafka topic, processes each transaction using the Apriori algorithm, and stores the resulting frequent items in a MongoDB database. The MongoDB connection and data insertion are managed with error handling in place to ensure robustness.

This approach leverages Kafka for data streaming, the Apriori algorithm for identifying frequent item sets, and MongoDB for data storage, providing a structured and efficient process for analyzing large transaction datasets and extracting valuable insights.

![Apriori](https://github.com/MaemoonFarooq/Assignment3/assets/128331365/471043af-492b-4c44-aded-aa23c533cde4)





 **Custom Algorithm**


 The code uses a sliding window approach combined with timestamps and a decaying factor to efficiently analyze data streams and generate real-time insights. The sliding window maintains a record of the most recent events within a specified size (1,000 events in this case) to focus on current trends and customer behaviors. By pairing each event with a timestamp, the script can apply the decaying factor to weigh older events less heavily and give more importance to newer events. This method helps identify emerging patterns and avoid outdated data from influencing the results.

 In addition to the sliding window, the code utilizes a Kafka consumer to read incoming data from a Kafka topic, with automatic deserialization of JSON-formatted messages for easier handling. As each message arrives, the script extracts relevant information such as `asin`, `title`, and `also\_buy` products, and updates the `also\_buy\_counter` with the frequencies of products bought together. By adjusting the `also\_buy\_counter` with the decaying factor, the code ensures that the most relevant and recent data influences the recommendations.

 The `get\_frequent\_items` function identifies frequent items based on a specified support threshold, helping the script generate product recommendations for the current product. This provides valuable insights into customer preferences and potential product pairings, which can be beneficial for targeted marketing and inventory management. Once the recommendations are generated, the script inserts them into a MongoDB collection, making them easily accessible for further analysis.

 Overall, this approach allows the code to process data streams in real-time, prioritize recent events, and efficiently manage and analyze customer behavior patterns. This can provide significant benefits for businesses looking to understand their customers better and tailor their offerings accordingly.

![Custom](https://github.com/MaemoonFarooq/Assignment3/assets/128331365/15d919ef-1344-452c-865f-f7b76327af21)


**Output:**

![custom_output](https://github.com/MaemoonFarooq/Assignment3/assets/128331365/fae5f479-0bc5-463d-9519-68180ce70d9a)

================================================================

# **MongoDB**

MongoDB is used for data storage. Three collections have been made to store individual data produced for each algorithm.

# **Bash Script**
Bash script also created which upon executing would start all Hadoop and Kafka services.


**Group Members:**

Maemoon Farooq i211680

` `Taimoor Atta i211754

Younas Sohail i212680
