from kafka import KafkaConsumer, TopicPartition
from json import loads, dumps
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from decouple import config
import settings


TOPIC = "topic1"
#PARTITION_0 = 0


consumer = KafkaConsumer(
     TOPIC,
     bootstrap_servers=['localhost:9092'],
     auto_offset_reset='earliest',
     enable_auto_commit=True,
     group_id='test',
     value_deserializer=lambda x: loads(str(x.decode("utf-8")).replace("'", "\"")))


bucket = config("bucket")
org = config("org")
token = config("token")
url=config("url")

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

# Write script
write_api = client.write_api(write_options=SYNCHRONOUS)

settings.init()

for message in consumer:
    print(message.value)
    print(message.topic)
    print(message.partition)
    print("=================")
    for key, value in settings.measures.items():
        if message.partition == value:
            p = influxdb_client.Point("my_measurement").field(key,message.value)
            write_api.write(bucket=bucket, org=org, record=p)
