import json

import yaml
def increment_test_variables(test_data,save=False):
    for variable in test_data["variables"]:
        info_variable = test_data["variables"][variable]
        if "increment" in info_variable and info_variable["increment"] and (info_variable["save"] is save) :
            info_variable["value"] += 1

    
def replace_within_vars(test_data):

    content = json.dumps(test_data["variables"])
    for variable, value in test_data["variables"].items():
            content = content.replace(f'${variable}$',str(value['value']))

    return json.loads(content)
        
def load_workflow_file(test_data):
    if "workflow_file" in test_data and "workflow" not in test_data:
        file_location= f'workflows/{test_data["name"]}/{test_data['workflow_file']}'
        with open(file_location, 'r') as file:
            if '.json' in file_location:
                test_data['workflow']= json.loads(file.read())
            elif '.yaml' in file_location:
                test_data['workflow']= yaml.safe_load(file.read())
            
