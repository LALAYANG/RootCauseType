import pandas as pd
import requests
import os,json

GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
HEADERS = {
    "Authorization": f"token {GITHUB_TOKEN}",
    "Accept": "application/vnd.github.v3+json"
}

def extract_owner_repo_from_url(url):
    parts = url.split('/')
    owner, repo = parts[3], parts[4]
    return owner, repo

def get_issue_description(issue_url):
    owner, repo = extract_owner_repo_from_url(issue_url)
    issue_number = issue_url.rstrip('/').split('/')[-1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}/issues/{issue_number}"
    response = requests.get(api_url, headers=HEADERS)
    response.raise_for_status()
    return response.json().get("body", "")

def get_pr_files_changed(pr_url):
    owner, repo = extract_owner_repo_from_url(pr_url)
    pr_number = pr_url.rstrip('/').split('/')[-1]
    api_url = f"https://api.github.com/repos/{owner}/{repo}/pulls/{pr_number}/files"
    response = requests.get(api_url, headers=HEADERS)
    response.raise_for_status()
    
    files_data = []
    for file in response.json():
        files_data.append({
            "filename": file["filename"],
            "status": file["status"],  # modified / added / removed
            "patch": file.get("patch", "")  # unified diff for the file
        })
    return files_data

def process_csv(file_path, output_dir="info_json"):
    df = pd.read_csv(file_path)
    os.makedirs(output_dir, exist_ok=True)

    for _, row in df.iterrows():
        issue_id = row['id']
        print(f"Processing ID {issue_id}: {row['repo_name']}")

        result = {
            "id": issue_id,
            "repo": row['repo_name'],
            "issue_url": row['issue_url'],
            "pr_url": row['linked_pr_url'],
            "issue_description": None,
            "files_changed": [],
            "fix_category": row.get('fix_category', None),
            "root_cause_category": row.get('root_cause_category', None),
            "root_cause_subcategory": row.get('root_cause_subcategory', None)
        }

        try:
            result["issue_description"] = get_issue_description(row['issue_url'])
        except Exception as e:
            print(f"[!] Failed to fetch issue description: {e}")

        try:
            result["files_changed"] = get_pr_files_changed(row['linked_pr_url'])
        except Exception as e:
            print(f"[!] Failed to fetch PR files: {e}")

        output_path = os.path.join(output_dir, f"{issue_id}.json")
        with open(output_path, "w") as f:
            json.dump(result, f, indent=2)
        print(f"✓ Saved to {output_path}")

if __name__ == "__main__":
    process_csv("RustFlakyTest/issues-ftw25-artifact.csv")