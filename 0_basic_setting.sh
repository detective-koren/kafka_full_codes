#based on codes
#https://tecadmin.net/install-apache-kafka-ubuntu/

sudo apt update
sudo apt install default-jdk

wget http://www-us.apache.org/dist/kafka/2.2.1/kafka_2.12-2.2.1.tgz
tar xzf kafka_2.12-2.2.1.tgz
sudo mv kafka_2.12-2.2.1 /usr/local/kafka
