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
docathon_start = '2017-03-06'
docathon_end = '2017-03-10'
figsize = (8, 4)


def plot_commits(all_dates, ylim=[0, 20], figsize=(10, 5)):

    # --- Plotting ---
    fig, ax = plt.subplots(figsize=figsize)
    for label in all_dates.columns:
        ax.bar(all_dates.index.to_pydatetime(), all_dates[label].values,
               label=label)
    ax.set_ylim(ylim)

    # Plot today
    ax.fill_between([docathon_start, docathon_end], *ax.get_ylim(),
                    alpha=.1, color='k')
    yticks = np.arange(0, ylim[1] + 1, 4).astype(int)
    ax.set_yticks(yticks)
    ax.set_yticklabels(yticks)
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

    ax.legend(loc=1)
    ax.set_title(project, fontweight="bold", fontsize=22)
    plt.tight_layout()
    plt.autoscale(tight=True)
    return fig, ax

commits = pd.read_csv('.project_totals.csv')
commits['date'] = pd.to_datetime(commits['date'])
grp_projects = commits.groupby('project')
exceptions = []
for project, values in tqdm(grp_projects):
    try:
        values = values.set_index('date').drop('project', axis=1)
        fig, ax = plot_commits(values)
        if fig is None:
            exceptions.append(project)
            continue
        plt.close(fig)
    except Exception as e:
        fig, ax = plot_commits(values, figsize=figsize)
        ax.set_title(project, fontweight="bold", fontsize=22)
        ax.text(.5, .5, 'No info for project\n{}'.format(project),
                horizontalalignment='center', fontsize=16)
        exceptions.append(project)
        traceback.print_exception(None, e, e.__traceback__)
    # Save the figure
    if not os.path.exists("build/images"):
        os.makedirs("build/images")
    filename = os.path.join("build/images", project.lower() + ".png")
    fig.savefig(filename, bbox_inches='tight')

print('Finished building images.\nExceptions: {}'.format(exceptions))
