import yaml
import argparse
from modules.VariableTreating import increment_test_variables, replace_within_vars, load_workflow_file, load_variables_from_files, load_servers_file, load_endpoints_files
from modules.VariableTreating import save_variables_in_files, load_file_data
from modules.EndpointExecution import execute_endpoints
import copy
import os

def main():
    parser = argparse.ArgumentParser(
        description='Process the file for the test execution.')

    parser.add_argument('-f', '--filename', type=str,
                        help='File name of the execution configuration file.')

    args = parser.parse_args()

    if not args.filename:
        print('No configuration file specified.')
        exit(500)

    test_data = load_file_data(args.filename)
    test_data['name'] = os.path.dirname(args.filename)

    if 'variables' not in test_data:
        test_data['variables'] = {}

    data_save = None

    load_variables_from_files(test_data)
    increment_test_variables(test_data)
    data_save = (copy.deepcopy(test_data))

    load_servers_file(test_data)
    load_endpoints_files(test_data)

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
        elif data_save is not None:
            save_variables_in_files(data_save)

if __name__ == "__main__":
    main()
