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


def count_doc_commits(user, project, search_queries=None,
                      groupby='month', start='2017-01-01', stop=None):
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
        search_queries = ['DOC', 'docs', 'docstring', 'documentation', 'docathon']

    start = pd.to_datetime(start)
    if stop is None:
        stop = pd.datetime.today()
    else:
        stop = pd.to_datetime(stop)

    if project == 'IPython':
        import IPython; IPython.embed()
    commits = commits_.load_commits(user, project)
    if commits is None:
        return None, None
    commits['message'] = [commit['message'] for commit in commits['commit']]
    if commits is None or not len(commits):
        raise ValueError(
            'No commits: load_commits returned None, '
            'or None like : %r' % commits)
    dates = pd.to_datetime([ii['author']['date']
                           for ii in commits['commit']])
    commits.index = dates

    # Define full date range
    all_dates = pd.date_range(start, stop, freq='D')
    all_dates = pd.DataFrame(np.zeros(all_dates.shape[0], dtype=int),
                             index=all_dates)

    # Remove commits from the past we don't want
    mask_since = (dates > start) * (dates < stop)
    commits = commits[mask_since]

    # Find commits that match our queries
    mask_doc = np.zeros(commits.shape[0])
    for query in search_queries:
        # This is a really hacky way to do this but python keeps giving me errors
        for ix, message in enumerate(commits['message'].values):
            if message.find(query) != -1:
                mask_doc[ix] += 1
    mask_doc = np.array(mask_doc) > 0
    commits['is_doc'] = mask_doc

    # Tally the total number vs. doc-related commits
    commits_doc = commits['is_doc'].resample('D').sum()
    commits_all = commits['is_doc'].resample('D').count()

    for date, val in commits_all.items():
        all_dates.loc[date, 'All'] = val
    for date, val in commits_doc.items():
        all_dates.loc[date, 'Doc'] = val

    # Clean up
    all_dates = all_dates.drop(0, axis=1)
    all_dates = all_dates.replace(np.nan, 0)
    all_dates = all_dates.astype(int)
    return all_dates


def plot_commits(all_dates):

    # --- Plotting ---
    fig, ax = plt.subplots(figsize=(8, 4))
    for label in all_dates.columns:
        ax.bar(all_dates.index.to_pydatetime(), all_dates[label].values,
               label=label)
    # Plot today
    today = pd.datetime.today()
    ax.axvline(today, ls='--', alpha=.5, lw=2, color='k')
    ax.grid("off")
    ax.spines['right'].set_color('none')
    ax.spines['left'].set_color('none')
    ax.spines['top'].set_color('none')
    ax.xaxis.set_ticks_position('bottom')
    ax.yaxis.set_ticks_position('left')
    ax.xaxis.set_major_formatter(mpd.DateFormatter('%b\n%d'))

    # Y-axis formatting
    ax.set_ylabel("# commits")
    ax.set_ylim([0, np.max([5, int(ax.get_ylim()[-1])])])
    yticks = ax.get_yticks()
    for l in yticks:
        ax.axhline(l, linewidth=0.75, zorder=-10, color="0.5")
    ax.set_yticks(yticks)

    ax.legend(loc=1)
    ax.set_title(project, fontweight="bold", fontsize=22)
    plt.tight_layout()
    plt.autoscale(tight=True)
    return fig, ax


# --- Run the script ---
informations = pd.read_csv(".downloaded_projects").values
try:
    os.makedirs("build/images")
except OSError:
    pass

groupby = 'weekday'
start = '2017-02-02'
stop = '2017-03-10'
exceptions = []
all_dates = []
for user, project in tqdm(informations):
    try:
        this_all_dates = count_doc_commits(user, project,
                                      groupby=groupby, start=start, stop=stop)
        fig, ax = plot_commits(this_all_dates)
        if fig is None:
            exceptions.append(project)
            continue
        filename = os.path.join("build/images", project.lower() + ".png")
        fig.savefig(filename, bbox_inches='tight')

        # Collect data so we can save it
        this_all_dates['project'] = project
        all_dates.append(this_all_dates)
    except Exception as e:
        exceptions.append(project)
        traceback.print_exception(None, e, e.__traceback__)
all_dates = pd.concat(all_dates, axis=0)
all_dates.to_csv('.totals.csv')
print('Finished building images.\nExceptions: {}'.format(exceptions))
