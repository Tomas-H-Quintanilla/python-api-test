import json
import yaml


VARIABLE_SEPARATOR="@"


def replace_from_keys(content,variable,variables):
    variable_text=f'${variable}{VARIABLE_SEPARATOR}'+content.split(f'${variable}{VARIABLE_SEPARATOR}')[1].split('$')[0]
    keys=variable_text[1:].split(f'{VARIABLE_SEPARATOR}')
    value=variables[keys[0]]["value"]
    keys.pop(0)
    for key in keys:
        value=value[key]
    
    return content.replace(f'{variable_text}$', str(value))
        

def replace_vars(content, variables):
    isJson = False
    if not isinstance(content, str):
        content = json.dumps(content)
        isJson = True

    for variable, value in variables.items():
        if variable in content:
            content = content.replace(f'${variable}$', str(value['value']))
        if f'${variable}{VARIABLE_SEPARATOR}' in content:
            content=replace_from_keys(content,variable,variables)

        
    return json.loads(content) if isJson else content


def load_file_data(location,variables=None):
    with open(location, 'r') as file:
        content=file.read()
        if variables is not None:
            content=replace_vars(content,variables)

        if '.json' in location:
            return json.loads(content)
        elif '.yaml' in location:
            return yaml.safe_load(content)
        return content


def increment_test_variables(test_data):
    for variable in test_data["variables"]:
        info_variable = test_data["variables"][variable]
        if "increment" in info_variable and info_variable["increment"]:
            info_variable["value"] += info_variable["increment"]

    
def replace_within_vars(test_data):

    content = replace_vars(json.dumps(test_data["variables"]),test_data["variables"])

    test_data["variables"]= json.loads(content)
        
def load_workflow_file(test_data):
    if "workflow_file" in test_data and "workflow" not in test_data:
        test_data['workflow']=load_file_data(f'{test_data["name"]}/workflows/{test_data['workflow_file']}')
            
def load_variables_from_file(test_data,file_name):
    file_location=f'{test_data["name"]}/variables/{file_name}'

    data= load_file_data(file_location)

    for key, value in data.items():
        if key not in test_data['variables']:
            test_data['variables'][key] = value
            test_data['variables'][key]['file']=file_name

def load_servers_file(test_data):
    if 'servers' not in test_data:
        test_data['servers']={}

    if "servers_file" in test_data:
        data_servers=load_file_data(f'{test_data["name"]}/servers/{test_data['servers_file']}')
        for server in data_servers:
            if server not in test_data["servers"]:
                test_data['servers'][server]=data_servers[server]

def load_endpoints_files(test_data):
        
    if 'endpoints' not in test_data:
        test_data['endpoints']={}

    if "endpoints_files" in test_data:
        for endpoint_file in test_data["endpoints_files"]:
            data_endpoints=load_file_data(f'{test_data["name"]}/endpoints/{endpoint_file}')
            for endpoint in data_endpoints:
                if endpoint not in test_data:
                    test_data['endpoints'][endpoint]=data_endpoints[endpoint]
    

def load_variables_from_files(test_data):
    if 'variables_files' in test_data:
        for file_name in test_data['variables_files']:
            load_variables_from_file(test_data,file_name)

def save_variables_in_file(data_save,file_name):
    file_location=f'{data_save["name"]}/variables/{file_name}'
    variables_save={}

    for variable_name in data_save['variables']:
        if 'file' not in data_save['variables'][variable_name] or file_name!=data_save['variables'][variable_name]['file']:
            continue
        variables_save[variable_name]=data_save['variables'][variable_name]

    with open(file_location, 'w') as file:
        if '.json' in file_location:
            json.dump(variables_save,file)
        elif '.yaml' in file_location:
            yaml.dump(variables_save, file, sort_keys=False)

def save_variables_in_files(data_save):
    for file_name in data_save['variables_files']:
        save_variables_in_file(data_save,file_name)