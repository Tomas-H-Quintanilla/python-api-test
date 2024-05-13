import yaml
import json
import argparse
from modules.VariableTreating import increment_test_variables,replace_within_vars
from modules.EndpointExecution import execute_endpoints
import copy
from modules.utils import pprint

parser = argparse.ArgumentParser(
    description='Process the file for the test execution.')

parser.add_argument('-f', '--filename', type=str,
                    help='File name of the execution configuration file.')

args = parser.parse_args()

if not args.filename:
    print('No configuration file specified.')
    exit(500)

test_data = None

with open(args.filename, "r") as file:
    if args.filename.endswith(".yaml"):
        test_data = yaml.safe_load(file)
    elif args.filename.endswith(".json"):
        test_data = json.load(file)
    else:
        raise Exception("Invalid file extension used for the configuration.")
    
    increment_test_variables(test_data,True)
    data_save=(copy.deepcopy(test_data))
    increment_test_variables(test_data,False)
    replace_within_vars(test_data)

try:
    execute_endpoints(copy.deepcopy(test_data))
except Exception as e:
    print(e)
finally:
    with open(args.filename, "w") as yaml_file:
        yaml.dump(data_save, yaml_file, sort_keys=False)