'''
Module to write data in the influx db.
'''
from influxdb_client import InfluxDBClient, WriteOptions
from influxdb_client.client.exceptions import InfluxDBError


def write(data, influx_bucket):
    '''
    Write metrics to influx.
    '''
    with InfluxDBClient.from_config_file("conf/influx.ini") as _client:
        with _client.write_api(write_options=WriteOptions(batch_size=5000,
                                                            flush_interval=10_000,
                                                            jitter_interval=2_000,
                                                            retry_interval=5_000,
                                                            max_retries=5,
                                                            max_retry_delay=30_000,
                                                            exponential_base=2,
                                                            )) as _write_client:
            try:
                _write_client.write(influx_bucket, _client.org , data)
            except InfluxDBError as err_:
                print (err_.response.status)
