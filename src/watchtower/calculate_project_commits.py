import numpy as np
import os
from watchtower import GithubDatabase
from watchtower.commits_ import find_word_in_string
from tqdm import tqdm
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

    commits = db.load(user, project).commits
    if commits is None:
        return None, None
    if commits is None or not len(commits):
        raise ValueError(
            'No commits: load_commits returned None, '
            'or None like : %r' % commits)

    # Define full date range
    all_dates = pd.date_range(start, stop, freq='D')
    all_dates = pd.DataFrame(np.zeros(all_dates.shape[0], dtype=int),
                             index=all_dates)

    # Remove commits from the past we don't want
    commits = commits.query('date > @start and date < @stop')
    if len(commits) == 0:
        # In case no commits for this project
        all_dates = all_dates.drop(0, axis=1).astype(int)
        all_dates['all'] = 0
        all_dates['doc'] = 0
        return all_dates

    commits.loc[:, 'is_doc'] = commits['message'].apply(
        find_word_in_string, args=(search_queries,))

    # Tally the total number vs. doc-related commits
    commits_doc = commits['is_doc'].resample('D').sum()
    commits_all = commits['is_doc'].resample('D').count()

    for date, val in commits_all.items():
        all_dates.loc[date, 'all'] = val
    for date, val in commits_doc.items():
        all_dates.loc[date, 'doc'] = val

    # Clean up
    all_dates = all_dates.drop(0, axis=1)
    all_dates = all_dates.replace(np.nan, 0)
    all_dates = all_dates.astype(int)
    return all_dates


# --- Run the script ---
try:
    os.makedirs("build/images")
except OSError:
    pass

db = GithubDatabase()
projects = [ii.split('/')[-2:] for ii in db.projects]
groupby = 'weekday'
start = '2017-03-01'
stop = '2017-03-11'
exceptions = []
all_dates = []
for user, project in tqdm(projects):
    try:
        this_all_dates = count_doc_commits(
            user, project, groupby=groupby, start=start, stop=stop)

        # Collect data so we can save it
        this_all_dates['project'] = project
        all_dates.append(this_all_dates)
    except Exception as e:
        exceptions.append((user, project))
        traceback.print_exception(None, e, e.__traceback__)

print('Exceptions: {}'.format(exceptions))
all_dates = pd.concat(all_dates, axis=0)
all_dates.index.name = 'date'
all_dates.to_csv('.project_totals.csv')
