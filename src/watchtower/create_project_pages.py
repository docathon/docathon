from datetime import date
import argparse
import os
import pandas as pd

header = (
    "title: {repo}\n"
    "date: {registration_date}\n"
    "modified: {now}\n"
    "tags: projects, docathon\n"
    "category: info\n"
    "slug: projects/{target}\n"
    "authors: watchtower\n"
    "summary: {repo}\n"
    "status: hidden\n"
    "\n"
    "# {repo}\n"
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
    filename = os.path.join(args.outdir, '{}.md'.format(project_name_lc))

    # Prep header and write
    header_formatted = header.format(
        repo=repo,
        registration_date=timestamp,
        target=project_name_lc,
        now=now,
        description=description)

    with open(filename, "w") as ff:
        ff.write(header_formatted)
        if isinstance(url, str):
            ff.write(
                "* **Documentation**:  [{url}]({url})\n".format(
                    url=url))
        if is_github:
            url_org = 'http://github.org/{}/{}'.format(
                user, repo)
            ff.write(
                "* **Github organization**: [{url_org}]({url_org})\n".format(
                    url_org=url_org))

        if isinstance(url_doc, str) and len(url_doc) > 0:
            ff.write(
                "* **Docathon project**: "
                "[{url_doc}]({url_doc})\n".format(
                    url_doc=url_doc))
        ff.write(
            "* **Description**: {description}\n".format(
                description=description))
