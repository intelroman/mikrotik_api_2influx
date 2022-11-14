'''
Modules to convet values from str to intergers or float
'''

import re

def field_to_int(item) -> int:
    '''
    Convert filed value in interger.
    If the item can't be converte in integer the result will be 0
    '''
    if item is not None:
        try:
            return int(item)
        except ValueError:
            return 0
    else:
        item = 0

def uptime_conv(uptime: str) -> int:
    '''
    Convert time form example: '7w1h11m24s' to seconds
    ppuptime_conv('7w1h11m24s')
    result = 4237884
    '''
    split_uptime: list = []
    result: int = 0
    t0_ : str = '|'.join(re.sub(r'\d+', '', uptime))
    t1_ : str = re.split(t0_, uptime)
    for idx , valu in enumerate(t0_.split('|')):
        split_uptime.append((valu, t1_[idx] ))
    for time_ in split_uptime:
        if time_[0] == 's': # seconds
            result += int(time_[1])
        if time_[0] == 'm': # minutes
            result += (int(time_[1]) * 60)
        if time_[0] == 'h': # hours
            result += (int(time_[1]) * 3600)
        if time_[0] == 'd': # days
            result += (int(time_[1]) * 86400)
        if time_[0] == 'w': # weeks
            result += (int(time_[1]) * 604800)
        #Months and Years should not be present as they can be 2 type of values.
        #Months can be 28, 29, 30, 31 days
        #Years can have 364 or 365 days
    return result
