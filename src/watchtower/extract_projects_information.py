import pandas as pd
import numpy as np
import argparse
from watchtower import GithubDatabase
from tqdm import tqdm


parser = argparse.ArgumentParser()
parser.add_argument("filename",
                    help=("CSV file containing the project "
                          "registration information."))
args = parser.parse_args()


def validate_url(url):
    if isinstance(url, str):
        if 'http' not in url:
            url = 'http://' + url
    else:
        url = 'http://docathon.github.io/docathon'
    return url

projects = pd.read_csv(args.filename)

rename = {'Documentation URL': 'url', 'Name of the project': 'name',
          'If yes, can you provide the Github url?': 'url_doc',
          'Github organization and project (if applicable)': 'github_org',
          'Description': 'description',
          'Timestamp': 'date',
          'is_github': 'is_github',
          'Would you like any help from others in improving documentation?': 'wants_help',
          'branch': 'branch', 'words': 'words'}
projects = projects.rename(columns=rename)
projects = projects[list(rename.values())]
projects['url'] = projects['url'].apply(validate_url)


def is_doc(row):
    doc_words = ['doc', 'documentation', 'docathon']
    is_doc = 0
    for word in doc_words:
        if word in row['title']:
            is_doc += 1
        if word in row['label_names']:
            is_doc += 1
    return is_doc > 0

projects['doc_issues'] = None
db = GithubDatabase()
for ix, project in tqdm(projects.iterrows()):
    if not isinstance(project['github_org'], str):
        continue
    org, repo = project['github_org'].split('/')[-2:]
    proj = db.load(org, repo)
    if proj.issues is None:
        continue
    issues = proj.issues.query('state == "open"')
    issues = issues[pd.isnull(issues['pull_request'])]
    if len(issues) == 0:
        print('{}: No open issues w/o a PR'.format(repo))
        continue
    issues['is_doc'] = issues.apply(is_doc, axis=1)
    doc_issues = [{'url': issue['html_url'],
                   'title': issue['title']}
                  for ix, issue in issues.iterrows()
                  if issue['is_doc'] is True]
    doc_issues = None if len(doc_issues) is 0 else doc_issues
    projects.loc[ix, 'doc_issues'] = doc_issues


projects = projects.replace({'doc_issues': {np.nan: None}})
projects.to_csv('.project_info.csv')
