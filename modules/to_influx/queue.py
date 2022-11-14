'''
Process queues output.
'''
import re
from typing import Any

import modules.fields_conversion as conv
from models.influx_model import InfluxModel

def simple_queue(section: str, api_value: dict , measurement_loc: str, time_: Any, api_) -> list:
    '''
    Simple queues API
    {'simple_queues':
        [{
            ".id": "*4", ## tags
            "bucket-size": "0.1/0.1", ## tags Target-Upload/Target-Download
            "burst-limit": "1000000011/1000000011", ## tags Target-Upload/Target-Download
            "burst-threshold": "1000000002/1000000002", ## tags Target-Upload/Target-Download
            "burst-time": "1653w3d1h46m43s/1653w3d1h46m43s", ## tags Target-Upload/Target-Download
            "bytes": "45666/172388", ## fields Target-Upload/Target-Download
            "disabled": "false", ## tags
            "dropped": "0/0", ## fields Target-Upload/Target-Download
            "dynamic": "false", ## tags
            "invalid": "false", ## tags
            "limit-at": "0/0", ## tags Target-Upload/Target-Download
            "max-limit": "1000000000/1000000000", ## tags Target-Upload/Target-Download
            "name": "queue1", ## tags
            "packet-marks": "", ## tags
            "packet-rate": "16/30", ## fields Target-Upload/Target-Download
            "packets": "457/888", ## fields Target-Upload/Target-Download
            "parent": "none", ## tags
            "priority": "8/8", ## tags Target-Upload/Target-Download
            "queue": "default-small/default-small", ## tags Target-Upload/Target-Download
            "queued-bytes": "0/0", ## fields Target-Upload/Target-Download
            "queued-packets": "0/0", ## fields Target-Upload/Target-Download
            "rate": "17424/62464", ## fields Target-Upload/Target-Download
            "target": "", ## tags
            "total-bytes": "0", ## filed
            "total-dropped": "0", ## field
            "total-packet-rate": "0", ## field
            "total-packets": "0", ## field
            "total-queued-bytes": "0", ## field
            "total-queued-packets": "0", ## field
            "total-rate": "0" ##field
        }]
    }
    '''
    output = []
    for item_ in api_value[api_]:
        _fields = {
            "bytes-Target-Upload": conv.field_to_int(item_.get("bytes").split("/")[0]),
            "bytes-Target-Download": conv.field_to_int(item_.get("bytes").split("/")[1]),
            "dropped-Target-Upload": conv.field_to_int(item_.get("dropped").split("/")[0]),
            "dropped-Target-Download": conv.field_to_int(item_.get("dropped").split("/")[1]),
            "packet-rate-Target-Upload": conv.field_to_int(item_.get("packet-rate").split("/")[0]),
            "packet-rate-Target-Download": conv.field_to_int(item_.get("packet-rate").split("/")[1]),
            "packets-Target-Upload": conv.field_to_int(item_.get("packets").split("/")[0]),
            "packets-Target-Download": conv.field_to_int(item_.get("packets").split("/")[1]),
            "queued-bytes-Target-Upload": conv.field_to_int(item_.get("queued-bytes").split("/")[0]),
            "queued-bytes-Target-Download": conv.field_to_int(item_.get("queued-bytes").split("/")[1]),
            "queued-packets-Target-Upload": conv.field_to_int(item_.get("queued-packets").split("/")[0]),
            "queued-packets-Target-Download": conv.field_to_int(item_.get("queued-packets").split("/")[1]),
            "rate-Target-Upload": conv.field_to_int(item_.get("rate").split("/")[0]),
            "rate-Target-Download": conv.field_to_int(item_.get("rate").split("/")[1]),
            "total-bytes": conv.field_to_int(item_.get("total-bytes")),
            "total-dropped": conv.field_to_int(item_.get("total-dropped")),
            "total-packet-rate": conv.field_to_int(item_.get("total-packet-rate")),
            "total-packets": conv.field_to_int(item_.get("total-packets")),
            "total-queued-bytes": conv.field_to_int(item_.get("total-queued-bytes")),
            "total-queued-packets": conv.field_to_int(item_.get("total-queued-packets")),
            "total-rate": conv.field_to_int(item_.get("total-rate"))
            }
        _tags = item_.copy()
        #Unique fields keys
        #tuple(set([re.sub('(-Target-Upload|-Target-Download)' , '', key) for key in a.keys()]))
        _sub = '(-Target-Upload|-Target-Download)'
        # Removing multiple keys for a dict
        # >>> d = {'a': 'valueA', 'b': 'valueB', 'c': 'valueC', 'd': 'valueD'}
        # >>> keys = ['a', 'b', 'c']
        # >>> list(map(d.pop, keys))
        # ['valueA', 'valueB', 'valueC']
        to_remove_fields = tuple(set([re.sub(_sub , '', key) for key in _fields]))
        list(map(_tags.__delitem__, filter(_tags.__contains__,to_remove_fields)))
        _tags.update({
                    "router": section,
                    "type": api_
                    })
        output.append({
            "measurement" : measurement_loc,
            "fields": _fields,
            "tags" : _tags,
            "time": time_
            })
    if bool(InfluxModel(Output=output)):
        return output

def tree_queue(section: str, api_value: dict , measurement_loc: str, time_: Any, api_) -> list:
    '''
    Tree queues API
    {'tree_queues':
        [
    {
        ".id": "*1000005", ## tags
        "bucket-size": "0.1", ## tags
        "burst-limit": "13000000000", ## tags
        "burst-threshold": "9500000000", ## tags
        "burst-time": "59s", ## tags
        "bytes": "28841743", ##field
        "disabled": "false", ## tags
        "dropped": "0", ##field
        "invalid": "false", ## tags
        "limit-at": "12000000000", ## tags
        "max-limit": "12000000000", ## tags
        "name": "queue1", ## tags
        "packet-mark": "no-mark", ## tags
        "packet-rate": "41", ##field
        "packets": "55519", ##field
        "parent": "global", ## tags
        "priority": "8", ## tags
        "queue": "default-small", ## tags
        "queued-bytes": "0", ##field
        "queued-packets": "0", ##field
        "rate": "254232" ##field
    }
]
    }
    '''
    output = []
    for item_ in api_value[api_]:
        _fields = {
                "bytes": conv.field_to_int(item_.get("bytes")),
                "dropped": conv.field_to_int(item_.get("dropped")),
                "packet-rate": conv.field_to_int(item_.get("packet-rate")),
                "packets": conv.field_to_int(item_.get("packets")),
                "queued-bytes": conv.field_to_int(item_.get("queued-bytes")),
                "queued-packets": conv.field_to_int(item_.get("queued-packets")),
                "rate": conv.field_to_int(item_.get("rate"))
            }
        _tags = item_.copy()
        # Removing multiple keys for a dict
        # >>> d = {'a': 'valueA', 'b': 'valueB', 'c': 'valueC', 'd': 'valueD'}
        # >>> keys = ['a', 'b', 'c']
        # >>> list(map(d.pop, keys))
        # ['valueA', 'valueB', 'valueC']
        list(map(_tags.__delitem__, filter(_tags.__contains__,tuple(_fields.keys()))))
        _tags.update({
                    "router": section,
                    "type": api_
                    })
        output.append({
            "measurement" : measurement_loc,
            "fields": _fields,
            "tags" : _tags,
            "time": time_
            })
    if bool(InfluxModel(Output=output)):
        return output
