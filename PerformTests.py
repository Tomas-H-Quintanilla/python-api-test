import yaml
import argparse
import json
from collections import OrderedDict
from modules.VariableTreating import increment_test_variables
from modules.EndpointExecution import execute_endpoints


parser = argparse.ArgumentParser(
    description='Process the file for the test execution.')

parser.add_argument('-f', '--filename', type=str,
                    help='File name of the execution configuration file.')

args = parser.parse_args()

if not args.filename:
    print('No configuration file specified.')
    exit(500)

test_data = None
# Open the YAML file
with open(args.filename, "r") as yaml_file:
    # Load the YAML data
    test_data = yaml.safe_load(yaml_file)
    increment_test_variables(test_data)

execute_endpoints(test_data)

