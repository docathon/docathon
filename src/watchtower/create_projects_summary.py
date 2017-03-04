import argparse
from datetime import date
import os
import os.path as op
import pandas as pd

# Now create one page for all the projects
header_index = (
    "Title: Projects\n"
    "Date: 2017-02-18\n"
    "Modified: {now}\n"
    "Tags: projects, docathon\n"
    "Category: info\n"
    "Slug: projects/projects\n"
    "Authors: watchtower\n"
    "Summary: List of projects\n"
    "\n"
    "# Projects\n"
    "\n "
    "Here is a list of projects involved in the Docathon along "
    "with information about contributions to their documentation. If "
    "you'd like to help out with a project, click an image below "
    "to see more information about it. "
    "If you'd like to see your project here, please fill in [this "
    "registration form](https://goo.gl/forms/0cPpw01zehrEyDDE3) \n"
    "\n")


# Pull commit totals
commit_totals = pd.read_csv('.project_totals.csv', index_col=0, parse_dates=True)
sorted_totals = commit_totals.groupby('project').sum()['doc'].sort_values(ascending=False)

# Create a summary page
filename = os.path.join('build', "projects.md")
header_formatted = header_index.format(now=date.today().strftime("%Y-%m-%d"))
project_template = "<a href='{project_url}'><img src='{project_image}' style='width: 48%; float:left; box-shadow: none; margin: auto' /></a>"
with open(filename, "w") as f:
    f.write(header_formatted)
    for project_name, _ in sorted_totals.items():
        path_img_read = 'build/images/{}.png'.format(project_name)
        if not op.exists(path_img_read):
            print('Skipping {}'.format(project_name))
            continue
        path_img_write = 'images/{}.png'.format(project_name)
        project_image = path_img_write
        f.write(project_template.format(project_image=project_image,
                project_url=project_name.lower()+".html"))
print('Finished creating projects summary...')
