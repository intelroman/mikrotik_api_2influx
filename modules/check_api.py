'''
Check if i can use the api provide in the list
'''
import json

with open('conf/api.json', 'r', encoding='UTF-8') as f_:
    api_items = json.load(f_)

def items_check(section_, section):
    '''
    Check if the api are availabale in the script list.
    '''
    list_to_use: list = []
    list_not_to_use: list = []
    api_items_list: list = []
    use_api: list = []
    for api_item in api_items:
        if api_item.get('item') and api_item.get("to_flux") is True:
            api_items_list.append(api_item.get('item'))
    for section_item in section_:
        if section_item in api_items_list:
            list_to_use.append(section_item)
        else:
            list_not_to_use.append(section_item)
    for api_item in api_items:
        if api_item.get('item') in list_to_use:
            use_api.append((api_item.get('item'), api_item.get('url'), section))
    return use_api, list_not_to_use
