'''
Process rest/system/resource/cpu api.
'''

from typing import Any

import modules.fields_conversion as conv
from models.influx_model import InfluxModel

def ipsec_stats(section: str, api_value: dict , measurement_loc: str, time_: Any, api_: str) -> list:
    '''
    ipsec
    {'ipsec_statistics':
        [{
        'in-buffer-errors': '0', ## field
        'in-errors': '0', ## field
        'in-header-errors': '0', ## field
        'in-no-policies': '0', ## field
        'in-no-states': '0', ## field
        'in-policy-blocked': '0', ## field
        'in-policy-errors': '0', ## field
        'in-state-expired': '0', ## field
        'in-state-invalid': '0', ## field
        'in-state-mismatches': '0', ## field
        'in-state-mode-errors': '0', ## field
        'in-state-protocol-errors': '0', ## field
        'in-state-sequence-errors': '0', ## field
        'in-template-mismatches': '0', ## field
        'out-bundle-check-errors': '0', ## field
        'out-bundle-errors': '0', ## field
        'out-errors': '0', ## field
        'out-no-states': '57', ## field
        'out-policy-blocked': '0', ## field
        'out-policy-dead': '0', ## field
        'out-policy-errors': '0', ## field
        'out-state-expired': '0', ## field
        'out-state-mode-errors': '1', ## field
        'out-state-protocol-errors': '0', ## field
        'out-state-sequence-errors': '0' ## field
        }]
    }
    '''
    output = []
    for item_ in api_value['ipsec_statistics']:
        _fields = {
            "in-buffer-errors": conv.field_to_int(item_.get("in-buffer-errors")),
            "in-errors": conv.field_to_int(item_.get("in-errors")),
            "in-header-errors": conv.field_to_int(item_.get("in-header-errors")),
            "in-no-policies": conv.field_to_int(item_.get("in-no-policies")),
            "in-no-states": conv.field_to_int(item_.get("in-no-states")),
            "in-policy-blocked": conv.field_to_int(item_.get("in-policy-blocked")),
            "in-policy-errors": conv.field_to_int(item_.get("in-policy-errors")),
            "in-state-expired": conv.field_to_int(item_.get("in-state-expired")),
            "in-state-invalid": conv.field_to_int(item_.get("in-state-invalid")),
            "in-state-mismatches": conv.field_to_int(item_.get("in-state-mismatches")),
            "in-state-mode-errors": conv.field_to_int(item_.get("in-state-mode-errors")),
            "in-state-protocol-errors": conv.field_to_int(item_.get("in-state-protocol-errors")),
            "in-state-sequence-errors": conv.field_to_int(item_.get("in-state-sequence-errors")),
            "in-template-mismatches": conv.field_to_int(item_.get("in-template-mismatches")),
            "out-bundle-check-errors": conv.field_to_int(item_.get("out-bundle-check-errors")),
            "out-bundle-errors": conv.field_to_int(item_.get("out-bundle-errors")),
            "out-errors": conv.field_to_int(item_.get("out-errors")),
            "out-no-states": conv.field_to_int(item_.get("out-no-states")),
            "out-policy-blocked": conv.field_to_int(item_.get("out-policy-blocked")),
            "out-policy-dead": conv.field_to_int(item_.get("out-policy-dead")),
            "out-policy-errors": conv.field_to_int(item_.get("out-policy-errors")),
            "out-state-expired": conv.field_to_int(item_.get("out-state-expired")),
            "out-state-mode-errors": conv.field_to_int(item_.get("out-state-mode-errors")),
            "out-state-protocol-errors": conv.field_to_int(item_.get("out-state-protocol-errors")),
            "out-state-sequence-errors": conv.field_to_int(item_.get("out-state-sequence-errors"))
            }
        _tags = {
            "router": section,
            "type": api_

        }
        output.append({
            "measurement" : measurement_loc,
            "fields": _fields,
            "tags" : _tags,
            "time": time_
            })
    if bool(InfluxModel(Output=output)):
        return output
