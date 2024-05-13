import json
from .APITester import APIClient
import yaml

def replace_vars(content, variables):
    isJson = False
    if not isinstance(content, str):
        content = json.dumps(content)
        isJson = True

    for variable, value in variables.items():
        content = content.replace(f'${variable}$', str(value['value']))
        
    return json.loads(content) if isJson else content

def load_endpoint_data(location):
    with open(location, 'r') as file:
        if '.json' in location:
            return json.loads(file.read())
        elif '.yaml' in location:
            return yaml.safe_load(file.read())
        return "Invalid format"



def is_endpoint_for_execution(endpoint, test_data, endpoint_data):
    endpoint_data = test_data["endpoints"].get(endpoint, {})
    
    if "execute" in endpoint_data:
        return endpoint_data["execute"]
    
    if "workflow" in test_data:
        endpoint_in_workflow = endpoint in test_data["workflow"].get("endpoints", [])
        is_workflow_execute = test_data["workflow"].get("type", "") == "execute"
        
        return endpoint_in_workflow == is_workflow_execute
    
    return True

def process_result(test_data,endpoint_data,response):
    dataResponse=response.json()
    test_data["variables"][endpoint_data["result"]["name"]]=dataResponse

    if "keys" not in endpoint_data["result"]:
        for key in endpoint_data["result"]["keys"]:
            test_data["variables"][endpoint_data["result"]["name"]]= test_data["variables"][endpoint_data["result"]["name"]][key]

def request_call(test_data,endpoint_data):
    times = endpoint_data.get("repeat",1)

    for _ in range(times):
        client = APIClient(test_data["servers"][endpoint_data['server']], replace_vars(endpoint_data["url"], test_data['variables']), endpoint_data["method"], endpoint_data.get("headers",[]))
        response=client.check(endpoint_data.get("expected_code",200),endpoint_data.get("expected_text",None),endpoint_data.get('payload',None))
        if "result" in endpoint_data:
           process_result(test_data,endpoint_data,response)
                

def get_payload(endpoint_data,test_data):
    if 'payload_file' in endpoint_data and "payload" not in endpoint_data:
        endpoint_data['payload'] = load_endpoint_data(f'data/{test_data["name"]}/{endpoint_data['payload_file']}')
    
    if "payload" in endpoint_data:
        endpoint_data['payload'] = replace_vars(endpoint_data['payload'], test_data['variables'])
                


def execute_endpoint(endpoint, test_data):
    endpoint_data = test_data["endpoints"][endpoint]
    if not is_endpoint_for_execution(endpoint,test_data,endpoint_data):
        return

    get_payload(endpoint_data,test_data)

    if not "url_file" in endpoint_data:
        request_call(test_data,endpoint_data)
    else:
        urls= load_endpoint_data(f'data/{test_data["name"]}/{endpoint_data['url_file']}')
        for url in urls:
            endpoint_data["url"]=url
            request_call(test_data,endpoint_data)
         
       

def execute_endpoints(test_data):
    for endpoint in test_data["endpoints"]:
        execute_endpoint(endpoint, test_data)
