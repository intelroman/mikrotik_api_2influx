'''
Process rest/system/resource/cpu api.
'''

from typing import Any

import modules.fields_conversion as conv
from models.influx_model import InfluxModel

def firewall(section: str, api_value: dict , measurement_loc: str, time_: Any, api_) -> list:
    '''
    SystemCPU API
    {'firewall_filter':
        [{
            '.id': '*15', ## tags
            'action': 'passthrough', ## tags
            'bytes': '3071457536530', ## field
            'chain': 'forward', ## tags
            'comment': 'special dummy rule to show fasttrack counters', ## tags
            'dynamic': 'true', ## tags
            'packets': '2421844624' ##  field
        }]
    }
    '''
    output = []
    for item_ in api_value[api_]:
        _fields = {
            "packets": conv.field_to_int(item_.get("packets")),
            "bytes": conv.field_to_int(item_.get("bytes")),
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
