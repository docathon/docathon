import argparse
from datetime import date
import os
import os.path as op
import pandas as pd


parser = argparse.ArgumentParser()
parser.add_argument("filename",
                    help=("CSV file containing the project "
                          "registration information."))
parser.add_argument("--outdir", "-o", default="build")
args = parser.parse_args()

columns = ["timestamp", "username", "name", "contact", "github_org",
           "description", "language", "url", "goal", "help",
           "has_github_project",
           "github_project_url"]
information = pd.read_csv(args.filename, header=None, skiprows=1,
                          names=columns)

header = (
    "title: {project_name}\n"
    "date: {registration_date}\n"
    "modified: {now}\n"
    "tags: projects, docathon\n"
    "category: info\n"
    "slug: projects/{target}\n"
    "authors: watchtower\n"
    "summary: {project_name}\n"
    "status: hidden\n"
    "\n"
    "# {project_name}\n"
      )

try:
    os.makedirs(args.outdir)
except OSError:
    pass

print('Creating pages for {} projects'.format(len(information)))
projects = {}
for ix, project in information.iterrows():
    project_url = project['url']

    # Try to be clever about pulling project information
    project_info = project['github_org'].split('/')[-2:]
    if len(project_info) == 2:
        project_user, project_name = project_info
    else:
        project_user = project_info[0]
        project_name = project['name']
    project_description = project['description']
    project_name_lc = project_name.lower().replace(" ", "_")
    filename = os.path.join(args.outdir, project_name_lc.replace(" ", "_")
                            + ".md")
    header_formatted = header.format(
        project_name=project_name,
        registration_date=project['timestamp'],
        target=project_name_lc.replace(" ", "_").lower(),
        now=date.today().strftime("%Y-%m-%d"),
        project_description=project_description)

    projects[project_name] = project_name_lc.replace(" ", "_")

    # Write the content page
    with open(filename, "w") as f:
        f.write(header_formatted)
        if isinstance(project_url, str):
            f.write(
                "* **Documentation** [{project_url}]({project_url})\n".format(
                    project_url=project_url))
        if isinstance(project['github_org'], str):
            if project["github_org"].startswith("http"):
                github_org = project["github_org"]
            elif len(project["github_org"].split("/")) == 2:
                github_org = (
                    "https://github.org/%s/%s" %
                    (project["github_org"].split("/")[0],
                    project["github_org"].split("/")[1]))
            else:
                github_org = None

            if github_org is not None:
                f.write(
                    "* **Github organization** [{github_org}]({github_org})\n".format(
                        github_org=github_org))
        if isinstance(project["github_project_url"], str):
            if len(project["github_project_url"].split(" ")) == 1:
                f.write(
                    "* **Docathon project** "
                    "[{github_project_org}]({github_project_org})\n".format(
                        github_project_org=project["github_project_url"]))
        f.write(
            "* **Description** {project_description}\n".format(
                project_description=project_description))


    # Compile list of which projects we've pulled
    open_as = 'w' if ix == 0 else 'a'
    with open('.downloaded_projects', open_as) as ff:
        ff.writelines('{},{}\n'.format(project_user, project_name))