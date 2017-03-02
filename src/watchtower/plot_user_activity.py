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

n_plot = 40
df = pd.read_csv('./.user_totals.csv', index_col=0)
df['perc'] = (df['perc'] * 100).replace(np.nan, 0).astype(int)
fig, ax = plt.sublots(figsize=(10, 5))
ax = df.iloc[:n_plot]['perc'].plot.bar(ax=ax)
ax.xaxis.label.set(visible=False)
ax.set_ylabel('Percent DOC commits')
plt.tight_layout()

path_content = '../../blog/content/'
path_img = os.path.join(path_content, 'images', 'users.png')
ax.figure.savefig(path_img, bbox_inches='tight')

with open(os.path.join(path_content, 'pages', 'users.md'), 'w') as ff:
    ff.write(header)
    ff.write('![](../images/users.png)')
