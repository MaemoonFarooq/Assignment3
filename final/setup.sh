#!/bin/bash
echo "****Staring the setup****"

echo "****Formating the HDFS NameNode****"
# Format the HDFS NameNode
/usr/local/hadoop-2.10.2/bin/hdfs namenode -format
echo"****NameNode Formatted****"

echo "****Start all Hadoop daemons****"
# Start all Hadoop daemons
/usr/local/hadoop-2.10.2/sbin/start-all.sh
echo "****Hadoop daemons started****"

echo "****Starting Zookeeper****"
# Open a new terminal and run the command to start Zookeeper
gnome-terminal -- /bin/bash -c 'cd /home/maemoon/kafka && bin/zookeeper-server-start.sh config/zookeeper.properties; echo "Press Enter to close this terminal..."; read'

#sleeping so zookeper can run completely before the server starts
sleep 10 

echo "****Starting Server****"
# Open another new terminal and run the command to start Kafka server
gnome-terminal -- /bin/bash -c 'cd /home/maemoon/kafka && bin/kafka-server-start.sh config/server.properties; echo "Press Enter to close this terminal..."; read'

echo "****Checking Nodes****"
jps
