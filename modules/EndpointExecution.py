import json
from .APITester import APIClient
def load_endpoint_data(json_location, variables):
    with open(json_location, 'r') as file:

        text = file.read()
        for variable in variables:
            text = text.replace(f'${variable}$', f'{variables[variable]['value']}')

        data = json.loads(text)
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
        endpoint_data['payload'] = load_endpoint_data(f'data/{test_data["name"]}/{endpoint_data['payload_file']}', test_data['variables'])
    
    client = APIClient(test_data["servers"][endpoint_data['server']], endpoint_data["url"], endpoint_data["method"], endpoint_data.get("headers",[]))
    client.check(endpoint_data.get("expected_code",200),endpoint_data.get("expected_text",None),endpoint_data.get('payload',None))

def execute_endpoints(test_data):
    for endpoint in test_data["endpoints"]:
        execute_endpoint(endpoint, test_data)
