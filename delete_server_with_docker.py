import os
import sys
import requests

repo = "mcp-memgraph"
owner = "spacegoatai"
branch = "improve-configuration"
file_path = "server_with_docker.py"
token = os.environ.get("GITHUB_TOKEN")

# Get file SHA
url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}?ref={branch}"
headers = {"Authorization": f"token {token}"}
response = requests.get(url, headers=headers)
file_data = response.json()
sha = file_data["sha"]

# Delete file
delete_url = f"https://api.github.com/repos/{owner}/{repo}/contents/{file_path}"
data = {
    "message": "Remove server_with_docker.py as it doesn't align with intended architecture",
    "sha": sha,
    "branch": branch
}
response = requests.delete(delete_url, json=data, headers=headers)
if response.status_code == 200:
    print(f"Successfully deleted {file_path}")
else:
    print(f"Error deleting file: {response.text}")
