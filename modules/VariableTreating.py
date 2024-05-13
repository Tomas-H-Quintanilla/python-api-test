import json

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
        
def load_execute_list(test_data):
    if "execute_list_file" in test_data and "execute_list" not in test_data:
        file_location= f'data/{test_data["name"]}/{test_data['execute_list_file']}'
        with open(file_location, 'r') as file:
            test_data['execute_list'] = json.load(file)
