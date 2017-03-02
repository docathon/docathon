import pandas as pd
import numpy as np
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

df = pd.read_csv('./.user_totals.csv', index_col=0)
df['perc'] = (df['perc'] * 100).replace(np.nan, 0).astype(int)
ax = df.iloc[:20]['perc'].plot.bar()
ax.xaxis.label.set(visible=False)
ax.set_ylabel('Percent DOC commits')
plt.tight_layout()

path_content = '../../blog/content/'
path_img = os.path.join(path_content, 'images', 'users.png')
ax.figure.savefig(path_img, bbox_inches='tight')

with open(os.path.join(path_content, 'pages', 'users.md'), 'w') as ff:
    ff.write(header)
    ff.write('![](../images/users.png)')
