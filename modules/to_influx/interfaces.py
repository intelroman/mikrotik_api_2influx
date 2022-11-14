'''
Process interfaces output.
'''

from typing import Any

import modules.fields_conversion as conv
from models.influx_model import InfluxModel

def interfaces(section: str, api_value: dict , measurement_loc: str, time_: Any, api_) -> list:
    '''
    Interfaces API
    {'interfaces':
        [{
            '.id': '*B',
            'actual-mtu': '9204',
            'default-name': 'sfp-sfpplus10',
            'disabled': 'false',
            'fp-rx-byte': '0',
            'fp-rx-packet': '0',
            'fp-tx-byte': '0',
            'fp-tx-packet': '0',
            'l2mtu': '9578',
            'link-downs': '0',
            'mac-address': '08:55:31:55:EF:6D',
            'max-l2mtu': '9578',
            'mtu': '9204',
            'name': 'Cisco10GTenG0/2-Trunk-2-4094',
            'running': 'false',
            'rx-byte': '0',
            'rx-packet': '0',
            'tx-byte': '0',
            'tx-packet': '0',
            'tx-queue-drop': '0',
            'type': 'ether'
        }]
    }
    '''
    output = []
    for item_ in api_value[api_]:
        _fields = {
            "fp-rx-byte": conv.field_to_int(item_.get("fp-rx-byte")),
            "fp-rx-packet": conv.field_to_int(item_.get("fp-rx-packet")),
            "fp-tx-byte": conv.field_to_int(item_.get("fp-tx-byte")),
            "fp-tx-packet": conv.field_to_int(item_.get("fp-tx-packet")),
            "rx-byte": conv.field_to_int(item_.get("rx-byte")),
            "rx-drop": conv.field_to_int(item_.get("rx-drop")),
            "rx-error": conv.field_to_int(item_.get("rx-error")),
            "rx-packet": conv.field_to_int(item_.get("rx-packet")),
            "tx-byte": conv.field_to_int(item_.get("tx-byte")),
            "tx-drop": conv.field_to_int(item_.get("tx-drop")),
            "tx-error": conv.field_to_int(item_.get("tx-error")),
            "tx-packet": conv.field_to_int(item_.get("tx-packet")),
            "tx-queue-drop": conv.field_to_int(item_.get("tx-queue-drop")),
            "link-down": conv.field_to_int(item_.get("link-down"))
            }
        _tags = item_.copy()
        # Removing multiple keys for a dict
        # >>> d = {'a': 'valueA', 'b': 'valueB', 'c': 'valueC', 'd': 'valueD'}
        # >>> keys = ['a', 'b', 'c']
        # >>> list(map(d.pop, keys))
        # ['valueA', 'valueB', 'valueC']
        list(map(_tags.__delitem__, filter(_tags.__contains__,tuple(_fields.keys()))))
        _tags.update({"router": section})
        output.append({
            "measurement" : measurement_loc,
            "fields": _fields,
            "tags" : _tags,
            "time": time_
            })
    if bool(InfluxModel(Output=output)):
        return output