'''
String formating modules.
'''
import re


def replace_spaces(data, replace_with, **kwargs) -> str:
    '''
    replace spaces with the specific string of char
    example:
    replace_spaces("   What is  Lorem   Ipsum?   ", ";")
    Output
        ";What;is;Lorem;Ipsum?;"
    or
    This example will replace the start space and end spaces with no space.
    replace_spaces("   What is  Lorem   Ipsum?   ", ";", replace_begining="", replace_end="")
    This example will replace the start space and end spaces with no space.
    Output
        " What;is;Lorem;Ipsum?"
    '''
    if kwargs.get('replace_begin') is not None:
        data = re.sub(r'^[\s]+', kwargs.get('remove_start'), data )
    if kwargs.get('replace_end') is not None:
        data = re.sub(r'[\s]+$', kwargs.get('remove_end'), data )
    data = re.sub(r'[\s]+', replace_with, data )
    return data
    