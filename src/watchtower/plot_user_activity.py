import pandas as pd
import numpy as np
import matplotlib
matplotlib.use('agg')
import matplotlib.pyplot as plt
import os
from datetime import date


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
        color = '#f44265' if i_type == 'doc' else None
        ax.bar(ixs, i_data.values, label=i_type, color=color)
        ax.set_xticks(ixs)
        ax.set_xticklabels(i_data.index)
        plt.setp(ax.get_xticklabels(), rotation=45,
                 horizontalalignment='right', fontsize=18)
        if ylabel is not None:
            ax.set_ylabel(ylabel)
    return ax


def parse_dates(dates):
    dates = list(dates)
    for ii, iindex in enumerate(dates):
        if isinstance(iindex, str):
            dates[ii] = iindex.split(' ')[0]

    return pd.to_datetime(dates)

header = (
    "title: Users\n"
    "date: 2017-03-01\n"
    "modified: 2017-03-01\n"
    "tags: users, docathon\n"
    "category: info\n"
    "slug: users\n"
    "authors: watchtower\n"
    "summary: A page to celebrate user contributions for the docathon\n"
    "\n"
      )

# --- Load data ---
exclude = ['NelleV', 'choldgraf']  # if we want to drop admins
plot_type = 'doc'  # 'perc'
n_plot = 30
df = pd.read_csv('./.user_totals.csv', index_col=0)
df.index = parse_dates(df.index)
df.index.name = 'date'
date_min = pd.to_datetime('2017-03-06')
date_max = pd.to_datetime(date.today())

# --- Choose a date ---
df = df.query('date != "NaT"')
df = df.query('user not in @exclude')
df['is_doc'] = df['is_doc'].astype(int)
df = df.replace(np.nan, 0)
df = df.query('date >= @date_min and date <= @date_max')
all_commits = df.groupby('user').resample('D').\
    count()
doc_commits = df.groupby('user').resample('D').sum().\
    replace('NaN', 0).astype(int)

# --- Plot leaderboard ---
total_doc = doc_commits.unstack('date').sum(1).astype(int)
total_doc.name = 'doc'
total_all = all_commits.unstack('date').sum(1).astype(int)
total_all.name = 'all'
df = pd.concat([total_doc, total_all], axis=1).\
    sort_values('doc', ascending=False)

# Plotting
fig, ax = plt.subplots(figsize=(10, 5))
ax = plot_bar(df, ax, ylabel=None)
ax.set_ylim([0, 70])
format_axis(ax)
ax.legend()
ax.set_title('Commits from {:%D} to {:%D}'.format(date_min, date_max),
             fontsize=26)


path_content = '../../blog/content/'
path_img = os.path.join(path_content, 'images', 'users_all.png')
plt.tight_layout()
ax.figure.savefig(path_img, bbox_inches='tight')

# --- Plot weekly user commits ---
# Now join together the totals so that we can plot by day
all_commits = all_commits['user'].to_frame('all')
df_week = pd.merge(all_commits, doc_commits, how='outer',
                   left_index=True, right_index=True)
df_week.columns = ['all', 'doc']
days = pd.to_datetime(df_week.index.get_level_values('date')).day

# Only plot the last 5 days
n_users_weekly = 10
y_max = 20
dates_plot = [6, 7, 8, 9, 10]
ixs_plot = range(len(dates_plot))
n_dates = len(ixs_plot)
fig, axs = plt.subplots(1, n_dates, figsize=(n_dates * 5, 5), sharey=True)
for ii, (ax, idate) in enumerate(zip(axs, dates_plot)):
    mask = idate == days
    this_date = pd.to_datetime('2017-03-{:02}'.format(idate))
    this_day = df_week.loc[mask].reset_index('date', drop=True)
    ax.set_title('Commits for {:%a}'.format(this_date), fontsize=22)
    if len(this_day) == 0:
        # Skip if we have no commits yet
        ax.set_axis_off()
        continue
    this_day = this_day.sort_values('doc', ascending=False)
    this_day = this_day.iloc[:n_users_weekly]
    ixs = range(this_day.shape[0])
    for col in this_day.columns:
        color = '#f44265' if col == 'doc' else None
        ax.bar(ixs, this_day[col].values, color=color)
        ax.set_xticks(ixs)
        ax.set_xticklabels(this_day.index, rotation=45,
                           horizontalalignment='right', fontsize=18)
    format_axis(ax)

path_img = os.path.join(path_content, 'images', 'users_week.png')
fig.savefig(path_img, bbox_inches='tight')

img_text = "<img src='../images/{img_name}' class='docathon_image' alt='{img_name}' />\n"
with open(os.path.join(path_content, 'pages', 'users.md'), 'w') as ff:
    ff.write(header)
    ff.write(img_text.format(img_name='users_all.png'))

    ff.write('\n# Daily totals\n---\n')
    ff.write(img_text.format(img_name='users_week.png'))
print('Finished plotting user activity...')
