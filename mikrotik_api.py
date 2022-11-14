"""
Start imports
"""
import argparse
import configparser
import datetime
import threading
import multiprocessing
import modules.check_api
import modules.data_gathering
import modules.string_format
from modules.to_influx import (interfaces,
                               system,
                               write_to,
                               ipsec,
                               firewall,
                               queue)

parser = argparse.ArgumentParser()
parser.add_argument("--display", "-d", default=False,
                    help="Display the stats instead of write to influxdb")
parser.add_argument("--multiprocess", "-mp", default=True,
                    help="Enable disable multiprocess on api requests")
args = parser.parse_args()

def main() -> None:
    '''
    Main function where everyting starts.
    Check each section for items and ensure the api is implemented for that item.
    '''
    conf = configparser.ConfigParser()
    conf.read('conf/config.ini')
    data: list = []
    use_api: list = []
    time_ = datetime.datetime.now()
    for section in conf.sections():
        if conf[section].get('items') is not None:
            conf_section_items = modules.string_format.replace_spaces(conf[section]['items'], "")
            _apis, _ = modules.check_api.items_check(conf_section_items.split(","), section)
            for api in _apis:
                use_api.append(api)

        # Using Multiprocess to gather the data.
    if args.multiprocess is True:
        # print ("Using multiprocesses module")
        mgr = multiprocessing.Manager()
        data = mgr.list()
        jobs = [
                multiprocessing.Process(
                    target=modules.data_gathering.data_gathering,
                    args=(api_value, section, api_, data)
                    )
                for api_, api_value, section in use_api
                ]
        for j in jobs:
            j.start()
        for j in jobs:
            j.join()

    # Using Threads instead of multiprocess if this to much for router CPU.
    else:
        # print("Using threads")
        api_threads: list = []
        for api_, api_value, section in use_api:
            thread_job = threading.Thread(
                    target=modules.data_gathering.data_gathering,
                    args=(api_value, section, api_, data)
                    )
            api_threads.append(thread_job)
            thread_job.start()
        for _, api_thread in enumerate(api_threads):
            api_thread.join()

    # - Looping thru the collected data,
    # - format the data for the influxdb (flux language)
    # - push data to influx server
    for data_ in data:

        #-------------------
        # Interfaces Section
        # BASE_URL: /rest/ + RES_URL
        #-------------------
        # Interfaces
        # RES_URL: interface
        #-------------------
        if data_.get("interfaces") and isinstance(data_.get("interfaces")[0], dict):
            result = interfaces.interfaces(data_.get("mikrotik_device"),
                                                data_,
                                                conf[data_.get("mikrotik_device")]['bucket'],
                                                time_,
                                                'interfaces')
            if args.display is False:
                write_to.write(result, conf[data_.get("mikrotik_device")]['bucket'])
            else: print (f"API interfaces:\n\t{result}\n")

        #---------------
        # System section
        # BASE URL: /rest/system/ + RES_URL
        #---------------
        # Resources CPU
        # RES_URL: resource/cpu
        #----------------------
        if data_.get("system_cpu") and isinstance(data_.get("system_cpu")[0], dict):
            result = system.system_cpu(data_.get("mikrotik_device"),
                                                data_,
                                                conf[data_.get("mikrotik_device")]['bucket'],
                                                time_,
                                                'system_cpu')
            if args.display is False:
                write_to.write(result, conf[data_.get("mikrotik_device")]['bucket'])
            else: print (f"API system_cpu:\n\t{result}\n")
        #----------
        # Resources
        # RES_URL: resource
        #----------
        if data_.get("system_resources") and isinstance(data_.get("system_resources")[0], dict):
            result  = system.system_resources(data_.get("mikrotik_device"),
                                                data_,
                                                conf[data_.get("mikrotik_device")]['bucket'],
                                                time_,
                                                'system_resources')
            if args.display is False:
                write_to.write(result, conf[data_.get("mikrotik_device")]['bucket'])
            else: print (f"API system_resources:\n\t{result}\n")
        #--------------
        # System health
        # RES_URL: health
        #--------------
        if data_.get("system_health") and isinstance(data_.get("system_health")[0], dict):
            result  = system.system_health(data_.get("mikrotik_device"),
                                                data_,
                                                conf[data_.get("mikrotik_device")]['bucket'],
                                                time_,
                                                'system_health')
            if args.display is False:
                write_to.write(result, conf[data_.get("mikrotik_device")]['bucket'])
            else: print (f"API system_health:\n\t{result}\n")
        #--------------
        # System irq
        # RES_URL: resource/irq
        #--------------
        if data_.get("system_irq") and isinstance(data_.get("system_irq")[0], dict):
            result  = system.system_irq(data_.get("mikrotik_device"),
                                                data_,
                                                conf[data_.get("mikrotik_device")]['bucket'],
                                                time_,
                                                'system_irq')
            if args.display is False:
                write_to.write(result, conf[data_.get("mikrotik_device")]['bucket'])
            else: print (f"API system_irq:\n\t{result}\n")

        #-----------------
        # FIREWALL Section
        # BASE URL: /rest/ip/firewall/ + RES_URL
        #-----------------
        # Firewall Filter
        # RES_URL: filter
        #----------------
        if data_.get("firewall_filter") and isinstance(data_.get("firewall_filter")[0], dict):
            result  = firewall.firewall(data_.get("mikrotik_device"),
                                            data_,
                                            conf[data_.get("mikrotik_device")]['bucket'],
                                            time_,
                                            'firewall_filter')
            if args.display is False:
                write_to.write(result, conf[data_.get("mikrotik_device")]['bucket'])
            else: print (f"API firewall filter:\n\t{result}\n")
        #-------------
        # Firewall NAT
        # RES_URL: nat
        #-------------
        if data_.get("firewall_nat") and isinstance(data_.get("firewall_nat")[0], dict):
            result  = firewall.firewall(data_.get("mikrotik_device"),
                                            data_,
                                            conf[data_.get("mikrotik_device")]['bucket'],
                                            time_,
                                            'firewall_nat')
            if args.display is False:
                write_to.write(result, conf[data_.get("mikrotik_device")]['bucket'])
            else: print (f"API firewall nat:\n\t{result}\n")
        #----------------
        # Firewall Mangle
        # RES_URL: mangle
        #----------------
        if data_.get("firewall_mangle") and isinstance(data_.get("firewall_mangle")[0], dict):
            result  = firewall.firewall(data_.get("mikrotik_device"),
                                            data_,
                                            conf[data_.get("mikrotik_device")]['bucket'],
                                            time_,
                                            'firewall_mangle')
            if args.display is False:
                write_to.write(result, conf[data_.get("mikrotik_device")]['bucket'])
            else: print (f"API firewall mangle:\n\t{result}\n")
        #-------------
        # Firewall RAW
        # RES_URL: raw
        #-------------
        if data_.get("firewall_raw") and isinstance(data_.get("firewall_raw")[0], dict):
            result  = firewall.firewall(data_.get("mikrotik_device"),
                                            data_,
                                            conf[data_.get("mikrotik_device")]['bucket'],
                                            time_,
                                            'firewall_raw')
            if args.display is False:
                write_to.write(result, conf[data_.get("mikrotik_device")]['bucket'])
            else: print (f"API firewall raw:\n\t{result}\n")

        #--------------
        # IPSEC Section
        # BASE_URL: /rest/ip/ipsec/ + RES_URL
        #--------------
        # IPSEC Statistics
        # RES_URL: statistics
        #--------------
        if data_.get("ipsec_statistics") and isinstance(data_.get("ipsec_statistics")[0], dict):
            result  = ipsec.ipsec_stats(data_.get("mikrotik_device"),
                                            data_,
                                            conf[data_.get("mikrotik_device")]['bucket'],
                                            time_,
                                            'ipsec_stats')
            if args.display is False:
                write_to.write(result, conf[data_.get("mikrotik_device")]['bucket'])
            else: print (f"API ipsec_statistics:\n\t{result}\n")

        #--------------
        # Queue Section
        # BASE_URL: /rest/queue/ + RES_URL
        #--------------
        # Simple queue
        # RES_URL: simple
        #--------------
        if data_.get("simple_queue") and isinstance(data_.get("simple_queue")[0], dict):
            result  = queue.simple_queue(data_.get("mikrotik_device"),
                                            data_,
                                            conf[data_.get("mikrotik_device")]['bucket'],
                                            time_,
                                            'simple_queue')
            if args.display is False:
                write_to.write(result, conf[data_.get("mikrotik_device")]['bucket'])
            else: print (f"API simple queues:\n\t{result}\n")
        #-----------
        # Tree Queue
        # RES_URL: tree
        #-----------
        if data_.get("tree_queue") and isinstance(data_.get("tree_queue")[0], dict):
            result  = queue.tree_queue(data_.get("mikrotik_device"),
                                            data_,
                                            conf[data_.get("mikrotik_device")]['bucket'],
                                            time_,
                                            'tree_queue')
            if args.display is False:
                write_to.write(result, conf[data_.get("mikrotik_device")]['bucket'])
            else: print (f"API tree queue:\n\t{result}\n")

if __name__ == "__main__":
    main()
