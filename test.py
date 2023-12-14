import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
from decouple import config

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

p = influxdb_client.Point("my_measurement").tag("location", "Prague").field("temperature", 25.3)
print(write_api.write(bucket=bucket, org=org, record=p))

query_api = client.query_api()
query = 'from(bucket:"test")\
|> range(start: -10m)\
|> filter(fn:(r) => r._measurement == "my_measurement")\
|> filter(fn:(r) => r.location == "Prague")\
|> filter(fn:(r) => r._field == "temperature")'
result = query_api.query(org=org, query=query)
results = []
for table in result:
    for record in table.records:
        results.append((record.get_field(), record.get_value()))

print(results)
