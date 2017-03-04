import pandas as pd
import requests
import numpy as np

# Load project registration data
data = pd.read_csv('../data/docathon_project_registration.csv')

# List the project info
data = data.sort_values('Name of the project')
s = []
for ix, row in data.iterrows():
    name = row['Name of the project']
    github_org = row['Github organization and project (if applicable)']
    if not isinstance(github_org, str):
        continue
    org, repo = github_org.split('/')[-2:]
    repo = repo.lower()
    s.append('* [{}](projects/{}.html)\n'.format(name, repo))

# Read current lines
with open('../../blog/content/pages/participate.md', 'r') as ff:
    lines = ff.readlines()

# Remove everything between `---`
ixs = [ii for ii, ln in enumerate(lines) if '---' in ln]
for ix in range(ixs[0] + 1, ixs[1])[::-1]:
    lines.pop(ix)

# Insert new projects
for project in s:
    lines.insert(ixs[0] + 1, project)

# Write the file
with open('../../blog/content/pages/participate.md', 'w') as ff:
    ff.writelines(lines)
