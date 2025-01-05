import json  # Importing JSON module for handling JSON data
import time  # Importing time module for handling time-related tasks
import requests  # Importing requests module for making HTTP requests

class Text2ImageAPI:
    def __init__(self, url, api_key, secret_key):
        # Initialize the API with the URL and authentication headers
        self.URL = url
        self.AUTH_HEADERS = {
            'X-Key': f'Key {api_key}',  # API key for authentication
            'X-Secret': f'Secret {secret_key}',  # Secret key for authentication
        }

    def get_model(self):
        # Make a GET request to retrieve available models
        response = requests.get(self.URL + 'key/api/v1/models', headers=self.AUTH_HEADERS)
        data = response.json()  # Parse the JSON response
        return data[0]['id']  # Return the ID of the first model

    def generate(self, prompt, model, width=1024, height=1024):
        # Prepare parameters for the image generation request
        params = {
            "type": "GENERATE",
            "numImages": 1,  # Number of images to generate
            "width": width,  # Width of the generated images
            "height": height,  # Height of the generated images
            "generateParams": {
                "query": f"{prompt}"  # Text prompt for generating images
            }
        }

        # Prepare data for the POST request
        data = {
            'model_id': (None, model),  # Model ID to use for generation
            'params': (None, json.dumps(params), 'application/json')  # Parameters in JSON format
        }
        response = requests.post(self.URL + 'key/api/v1/text2image/run', headers=self.AUTH_HEADERS, files=data)
        data = response.json()
        return data['uuid']

    def check_generation(self, request_id, attempts=10, delay=10):
        while attempts > 0:
            response = requests.get(self.URL + 'key/api/v1/text2image/status/' + request_id, headers=self.AUTH_HEADERS)
            data = response.json()
            if data['status'] == 'DONE':
                return data['images']

            attempts -= 1
            time.sleep(delay)

