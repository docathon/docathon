from datetime import date
import argparse
import os
import pandas as pd
import numpy as np

header = (
    "title: {repo}\n"
    "date: {registration_date}\n"
    "modified: {now}\n"
    "tags: projects, docathon\n"
    "category: info\n"
    "slug: projects/{repo}\n"
    "authors: watchtower\n"
    "summary: {repo}\n"
    "status: hidden\n"
    "\n"
    "# {repo}\n\n"
      )

parser = argparse.ArgumentParser()
parser.add_argument("--outdir", "-o", default="build")
args = parser.parse_args()
projects = pd.read_csv('.project_info.csv')
now = date.today().strftime("%Y-%m-%d")

try:
    os.makedirs(args.outdir)
except OSError:
    pass

print('Creating pages for {} projects'.format(len(projects)))
for ix, project in projects.iterrows():
    # Pull information about the project
    if not isinstance(project['github_org'], str):
        # Skip if we don't have an org / repo
        continue
    user, repo = project['github_org'].split('/')[-2:]
    description = project['description']
    url = project['url']
    timestamp = project['date']
    url_doc = project['url_doc']
    is_github = project['is_github']

    project_name = project['name']
    project_name_lc = project_name.lower().replace(" ", "_")
    filename = os.path.join(args.outdir, '{}.md'.format(repo))

    # Find doc issues
    doc_issues = project['doc_issues']
    doc_issues = None if isinstance(doc_issues, float) else eval(doc_issues)

    # Prep header and write
    header_formatted = header.format(
        repo=repo,
        registration_date=timestamp,
        now=now,
        description=description)

    with open(filename, "w") as ff:
        ff.write(header_formatted)
        ff.write('## Information\n\n')
        if isinstance(url, str):
            ff.write(
                "* **Documentation**: [{url}]({url})\n".format(
                    url=url))
        if is_github == 'yes':
            url_org = 'http://github.org/{}/{}'.format(
                user, repo)
            ff.write(
                "* **Github organization**: [{url_org}]({url_org})\n".format(
                    url_org=url_org))

        if isinstance(url_doc, str) and len(url_doc) > 0:
            ff.write(
                "* **Docathon project**: "
                "[{url_doc}]({url_doc})\n\n".format(
                    url_doc=url_doc))

        ff.write(
            "## Description\n{description}\n\n".format(
                description=description))

        if isinstance(doc_issues, list):
            ff.write(
                "## Open Doc issues\n\n"
                )
            for issue in doc_issues:
                ff.write(
                    "* [{title_issue}]({url_issue})\n".format(
                        title_issue=issue['title'], url_issue=issue['url']))
