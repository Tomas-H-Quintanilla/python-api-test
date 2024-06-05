import yaml
import json
import argparse
from modules.VariableTreating import increment_test_variables,replace_within_vars,load_workflow_file,load_variables_from_files
from modules.VariableTreating import save_variables_in_files,load_file_data
from modules.EndpointExecution import execute_endpoints
import copy
from modules.utils import pprint
import os

parser = argparse.ArgumentParser(
    description='Process the file for the test execution.')

parser.add_argument('-f', '--filename', type=str,
                    help='File name of the execution configuration file.')

args = parser.parse_args()

if not args.filename:
    print('No configuration file specified.')
    exit(500)

test_data = None

test_data=load_file_data(args.filename)
test_data['name']=os.path.dirname(args.filename)
if 'variables' not in test_data:
        test_data['variables'] = {}
if test_data == {}:
    raise Exception("Invalid file extension used for the configuration.")

data_save=None
if 'variables_files' in test_data:
    load_variables_from_files(test_data)


increment_test_variables(test_data)
data_save=(copy.deepcopy(test_data))
replace_within_vars(test_data)

load_workflow_file(test_data)

try:
    execute_endpoints(copy.deepcopy(test_data))
except Exception as e:
    print(e)
finally:

    if 'variables_files' not in test_data:
        with open(args.filename, "w") as yaml_file:
            yaml.dump(data_save, yaml_file, sort_keys=False)
    elif data_save:
        save_variables_in_files(data_save)