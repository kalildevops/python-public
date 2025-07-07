import requests
import json
import os
import base64

# Azure DevOps org URL
org_url = "https://dev.azure.com/my-org"
project_name = "project1"
api_version = "7.0"

# Personal Access Token (PAT) from ADO Library
pat = os.getenv('ADO-PAT')

# Base64 encode the PAT for authorization
encoded_pat = base64.b64encode(f":{pat}".encode()).decode()

# Headers for API requests
headers = {
  'Content-Type': 'application/json',
  'Authorization': f'Basic {encoded_pat}'
}

# Repository details
repo_id = "xxxxxxxxxxxxxxxx"
yaml_path = os.getenv('YAML_PATH')

# Pipeline configuration
pipeline_name = os.getenv('APP_NAME')
pipeline_folder = os.getenv('PIPELINE_FOLDER')

# Create the pipeline definition
pipeline_definition = {
  "name": pipeline_name,
  "folder": pipeline_folder,
  "configuration": {
    "type": "yaml",
    "path": yaml_path,
    "repository": {
      "id": repo_id,
      "name": project_name,
      "type": "azureReposGit"
    }
  }
}

# Create pipeline
url = f"{org_url}/{project_name}/_apis/pipelines?api-version={api_version}"
response = requests.post(url, headers=headers, data=json.dumps(pipeline_definition))

if response.status_code == 201 or response.status_code == 200:
  print(f"Pipeline '{pipeline_name}' created successfully in folder '{pipeline_folder}'.")
else:
  print(f"Failed to create pipeline. Status code: {response.status_code}")
