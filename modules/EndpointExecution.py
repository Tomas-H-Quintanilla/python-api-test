import json
from .APITester import APIClient
import yaml
from .VariableTreating import replace_vars,load_file_data


def is_endpoint_for_execution(endpoint, test_data, endpoint_data):
    endpoint_data = test_data["endpoints"].get(endpoint, {})
    
    if "execute" in endpoint_data:
        return endpoint_data["execute"]
    
    

    if "workflow" in test_data and test_data["workflow"].get("type", "") in {'execute', 'skip'}:
        endpoint_in_workflow = endpoint in test_data["workflow"].get("endpoints", [])

        return endpoint_in_workflow == (test_data["workflow"]["type"]=='execute')
    
    return True

def process_result(test_data,endpoint_data,response):
    dataResponse=response.json()
    test_data["variables"][endpoint_data["result"]["name"]]={"value":dataResponse}

    if "keys"  in endpoint_data["result"]:
        for key in endpoint_data["result"]["keys"]:
            test_data["variables"][endpoint_data["result"]["name"]]["value"]= test_data["variables"][endpoint_data["result"]["name"]]["value"][key]

def request_call(test_data,endpoint_data):
    times = endpoint_data.get("repeat",1)

    for _ in range(times):
        client = APIClient(test_data["servers"][endpoint_data['server']], replace_vars(endpoint_data["url"], test_data['variables']), endpoint_data["method"], endpoint_data.get("headers",[]))
        response=client.check(endpoint_data.get("expected_code",200),endpoint_data.get("expected_text",None),endpoint_data.get('payload',None))

        if "result" in endpoint_data:
           process_result(test_data,endpoint_data,response)
                

def get_payload(endpoint_data,test_data):
    if 'payload_file' in endpoint_data and "payload" not in endpoint_data:
        endpoint_data['payload'] = load_file_data(f'{test_data["name"]}/payloads/{endpoint_data['payload_file']}',test_data['variables'])
    
    elif "payload" in endpoint_data:
        endpoint_data['payload'] = replace_vars(endpoint_data['payload'], test_data['variables'])
                


def execute_endpoint(endpoint, test_data):
    endpoint_data = test_data["endpoints"][endpoint]
    if not is_endpoint_for_execution(endpoint,test_data,endpoint_data):
        return

    get_payload(endpoint_data,test_data)

    if not "url_file" in endpoint_data:
        request_call(test_data,endpoint_data)
    else:
        urls= load_file_data(f'{test_data["name"]}/urls/{endpoint_data['url_file']}',test_data['variables'])
        for url in urls:
            endpoint_data["url"]=url
            request_call(test_data,endpoint_data)
         
       

def execute_endpoints(test_data):
    for endpoint in test_data["endpoints"]:
        execute_endpoint(endpoint, test_data)
