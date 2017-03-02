import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import os

header = (
    "title: User Leaderboard\n"
    "date: 2017-03-01\n"
    "modified: 2017-03-01\n"
    "tags: users, docathon\n"
    "category: info\n"
    "slug: users\n"
    "authors: watchtower\n"
    "summary: A page to celebrate user contributions for the docathon\n"
    "status: hidden\n"
    "\n"
    "# User contributions\n\n"
      )

# Load data and drop admins
exclude = ['Carreau', 'NelleV', 'choldgraf']
plot_type = 'doc'  # 'perc'
n_plot = 30
df = pd.read_csv('./.user_totals.csv', index_col=0)
df = df.query('user not in @exclude')
df = df.sort_values(plot_type, ascending=False)

# Pull the values we want
if plot_type == 'perc':
    df[plot_type] = df[plot_type] * 100
    ylabel = 'Percent DOC commits'
else:
    ylabel = 'Number commits'
df = df.replace(np.nan, 0).astype(int)

# Make plot
fig, ax = plt.subplots(figsize=(10, 5))
i_types = [plot_type] if plot_type == 'perc' else ['all', 'doc']
for i_type in i_types:
    fillcolor = 'w' if i_type == 'all' else 'C1'
    edgecolor = 'k'
    i_data = df.iloc[:n_plot][i_type]
    ixs = range(i_data.shape[0])
    ax.bar(ixs, i_data.values, color=fillcolor,
           edgecolor=edgecolor, label=i_type)
    plt.xticks(ixs, i_data.index)
    plt.setp(ax.get_xticklabels(), rotation=45,
             horizontalalignment='right', fontsize=14)
if plot_type != 'perc':
    ax.legend()
    ax.set_ylim([0, 25])

# Formatting
plt.setp([ax.spines[ii] for ii in ['top', 'right']], visible=False)
ax.grid("off")
yticks = ax.get_yticks()
for l in yticks:
    ax.axhline(l, linewidth=0.75, zorder=-10, color="0.5")
ax.set_yticks(yticks)

ax.xaxis.label.set(visible=False)
ax.set_ylabel(ylabel)
plt.tight_layout()

path_content = '../../blog/content/'
path_img = os.path.join(path_content, 'images', 'users.png')
ax.figure.savefig(path_img, bbox_inches='tight')

with open(os.path.join(path_content, 'pages', 'users.md'), 'w') as ff:
    ff.write(header)
    ff.write('![](../images/users.png)')
