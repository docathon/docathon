import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import os


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


def plot_bar(df, ax, ylabel='Number commits'):
    # Make plot for totals
    for i_type in ['all', 'doc']:
        i_data = df.iloc[:n_plot][i_type]
        ixs = range(i_data.shape[0])
        ax.bar(ixs, i_data.values, label=i_type)
        ax.set_xticks(ixs)
        ax.set_xticklabels(i_data.index)
        plt.setp(ax.get_xticklabels(), rotation=45,
                 horizontalalignment='right', fontsize=14)
        if ylabel is not None:
            ax.set_ylabel(ylabel)
    return ax


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
      )

# Load data and drop admins
exclude = ['Carreau', 'NelleV', 'choldgraf']
plot_type = 'doc'  # 'perc'
n_plot = 30
df = pd.read_csv('./.user_totals.csv', index_col=0)
df.index = pd.to_datetime(df.index)
date_min = np.min(df.index)
date_max = np.max(df.index)
df = df.query('date != "NaT"')
df = df.query('user not in @exclude')
df['is_doc'] = df['is_doc'].astype(int)
df = df.replace(np.nan, 0)
all_commits = df.groupby('user').resample('D').\
    count()
doc_commits = df.groupby('user').resample('D').sum().\
    replace('NaN', 0).astype(int)

total_doc = doc_commits.unstack('date').sum(1).astype(int)
total_doc.name = 'doc'
total_all = all_commits.unstack('date').sum(1).astype(int)
total_all.name = 'all'
df = pd.concat([total_doc, total_all], axis=1).\
    sort_values('doc', ascending=False)

# Now join together the totals so that we can plot by day
all_commits = all_commits['user'].to_frame('all')
df_week = pd.merge(all_commits, doc_commits, how='outer',
                   left_index=True, right_index=True)
df_week.columns = ['all', 'doc']

# Plotting
fig, ax = plt.subplots(figsize=(10, 5))
ax = plot_bar(df, ax, ylabel=None)
ax.set_ylim([0, 30])
format_axis(ax)
ax.legend()
ax.set_title('Commits from {:%D} to {:%D}'.format(date_min, date_max),
             fontsize=26)


path_content = '../../blog/content/'
path_img = os.path.join(path_content, 'images', 'users_all.png')
plt.tight_layout()
ax.figure.savefig(path_img, bbox_inches='tight')

# Plot weekly user commits
n_users_weekly = 10
grp_date = df_week.groupby(level='date')
n_dates = len(grp_date)
fig, axs = plt.subplots(1, n_dates, figsize=(n_dates * 5, 5))
for ax, (date, values) in zip(axs, grp_date):
    values = values.reset_index('date', drop=True)
    values = values.sort_values('doc', ascending=False)
    values = values.iloc[:n_users_weekly]
    if len(values) != 0:
        ax = plot_bar(values, ax)
        ax.set_ylim([0, 20])
    format_axis(ax)
    ax.set_title('{:%a (%b %d)}'.format(date))

path_img = os.path.join(path_content, 'images', 'users_week.png')
fig.savefig(path_img, bbox_inches='tight')

img_text = "<img src='../images/{img_name}' style='box-shadow: none; margin: auto' />\n"
with open(os.path.join(path_content, 'pages', 'users.md'), 'w') as ff:
    ff.write(header)
    ff.write(img_text.format(img_name='users_all.png'))

    ff.write('\n# Daily totals\n---\n')
    ff.write(img_text.format(img_name='users_week.png'))
print('Finished plotting user activity...')
