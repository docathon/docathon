import pandas as pd
import numpy as np
import requests
from watchtower import GithubDatabase
from watchtower._config import get_API_token
from watchtower._github_api import colon_seperated_pair


DOC_SEARCH_WORDS = ['readme', 'doc/', 'docs/', 'blog/', 'example/',
                    'examples/', '.md', '.rst', '.txt']
DOC_CHEATING_WORDS = ['build/', 'static/']


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

    # Iterate through days, find latest commit for each day
    days = [1, 2, 3, 4, 5, 6, 7, 8, 9, 10]
    days = [pd.to_datetime('2017-03-{:02}'.format(ii)).date() for ii in days]
    commits = {}
    for ii in days:
        mask = proj.commits.index.date == ii
        this_commits = proj.commits[mask]
        if len(this_commits) == 0:
            commits[ii] = {'sha1': None, 'sha2': None}
        else:
            # Find the last / first commits for the day
            sha2 = this_commits.loc[this_commits.index.max()]['sha']
            sha_min = this_commits.loc[this_commits.index.min()]['sha']

            # Now find the commit just before the 1st commit for this day
            ix = np.argwhere(proj.commits['sha'] == sha_min)
            sha1 = proj.commits['sha'].values[ix - 1].squeeze()
            commits[ii] = {'sha1': sha1, 'sha2': sha2}
    commits = pd.DataFrame(commits).T.astype(str).replace({'None': None})
    commits.index = pd.to_datetime(commits.index)

    # Iterate through start / stop SHAs and return the diff statistics
    diffs = []
    for date, (sha1, sha2) in commits.iterrows():
        if sha1 is None:
            continue
        stats = summarize_changes(user, project, sha1, sha2)
        stats['date'] = date
        if len(stats) > 0:
            diffs.append(stats)

    if len(diffs) > 0:
        diffs = pd.concat(diffs).set_index('date')
        diffs.index = pd.to_datetime(diffs.index)
        diffs['net'] = diffs['additions'] - diffs['deletions']
    return diffs


def summarize_changes(user, project, sha1, sha2, search_words=None):
    """Grab the change summary between two hashes.

    Stats show changes *from* sha1 *to* sha2

    Parameters
    ----------
    sha1 : string
        The hash for the first commit.
    sha2 : string
        The hash for the second commit
    user : string
        The user for this repository
    project : string
        The project name on github
    search_words : list | None
        A list of words to search for in the diff files.


    Returns
    -------
    changes : DataFrame
        A summary of changes for these hashes
    """
    if not all(isinstance(ii, str) for ii in [user, project, sha1, sha2]):
        raise ValueError('All inputs must be strings')
    if search_words is None:
        search_words = DOC_SEARCH_WORDS
    search_words = [search_words] if isinstance(search_words, str) else search_words

    resp = get_diff(user, project, sha1, sha2).json()

    changes = []
    for ifile in resp['files']:
        found = 0
        for word in search_words:
            ifilename = ifile['filename'].lower()
            if word in ifilename and not any(bword in ifilename for bword in DOC_CHEATING_WORDS):
                found += 1
        found = found > 0
        changes.append({'filename': ifile['filename'],
                        'changes': ifile['changes'],
                        'additions': ifile['additions'],
                        'deletions': ifile['deletions'],
                        'found': found})
    return pd.DataFrame(changes)

db = GithubDatabase()
meta = pd.read_csv('.project_info.csv')

all_diffs = []
for proj in db.projects:
    print(proj)
    user, project = proj.split('/')
    this_meta = meta.query('github_org == "{}/{}"'.format(user, project))
    branch = this_meta['branch'].values[0]
    branch = None if isinstance(branch, float) else branch
    diffs = find_commit_diffs(user, project, branch=branch)
    if diffs is None or len(diffs) == 0:
        continue
    diffs['project'] = project
    diffs['user'] = user
    all_diffs.append(diffs)

# Collect
all_diffs = pd.concat(all_diffs)
stats = all_diffs.reset_index().groupby(['date', 'project', 'user', 'found']).sum()
stats.to_csv('.diff_stats')
print('Finished calculating diff stats')
