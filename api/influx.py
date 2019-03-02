from influxdb import InfluxDBClient
import os

host = "localhost"
port = 8086
database = "waterflow"

host = 'localhost'

try:
    if os.environ["DEPLOY"]:
        host = os.environ["INFLUX_HOST"]
except Exception as e:
    print("Running on develop environment")

client = InfluxDBClient(host=host, port=port, database=database)
