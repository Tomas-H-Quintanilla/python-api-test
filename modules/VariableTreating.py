import json

def increment_test_variables(test_data):
    for variable in test_data["variables"]:
        info_variable = test_data["variables"][variable]
        if info_variable["increment"]:
            info_variable["value"] += 1
            
def load_execute_list(test_data):
    if "execute_list_file" in test_data and "execute_list" not in test_data:
        file_location= f'data/{test_data["name"]}/{test_data['execute_list_file']}'
        with open(file_location, 'r') as file:
            test_data['execute_list'] = json.load(file)
