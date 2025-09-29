import requests
import re
import os
from dotenv import load_dotenv

load_dotenv()

def check_pr_conflicts(repo_url, token):
    match = re.match(r"https?://github.com/([^/]+)/([^/]+)", repo_url)
    if not match:
        raise ValueError("Invalid GitHub repository URL.")
    owner = match.group(1)
    repo = match.group(2)

    pr_num_url= f"https://api.github.com/repos/{owner}/{repo}/pulls?sort=created&direction=desc&per_page=1"
    headers = {
        "Authorization": f"token {token}",
        "Accept": "application/vnd.github+json"
    }
    pr_num_response = requests.get(pr_num_url, headers=headers)

    if pr_num_response.status_code != 200:
        raise Exception(f"Failed to fetch PR number: {pr_num_response.status_code} {pr_num_response.text}")
    
    pr_list = pr_num_response.json()
    if not pr_list:
        return "No PR Requests"
    pr_num= pr_list[0].get("number")
    conflict_status_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_num}"
    conflict_status_response = requests.get(conflict_status_url, headers=headers)
    pr_metadata = conflict_status_response.json()
    mergeable = pr_metadata.get("mergeable")
    
    if mergeable is None:
        return "Try again, status of conflict pending!"  
    return "Conflict" if not mergeable else "No Conflict"

    
if __name__ == "__main__":
    token = os.getenv("GITHUB_TOKEN")
    repo_url = "https://github.com/aarav-sahni/test"

    conflict = check_pr_conflicts(repo_url, token)
    print(conflict)
