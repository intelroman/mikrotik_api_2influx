'''
Different varibales to be loaded when needed.
'''
import os

if os.getenv('MIKROTIK_API_PATH') is not None:
    DEFAULT_PATH = os.getenv('MIKROTIK_API_PATH')
else:
    DEFAULT_PATH = './'
