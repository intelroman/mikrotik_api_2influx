'''
Process rest/system/resource/cpu api.
'''
import re
from typing import Any

import modules.fields_conversion as conv
from models.influx_model import InfluxModel

def system_cpu(section: str, api_value: dict , measurement_loc: str, time_: Any, api_) -> list:
    '''
    SystemCPU API
    {'system_cpu':
        [{
            '.id': '*0', ## None
            'cpu': 'cpu0', ## tag
            'disk': '0', ## field
            'irq': '0', ## field
            'load': '0' ## field
        }]
    }
    '''
    output = []
    for item_ in api_value[api_]:
        _fields = {
            "load": conv.field_to_int(item_.get("load")),
            "disk": conv.field_to_int(item_.get("disk")),
            "irq": conv.field_to_int(item_.get("irq"))
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

def system_resources(section: str, api_value: dict, measurement_loc: str, time_: Any, api_) -> list:
    '''
    Mikrotik resources:
        {'system_resources':
            [{
                'architecture-name': 'arm64', ## tags
                'board-name': 'CCR2004-1G-12S+2XS', ## tags
                'build-time': 'Aug/30/2022 09:25:53', ## tags
                'cpu': 'ARM64', ## tags
                'cpu-count': '4', ## field
                'cpu-load': '0', ## field
                'factory-software': '6.46.4', ## tags
                'free-hdd-space': '90357760', ## field
                'free-memory': '3870883840', ## field
                'platform': 'MikroTik', ## tags
                'total-hdd-space': '135266304', ## field
                'total-memory': '4227858432', ## field
                'uptime': '7w1h11m24s', ## field
                'version': '7.5 (stable)' ## tags
                }]
        }
    '''
    output = []
    for item_ in api_value[api_]:
        _fields = {
            "cpu-count": conv.field_to_int(item_.get("cpu-count")),
            "cpu-load": conv.field_to_int(item_.get("cpu-load")),
            "free-hdd-space": conv.field_to_int(item_.get("free-hdd-space")),
            "free-memory": conv.field_to_int(item_.get("free-memory")),
            "total-hdd-space": conv.field_to_int(item_.get("total-hdd-space")),
            "total-memory": conv.field_to_int(item_.get("total-memory")),
            "uptime": conv.uptime_conv(item_.get("uptime"))
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
    return []

def system_health(section: str, api_value: dict, measurement_loc: str, time_: Any, api_) -> list:
    '''
    Mikrotik heath:
    {'system_health':[{
        '.id': '*E', ## tags
        'name': 'temperature', ## tags
        'type': 'C', ## tags
        'value': '65' ## field
        }]}
    '''
    output = []
    for item_ in api_value[api_]:
        _fields = {
            "value": conv.field_to_int(item_.get("value"))
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

def system_irq(section: str, api_value: dict, measurement_loc: str, time_: Any, api_) -> list:
    '''
    Mikrotik irq:
    {'system_irq':[{
        ".id": "*5", ## tags
        "active-cpu": "0", ## tags
        "count": "0", ## fields
        "cpu": "auto", ## tags
        "irq": "5", ## tags
        "per-cpu-count": "0,0,0,0", ## fields
        "read-only": "false", ## tags
        "users": "arm-pmu" ## tags
    }]}
    '''
    output = []
    for item_ in api_value[api_]:
        _fields = {
            "count": conv.field_to_int(item_.get("count")), ## fields
            }
        for idx, item_value in enumerate(item_.get("per-cpu-count").split(",")):
            _fields.update({
                f'per-cpu-{idx}-count': conv.field_to_int(item_value)
                })
        _tags = item_.copy()
        #Unique fields keys
        #tuple(set([re.sub('(-\d+-)' , '', key) for key in a.keys()]))
        _sub = '(-\d+-)'
        # Removing multiple keys for a dict
        # >>> d = {'a': 'valueA', 'b': 'valueB', 'c': 'valueC', 'd': 'valueD'}
        # >>> keys = ['a', 'b', 'c']
        # >>> list(map(d.pop, keys))
        # ['valueA', 'valueB', 'valueC']
        to_remove_fields = tuple(set([re.sub(_sub , '-', key) for key in _fields]))
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
