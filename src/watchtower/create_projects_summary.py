from datetime import date
import os
import os.path as op
import pandas as pd
import matplotlib
import numpy as np
matplotlib.use('agg')
import matplotlib.pyplot as plt


def format_axis(ax):
    # Formatting
    plt.setp([ax.spines[ii] for ii in ['top', 'right']], visible=False)
    ax.grid("off")
    yticks = ax.get_yticks()
    for l in yticks:
        ax.axhline(l, linewidth=0.75, zorder=-10, color="0.5")
    ax.set_yticks(yticks)

    ax.xaxis.label.set(visible=False)
    plt.tight_layout()


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
count_since = pd.to_datetime('2017-02-25')
now = pd.to_datetime(date.today())

proj_info = pd.read_csv('.project_info.csv')
proj_info['name'] = proj_info['name'].str.lower()
proj_info = proj_info.sort_values('name')

commit_totals = pd.read_csv('.project_totals.csv', index_col=0, parse_dates=True)
sorted_totals = commit_totals.query('date > @count_since')
sorted_totals = sorted_totals.groupby('project').sum().sort_values('doc', ascending=False)

# Create leaderboard PNG
n_plot = 20
fig, ax = plt.subplots(figsize=(10, 5))
for column in sorted_totals.columns:
    ixs = range(n_plot)
    projects_plot = sorted_totals.index[:n_plot]
    ax.bar(ixs, sorted_totals.iloc[:n_plot][column], label=column)

ax.set_xticks(ixs)
ax.set_xticklabels(projects_plot)
ax.set_ylim([None, 50])
plt.setp(ax.get_xticklabels(), rotation=45,
         horizontalalignment='right', fontsize=16)
format_axis(ax)
ax.legend()
ax.set_title('Commits from {:%D} to {:%D}'.format(count_since, now), fontsize=26)
fig.savefig('../../blog/content/images/project_summary.png', bbox_inches='tight')

# Create a summary page
filename = os.path.join('build', "projects.md")
header_formatted = header_index.format(now=date.today().strftime("%Y-%m-%d"))
project_template = "<a href='{project_url}'><img src='{project_image}' alt='{project_image}' style='width: 48%; float:left; box-shadow: none; margin: auto' /></a>"
with open(filename, "w") as f:
    f.write(header_formatted)
    f.write('Docathon projects\n---\n')
    repos_names = []
    for ix, row in proj_info.iterrows():
        if isinstance(row['github_org'], str):
            org, repo = row['github_org'].split('/')[-2:]
            name = row['name']
            repos_names.append((name, org, repo))
    repos_names = np.array(repos_names)
    ixs_split = np.arange(len(repos_names))[::4][1:-1]
    repos_names = np.split(repos_names, ixs_split)
    for group in repos_names:
        f.write('&nbsp;&nbsp;-&nbsp;&nbsp;'.join(
            ['[{name}]({repo}.html)'.format(name=name, repo=repo.lower())
             for name, org, repo in group]) + '<br />')
    f.write('\n')
    f.write('# Project leaders\n')
    f.write("<img src='../../images/project_summary.png' alt='project_summary' style='box-shadow: none; margin: auto' />\n")
    f.write('# Project contributions\n')
    for project_name in sorted_totals.index:
        path_img_read = 'build/images/{}.png'.format(project_name)
        if not op.exists(path_img_read):
            print('Skipping {}'.format(project_name))
            continue
        path_img_write = 'images/{}.png'.format(project_name)
        project_image = path_img_write
        f.write(project_template.format(project_image=project_image,
                project_url=project_name.lower()+".html"))
print('Finished creating projects summary...')
