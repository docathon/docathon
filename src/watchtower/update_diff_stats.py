import pandas as pd
import numpy as np
import os
import requests
from watchtower import GithubDatabase
from watchtower._config import get_API_token, DATETIME_FORMAT
from watchtower._github_api import colon_seperated_pair


def get_diff(user, proj, sha1, sha2, auth=None):
    """Get the diff between two hashes for a project."""
    auth = get_API_token(auth)
    auth = colon_seperated_pair(auth)
    url = 'http://api.github.com/repos/{user}/{proj}/compare/{sha1}...{sha2}'
    url = url.format(user=user, proj=proj, sha1=sha1, sha2=sha2)
    resp = requests.get(url, auth=auth)
    return resp


def find_commit_diffs(user, project, branch=None):
    """Find commit diffs for a user/project."""
    proj = db.load(user, project, branch=branch)
    if proj.commits is None:
        print('No commits for {}/{}'.format(user, project))
        return None
    proj.commits = proj.commits.sort_index()

    # Iterate through days, find latest commit for each day
    days = pd.date_range(day_start, day_stop, freq='D')\
        .tz_localize('US/Pacific')
    commits = {}
    for ii in days:
        mask = proj.commits.index.date == ii.date()
        this_commits = proj.commits[mask]
        if len(this_commits) == 0:
            commits[ii] = {'date_start': None, 'sha1': None, 'sha2': None}
        else:
            # Find the last / first commits for the day
            commit_max = this_commits.loc[this_commits.index.max()]
            sha2 = commit_max['sha']
            date_max = commit_max.name
            sha_min = this_commits.loc[this_commits.index.min()]['sha']
            if isinstance(sha_min, pd.Series):
                sha_min = sha_min.values[0]
            if isinstance(sha2, pd.Series):
                sha2 = sha2.values[0]

            # Now find the commit just before the 1st commit for this day
            ix = np.argwhere(proj.commits['sha'] == sha_min).squeeze()
            commit_min = proj.commits.iloc[ix - 1]
            sha1 = commit_min['sha']
            date_start = commit_min.name
            commits[date_max] = {'sha1': sha1, 'sha2': sha2,
                                 'date_start': date_start}
    commits = pd.DataFrame(commits).T.astype(str).replace({'None': None})
    commits = commits[['date_start', 'sha1', 'sha2']]
    commits.index = pd.to_datetime(commits.index)

    # Iterate through start / stop SHAs and return the diffs
    files = []
    for date, (date_start, sha1, sha2) in commits.iterrows():
        if sha1 is None:
            continue
        resp = get_diff(user, project, sha1, sha2).json()
        resp = pd.Series(resp)
        if len(resp) > 0:
            for ifile in resp['files']:
                ifile['date'] = date
                ifile['sha_start'] = sha1
                ifile['sha_stop'] = sha2
                ifile['date_start'] = date_start
                files.append(ifile)

    if len(files) > 0:
        files = pd.DataFrame(files).set_index('date')
    return files


# --- Initialize ---

db = GithubDatabase()
meta = pd.read_csv('.project_info.csv')

# Check if we have pre-existing diffs so we only update the latest
day_stop = pd.datetime.today().date()
path_save = '../data/docathon_diffs.csv'
if os.path.exists(path_save):
    old_files = pd.read_csv(path_save).set_index('date')
    old_files.index = pd.to_datetime(old_files.index, utc=True)\
        .tz_convert('US/Pacific')
    day_start = old_files.index.max().date()
else:
    old_files = None
    day_start = pd.to_datetime('2017-02-24')
print('\n\nDownloading diffs from {:%x} to {:%x}'.format(day_start, day_stop))
print('---\n\n')

all_files = []
for proj in db.projects:
    user, project = proj.split('/')
    print('{}/{}'.format(user, project))
    this_meta = meta.query('github_org == "{}/{}"'.format(user, project))
    branch = this_meta['branch'].values[0]
    branch = None if isinstance(branch, float) else branch
    files = find_commit_diffs(user, project, branch=branch)
    if files is None or len(files) == 0:
        continue
    files['project'] = project
    files['user'] = user
    all_files.append(files)

# Collect
all_files = pd.concat(all_files)
if old_files is not None:
    all_files = pd.concat([old_files, all_files]).drop_duplicates(subset=['sha'])
all_files.to_csv('../data/docathon_diffs.csv', date_format=DATETIME_FORMAT)
print('Finished calculating diff stats')
