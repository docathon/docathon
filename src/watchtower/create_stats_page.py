from datetime import date
import os
import os.path as op
import pandas as pd
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt

# Now create one page for all the projects
header_index = (
    "Title: Stats\n"
    "Date: 2017-02-18\n"
    "Modified: {now}\n"
    "Tags: projects, users, docathon\n"
    "Category: info\n"
    "Slug: stats\n"
    "Authors: watchtower\n"
    "Summary: Activity during the docathon\n"
    "\n"
    "# Statistics\n"
    "\n "
    "Check out what's been going on in the world of documentation over the "
    "last few days. Click an image to see a breakdown of detailed activity \n"
    "\n")

now = date.today()
filename = os.path.join('build', "stats.md")
img_template = "<a href='{url}'><img src='{img_source}' style='width: 80%; box-shadow: none; margin: auto' /></a>\n"
with open(filename, 'w') as ff:
    ff.write(header_index.format(now=now))
    ff.write('# Projects\n')
    ff.write(img_template.format(url='projects/projects.html', img_source='../../images/project_summary.png'))
    ff.write('# Users\n')
    ff.write(img_template.format(url='users.html', img_source='../../images/users_all.png'))
