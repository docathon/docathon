import numpy as np
import os
import matplotlib
matplotlib.use('agg')
from watchtower import commits_
import matplotlib.pyplot as plt
from tqdm import tqdm
import calendar
import pandas as pd
import traceback



def plot_commits(user, project, search_queries=None,
                 groupby='month', since='2017-01-01'):
    """
    Parameters
    ----------
    user : string
        github username
    project : string
        project name
    search_queries : list of strings
        Strings to search within commits
    groupby : ['month', 'weekday']
        unit of time to group commits.
    since : time string
        Only use commits after this time
    """ 
    # Load commit data and return the date of each commit
    if search_queries is None:
        search_queries = ['DOC', 'docs', 'docstring']
    since = pd.to_datetime(since)
    commits = commits_.load_commits(user, project)
    if commits is None or not len(commits):
        raise ValueError(
            'No commits: load_commits returned None, '
            'or None like : %r' % commits)
    dates = pd.to_datetime([ii['author']['date']
                           for ii in commits['commit']])
    # Remove commits from the past we don't want
    mask_since = dates > since
    commits = commits[mask_since]
    dates = dates[mask_since]

    n_commits = []
    doc_commits = []

    iter_dates = range(1, 13) if groupby == 'month' else range(7)
    for ii_time in iter_dates:
        if commits is None:
            doc_commits.append(0)
            n_commits.append(0)
            continue
        # Count commits for this unit of time
        mask = getattr(dates, groupby) == ii_time
        n_commits.append(mask.sum())

        # Now count how many commits match the query
        doc_commits.append(sum(any(qu in c['message']
                                   for qu in search_queries)
                               for c in commits[mask]['commit']))
    # Generate barplots
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.bar(np.arange(len(n_commits)), n_commits, label="all")
    ax.bar(np.arange(len(n_commits)), doc_commits, label="doc")
    ax.grid("off")
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')

    # Create xaxis labels
    label_names = calendar.month_name if groupby == 'month' else calendar.day_name
    label_names = [label_names[ii][:3] for ii in iter_dates]
    ax.set_xticks(np.arange(len(iter_dates)))
    ax.set_xticklabels(label_names, rotation=90, fontsize="x-small")
    ax.set_ylabel("# commits")

    # Y-axis formatting
    yticks = ax.get_yticks()
    for l in yticks:
        ax.axhline(l, linewidth=0.75, zorder=-10, color="0.5")
    ax.set_yticks(yticks)

    ax.legend(loc=1)
    ax.set_title(project, fontweight="bold")
    return fig, ax


# --- Run the script ---
informations = pd.read_csv(".downloaded_projects").values
try:
    os.makedirs("build/images")
except OSError:
    pass

groupby = 'weekday'
since = '2017-02-02'

exceptions = []
for user, project in tqdm(informations):
    try:
        fig, ax = plot_commits(user, project,
                               groupby=groupby, since=since)
        filename = os.path.join("build/images", project + ".png")
        fig.savefig(filename, bbox_inches='tight')
    except Exception as e:
        exceptions.append(project)
        traceback.print_exception(None, e, e.__traceback__)
print('Finished building images.\nExceptions: {}'.format(exceptions))
