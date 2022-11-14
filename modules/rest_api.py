'''
Api query to the mikrotik device.
'''
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def mikrotik_api(
            base_url: str,
            url_path: str,
            user_name: str,
            user_pass: str,
            conn_timeout
            ) -> None:
    '''
    Do api connection
    '''
    try:
        with requests.get(
            base_url+url_path,
            auth=(user_name, user_pass),
            verify=False, timeout=conn_timeout, headers={'Connection': 'Close'}
            ) as req_res:
            if req_res.status_code != 200:
                print(
                    f"Something si wrong return code is not 200OK => {req_res.status_code}"
                    f"\n\tPlease the username password and url\n\t url is:{base_url}{url_path}"
                    )
                print(f"{(req_res.text)}")
                return None
            if req_res.json():
                if isinstance(req_res.json(), list):
                    return req_res.json()
                else:
                    return [req_res.json()]
            else:
                return [req_res.text]
    except Exception as err_:
        print (f'Error: {err_}')
