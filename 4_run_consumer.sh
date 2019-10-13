TIME_INTERVAL='1s'

TOTAL_TOPICS=$(seq 0 100)

PATH='/home/konan3/konan/consumer/face/'

CLIENT='203.237.53.5:9092'

for i in $TOTAL_TOPICS
do 

  python consumer.py --path $PATH --topic frame$i --client $CLIENT

  sleep $TIME_INTERVAL

done
