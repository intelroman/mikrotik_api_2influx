'''
Gathering information
'''
import configparser

from .rest_api import mikrotik_api

cnf = configparser.ConfigParser()
cnf.read('conf/config.ini')

def data_gathering(api_value, section, api_, _data: list):
    '''
    Gather the information base by the config.ini
    '''
    final_data = {}
    data = mikrotik_api(
        f"{cnf[section]['protocol']}://{cnf[section]['host']}:{cnf[section]['port']}/",
        f"{api_value}",
        f"{cnf[section]['user']}",
        f"{cnf[section]['pass']}",
        int(cnf[section]['connection_timeout'])
        )
    if isinstance(data, list):
        final_data.update({api_ : data, "mikrotik_device": section})
    else:
        print(
            "Check the api:",
            f"{cnf[section]['protocol']}://{cnf[section]['host']}:{cnf[section]['port']}/{api_value}",
            f"data class is: {type(data)}, excpecting List")
    _data.append(final_data)
