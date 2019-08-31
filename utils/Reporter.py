from influxdb import InfluxDBClient

class BaseReporter():

    def __init__(self):
        pass

    def report_lag(self, *args, **kw):
        pass

    def ping(self):
        pass

class InfluxReporter(BaseReporter):

    def __init__(self):
        self.conn = InfluxDBClient("localhost", "8086", "", "", "crawler", timeout=3)
    
    def report_lag(self, tag, value):
        data = [{
            "measurement": "crawler",
            "tags": {
                "name": tag
            },
            "fields": {
                "lag": value
            }
        }]
        self.conn.write_points(data)

    def ping(self):
        self.conn.get_list_database()