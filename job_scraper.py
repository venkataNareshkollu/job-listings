import requests
from bs4 import BeautifulSoup
import json
import base64

# Step 1: Scrape the mock job board
url = "file:///workspaces/job-listings/mock_job_board.html"  # Path to the mock job board
response = requests.get(url)
soup = BeautifulSoup(response.text, 'html.parser')

# Extract job listings
jobs = []
for job in soup.find_all('div', class_='job-listing'):
    title = job.find('h3').text
    company = job.find('p', text=lambda x: 'Company:' in x).text.replace('Company: ', '')
    location = job.find('p', text=lambda x: 'Location:' in x).text.replace('Location: ', '')
    experience = job.find('p', text=lambda x: 'Experience:' in x).text.replace('Experience: ', '')
    link = job.find('a')['href']
    jobs.append({
        'Title': title,
        'Company': company,
        'Location': location,
        'Experience': experience,
        'Link': link
    })

# Step 2: Filter jobs based on user input
def filter_jobs(jobs, title_filter, experience_filter):
    filtered_jobs = []
    for job in jobs:
        if title_filter.lower() in job['Title'].lower() and experience_filter in job['Experience']:
            filtered_jobs.append(job)
    return filtered_jobs

# User input (you can replace this with input() for dynamic filtering)
title_filter = "Python"
experience_filter = "2-5 years"
filtered_jobs = filter_jobs(jobs, title_filter, experience_filter)

# Step 3: Save filtered jobs to a JSON file
with open("jobs.json", "w") as file:
    json.dump(filtered_jobs, file, indent=4)
print("Filtered jobs saved to jobs.json!")

# Step 4: Push the file to GitHub
def push_to_github(file_path, repo_name, branch_name, github_token):
    # Read the file content
    with open(file_path, "rb") as file:
        file_content = file.read()
    file_content_base64 = base64.b64encode(file_content).decode("utf-8")

    # GitHub API URL
    url = f"https://api.github.com/repos/{repo_name}/contents/{file_path}"

    # Check if the file already exists
    headers = {
        "Authorization": f"token {github_token}",
        "Accept": "application/vnd.github.v3+json"
    }
    response = requests.get(url, headers=headers)
    sha = None
    if response.status_code == 200:
        sha = response.json()["sha"]

    # Create or update the file
    data = {
        "message": "Update job listings",
        "content": file_content_base64,
        "branch": branch_name,
        "sha": sha
    }
    response = requests.put(url, headers=headers, json=data)

    if response.status_code in [200, 201]:
        print("File successfully pushed to GitHub!")
    else:
        print("Failed to push file to GitHub:", response.json())

# Replace these with your details
github_token = "your_personal_access_token"  # Replace with your GitHub token
repo_name = "your_github_username/your_repo_name"  # Replace with your repo name
branch_name = "main"  # Replace with your branch name
file_path = "jobs.json"

# Push the file to GitHub
push_to_github(file_path, repo_name, branch_name, github_token)
