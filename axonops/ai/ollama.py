import requests
import json
import ast

url = "http://localhost:11434/api/generate"
headers = {"Content-Type": "application/json"}
data = {
    "model": "llama3:8b",
    "prompt": "What is AxonOps for Cassandra?",
    "stream": False  # Disable streaming
}

response = requests.post(url, headers=headers, data=json.dumps(data))
if response.status_code == 200:
    # Convert the string to a dictionary
    data = ast.literal_eval(str(response.json()))
    # Extract the 'response' field
    answer = data['response']

    print(f"answer: {answer}")
else:
    print(f"Error: {response.status_code}")