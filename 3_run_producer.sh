#chage some info in image_dir and host

TOTAL_TOPICS=$(seq 0 100)
TOPIC_INTERVAL=10
TOPIC_NUM=0

TIME_INTERVAL='1s'

IMAGES_DIR='/home/konan1/konan/producer/face'

HOST='203.237.53.3:9092'



for i in $TOTAL_TOPICS
do
  #MAKE topics
  /usr/local/kafka/bin/kafka-topics.sh --create --zookeeper localhost:2181 --replication-factor 1 --partitions 1 --topic frame$i

  #PUBLISH to topic py producer
  python producer.py --host $HOST --topic frame$i --images_dir_path $IMAGES_DIR

  #DELETE topics
  /usr/local/kafka/bin/kafka-topics.sh --zookeeper localhost:2181 --delete --topic frame$((TOPIC_NUM-TOPIC_INTERVAL))

  sleep $TIME_INTERVAL

done
