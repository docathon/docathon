import numpy as np
import os
import matplotlib
matplotlib.use('agg')
import matplotlib.dates as mpd
from watchtower import commits_
import matplotlib.pyplot as plt
from tqdm import tqdm
import calendar
import pandas as pd
import traceback

today = pd.datetime.today()
plot_start = '2017-02-24'
docathon_start = '2017-03-05'  # One day before/after so the color covers all days
docathon_end = '2017-03-11'
figsize = (8, 4)


def plot_commits(all_dates, ylim=[0, 200], figsize=(10, 5)):

    # --- Plotting ---
    fig, ax = plt.subplots(figsize=figsize)
    ax.bar(all_dates.index.to_pydatetime(), all_dates.values, color=None)
    ax.set_ylim(ylim)

    # Plot today
    ax.fill_between([docathon_start, docathon_end], *ax.get_ylim(),
                    alpha=.1, color='r')
    yticks = np.arange(0, ylim[1] + 1, 15).astype(int)
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticks, fontsize=18)
    ax.grid("off")
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_major_formatter(mpd.DateFormatter('%b\n%d'))

    # Y-axis formatting
    ax.set_ylabel("# commits")
    yticks = ax.get_yticks()
    for l in yticks:
        ax.axhline(l, linewidth=0.75, zorder=-10, color="0.5")
    ax.set_yticks(yticks)
    ax.set_ylim(ylim)

    plt.tight_layout()
    plt.autoscale(tight=True)
    return fig, ax

commits = pd.read_csv('.project_totals.csv')
commits = commits.set_index('date')
commits.index = pd.to_datetime(commits.index, utc=True)\
    .tz_convert('US/Pacific')
commits = commits.query('date > @plot_start')
all_commits = commits.groupby(level='date').sum()['doc']
fig, ax = plot_commits(all_commits, figsize=figsize)
ax.set_title('Docathon activity')
ax.set_ylabel('Number of doc commits')

# Save the figure
filename = os.path.join('..', '..', 'blog', 'content', 'images', "global_activity.png")
fig.savefig(filename, bbox_inches='tight')
print('Finished global activity!')
