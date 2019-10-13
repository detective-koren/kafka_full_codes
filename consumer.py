from kafka import KafkaConsumer, TopicPartition
import io
import time
from PIL import Image
import datetime
import os
import cv2
import numpy as np

# settings
client = "203.237.53.4:9092"
topic = 'test'
path = "/home/konan2/Desktop/kafka-consumer/"

consumer = KafkaConsumer(bootstrap_servers=client)

total_time = time.time()


topic_mod = topic
partitions = TopicPartition(topic_mod,0)
consumer.assign([partitions])
consumer.seek_to_beginning()
lastoffset = consumer.end_offsets([partitions])[partitions]

path_mod = path
if not os.path.exists(path_mod):
    os.makedirs(path_mod)

print("topic name: " + topic_mod)
print(lastoffset)

for msg in consumer:
    start_time = time.time()
    array = np.frombuffer(msg.value, dtype=np.dtype('uint8'))
    img = cv2.imdecode(array,1)
    #cv2.imshow('recv',img)
    #cv2.imwrite(mk_path+str(key)+'.jpg', img)
    cv2.imwrite(path_mod+"frame"+str(msg.offset)+".jpg", img)
    lat = time.time() - start_time
    print("topic: " + topic_mod + ", frame"+str(msg.offset))
    print("latency: {} seconds".format(lat))
    print("bandwidth: {} bytes/sec".format(len(msg.value)/lat))
    if msg.offset == lastoffset -1:
        break


total_lat = time.time() - total_time
print("total time: {} minutes".format(total_lat/60))
