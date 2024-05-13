import json
from .APITester import APIClient

def replace_vars(content, variables):
    isJson = False
    if not isinstance(content, str):
        content = json.dumps(content)
        isJson = True

    for variable, value in variables.items():
        content = content.replace(f'${variable}$', str(value['value']))
        
    return json.loads(content) if isJson else content

def load_endpoint_data(json_location):
    with open(json_location, 'r') as file:
        data = json.loads(file.read())
        return data

def is_endpoint_for_execution(endpoint,test_data,endpoint_data):
    endpoint_data = test_data["endpoints"][endpoint]
    response=True

    if "execute" in endpoint_data:
        response= endpoint_data["execute"]
    elif "execute_list" in test_data and endpoint in test_data["execute_list"]:
        response= test_data["execute_list"]["endpoint"]

    return response

def execute_endpoint(endpoint, test_data):
    endpoint_data = test_data["endpoints"][endpoint]
    if not is_endpoint_for_execution(endpoint,test_data,endpoint_data):
        return
    if 'payload_file' in endpoint_data and "payload" not in endpoint_data:
        endpoint_data['payload'] = load_endpoint_data(f'data/{test_data["name"]}/{endpoint_data['payload_file']}')
    
    if "payload" in endpoint_data:
        endpoint_data['payload'] = replace_vars(endpoint_data['payload'], test_data['variables'])
    
    times = endpoint_data.get("repeat",1)
    for _ in range(times):     
        client = APIClient(test_data["servers"][endpoint_data['server']], replace_vars(endpoint_data["url"], test_data['variables']), endpoint_data["method"], endpoint_data.get("headers",[]))
        client.check(endpoint_data.get("expected_code",200),endpoint_data.get("expected_text",None),endpoint_data.get('payload',None))

def execute_endpoints(test_data):
    for endpoint in test_data["endpoints"]:
        execute_endpoint(endpoint, test_data)
