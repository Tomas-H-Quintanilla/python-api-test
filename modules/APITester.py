import json
from urllib.parse import quote
import requests


class APIClient:
    _instances = {}

    def __new__(cls, api_server, *args, **kwargs):
        if api_server not in cls._instances:
            cls._instances[api_server] = super().__new__(cls)
        return cls._instances[api_server]

    def __init__(self, api_server, endpoint, method="GET", headers={}):
        if not hasattr(self, 'initialized'):
            self.api_server = api_server
            self.session = requests.Session()
            self.initialized = True
        self.endpoint = endpoint
        self.url = f'{api_server}{self.endpoint}'
        self.headers = headers
        self.method = method

    @staticmethod
    def encodeData(data):
        return quote(json.dumps(data))

    def get_response(self, data=None,):
        if self.method == "GET":
            return self.session.get(self.url, json=data, headers=self.headers)
        elif self.method == "POST":
            return self.session.post(self.url, json=data, headers=self.headers)
        elif self.method == "DELETE":
            return self.session.delete(self.url, json=data, headers=self.headers)
        elif self.method == "PUT":
            return self.session.put(self.url, json=data, headers=self.headers)

    def check_status_code(self,response, expected_status_code ):
        assert response.status_code == expected_status_code, f"Expected status code {expected_status_code}, but got {response.status_code} and {response.text}"

    def check_text(self,response, expected_text=None):
        if expected_text is not None:
            assert expected_text == response.text, f"Expected text {expected_text}, but got {response.text}"

    def check(self, expected_status_code=200, expected_text=None,payload=None):
        print("Testing "+self.endpoint+"\n")

        response = self.get_response(payload)
        self.check_status_code(response,expected_status_code)     
        self.check_text(response,expected_text)    

        print("Successfully tested "+self.endpoint)
        return response

    def set_endpoint(self, endpoint):
        self.endpoint = endpoint
        self.url = f'{self.api_server}{endpoint}'
