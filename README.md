# Python API Test

A simplified framework to perform Python API tests. The user defines a simple `.yaml` or `.json` file in order to define which endpoints to test, in which order and with which configurations and payloads shall them be executed. 

## Use

In order to use it the user needs to define a file with the test execution plan. The file has multiple options available and configuration settings that must be taken into account, in the example directory an example file with all the available options to be used can be found.

### Configuration Options

Below you can find an example of a configuration file to execute a set of tests against 6 different endpoints, each one with their unique configuration settings:

```yaml 
variables: 
  UserId:
    type: int
    value: 1
  PostCount:
    type: int
    increment: 10
    value: 1
  PostTitle:
    type: string
    value: foo$PostCount$
variables_files: [comments.yaml]
workflow_file: execute_only_get_all.yaml
workflow:
  type: skip
  endpoints: [all_posts]
servers:
    api_server: https://jsonplaceholder.typicode.com/
servers_file: main.json
endpoints_files: [user.yaml]
endpoints:
  all_posts:
    url: /posts
    method: GET
    server: api_server
    result:
      name: PostId
      keys:
      - 0
      - id
  get_single_post:
    url: /posts/$PostId$
    method: GET
    server: api_server
  create_post:
    url: /posts
    method: POST
    server: api_server
    expected_code: 201
    payload:
    - postId: $PostId$
    - name: bar
    - userId: $UserId$
  create_comment:
    url: /comments
    method: POST
    server: api_server
    expected_code: 201
    payload_file: create_comment.json
  delete_comment:
    url: /comments/1
    execute: true
    method: DELETE  
    server: api_server
  todos:
      url_file: todos.json
      execute: false
      method: GET
      server: api_server
```

### Directory naming and mapping

The configuration file should be place inside a directory **named after the directory of the file**. In the above example this would be a directory named `example`.
It is recommended that the directory contains 3 subdirectories for using all the options available for a test file, which are:

- **data**: Can be used to store the payloads of the endpoints to be used in the tests.
- **variables**: Can be used to store the variables that the tests are going to use in the payloads or URLs of the endpoints.
- **workflows**: The testing tool allow the use of workflow files for defining which endpoints should be executed or skipped.
- **servers**: Can be used to store the servers to be used in the tests with their corresponding names for reference.
- **endpoints**: Can be used to store the endpoints configuration to be used during the tests.

If any of the options that require a directory are used without the files being in the correct directory, the scripts will not work.

### Variables

The variables can be defined in the configuration file and in additional files in the variables directory. In order to use a variable file, it has to be specified in the `variables_files` array. Variables have to be configured in the following way:

```yaml
variables:
    NameOfTheVariable:
        type: string | int | dict | array
        value: -
        increment (optional): integer # Only for int variables
```

In case of using the increment statement, the variable will be incremented by the quantity defined and saved to the file, so in the above example, once the program is executed, 2 will be stored in the value of `PostCount`.

To use the variables in the requests a user can point to them using `$NameOfTheVariable$` as template. This will be later substitued by the variable value. In case the variable is a dictionary or an array and you want to access a certain key within it, you can do so by pointing to it using an `@` as `$NameOfTheVariable@SelectedKey$`. 

You can go as deep as you want within the dictionary, being able to concatenate multiple keys one after the other.

You can also use the output of an endpoint call to define a variable, please take a look at the [endpoints section](#Endpoints) for more information.

### Workflows

In some cases you might have defined a set of endpoints but do not want to use all of them for certain tests, that's when workflows come into play. You can define a list of endpoints that you want to `execute` or `skip` from a set of tests in the `worflow` section or define a location for a `workflow_file` with the list of endpoints to be treated differently. Below you can find an example of a  workflow that `skips all_posts` endpoint of the example file:

```yaml
workflow:
  type: skip
  endpoints: [all_posts]
```

### Servers

A set of tests may need to access multiple servers in order to check the endpoints. For this purpose, the `servers` section has been defined, where you name the different servers to be used. Below there is a sample with two different servers:

```yaml
servers:
  main_node: http://localhost:3000
  web_services: http://localhost:3003
```

You can also specify a path to a `servers_file` where you can define the servers to be used in the project, of course this file must be inside a subdirectory called `servers`

### Endpoints

This is the core part of the testing suite. The `endpoints` section defines which urls are going to be called, which payload will they need and what should be done with the output of the call. Let's look at the complete set of option available for an endpoint:

```yaml
endpoints:
  example:
    url: /example/$ExampleData@id$
    url_file: location
    method: GET | POST | PUT | DELETE ...
    server: api_server
    execute: true | false
    repeat: integer
    stop: boolean
    payload:
        - variable_name: primitive type | dictionary | array
    payload_file: location
    result:
      name: Variable
      keys:
      - 0
      - id
```

- **example**: We need to define a **unique** name for the endpoint execution, in this case `example`. 
- **url**: We define the `url` to be called, which can contain a reference to any of the variables of the test data. In case you want the same configuration for several different urls, you can define them in a file in the `urls` directory, as in the example.
- **method**: To be used for the url call.
- **server**: To which the call will be executed.
- **execute**_(optional)_: Whether the endpoint will be executed or not, it has preference over the workflow.
- **repeat**_(optional)_: How many consecutive times shall the endpoint be executed.
- **stop**_(optional)_: If is set to true, the endpoints after the one being executed will be skipped.
- **payload**_(optional)_: To be sent to the server as request body. Can also be defined as file location. It can contain any data to be sent in `yaml` or `json` format.
- **result**_(optional)_: You can use the result of the execution to set a variable. The `name` field defines its name and the `keys` field defines the keys to be accessed to set the value of the variable. We assume is a dictionary by default, but it can be anything.

You can also define the endpoints in several files with the `endpoints_files` directive, which allows you to specify multiple files to be loaded and executed.

**WARNING**

The order in which the enpoints files are defined does not have to comply with the order in which they are executed. You can only trust that the endpoints defined in the main file will be executed before any other and that the execution order within a file will be respected. We are working in this issue.

### More information

For more detail about how to create a configuration file, please refer to the example directory in this same repository.