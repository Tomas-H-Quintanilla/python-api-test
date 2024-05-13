import json
from .EndpointExecution import replace_vars
import yaml
def increment_test_variables(test_data,save=False):
    for variable in test_data["variables"]:
        info_variable = test_data["variables"][variable]
        if "increment" in info_variable and info_variable["increment"] and (info_variable["save"] is save) :
            info_variable["value"] += 1

    
def replace_within_vars(test_data):

    content = replace_vars(json.dumps(test_data["variables"]),test_data["variables"])

    test_data["variables"]= json.loads(content)
        
def load_workflow_file(test_data):
    if "workflow_file" in test_data and "workflow" not in test_data:
        file_location= f'workflows/{test_data["name"]}/{test_data['workflow_file']}'
        with open(file_location, 'r') as file:
            if '.json' in file_location:
                test_data['workflow']= json.loads(file.read())
            elif '.yaml' in file_location:
                test_data['workflow']= yaml.safe_load(file.read())
            
def load_variables_from_file(test_data,file_name):
    file_location=f'variables/{test_data["name"]}/{file_name}'
    if 'variables' not in test_data:
        test_data['variables'] = {}
    with open(file_location, 'r') as file:
        data={}
        if '.json' in file_location:
            data= json.loads(file.read())
        elif '.yaml' in file_location:
            data= yaml.safe_load(file.read())
        
        # Keep the value that is not in the file
        for key, value in data.items():
            if key not in test_data['variables']:
                test_data['variables'][key] = value