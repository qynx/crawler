from influxdb import InfluxDBClient
conn = InfluxDBClient("localhost", "8086", "", "", "crawler")

print(conn.query("show measurements"))

for i in range(0, 1000):
    data = [
        {
            "measurement": "crawler",
            "tags": {
                "name": "nbiquge"
            },
            "fields": {
                "lad": 4
            }
        }
    ]
    conn.write_points(data)