import argparse
import numpy as np
import pandas as pd
from watchtower.handlers_ import UserDatabase


def parse_name(name):
    if not isinstance(name, str):
        return None
    else:
        name = name.split('/')[-1]
        return name

parser = argparse.ArgumentParser()
parser.add_argument("filename",
                    help=("CSV file containing the user "
                          "registration information."))
parser.add_argument("--outdir", "-o", default="build")
args = parser.parse_args()

db = UserDatabase(auth='GITHUB_API')

users = pd.read_csv(args.filename)
names = [parse_name(name)
         for name in users['GitHub User Name'].values]
for name in names:
    if name is None:
        continue
    db.update_user(name)
db = UserDatabase(auth='GITHUB_API')

before = '2017-03-10'
after = '2017-02-01'
before, after = (pd.to_datetime(ii) for ii in [before, after])
exceptions = []
activity = []
for user in db.users:
    try:
        user_db = db.load_user(user)
        messages, dates = zip(*[(jj['message'], idate)
                              for idate, ii in user_db.PushEvent.iterrows()
                              for jj in ii['payload']['commits']])
        dates = np.array(dates)
        messages = np.array(messages)
        mask = (dates > after) * (dates < before)
        messages = messages[mask]
        n_doc = 0
        for message in messages:
            search_queries = ['DOC', 'docs', 'docstring',
                              'documentation', 'docathon']
            for query in search_queries:
                if message.find(query) != -1:
                    n_doc += 1
                    break
        activity.append((user, len(messages), n_doc))
    except Exception as e:
        exceptions.append(e)
        activity.append((user, np.nan, np.nan))
        continue
activity = pd.DataFrame(activity, columns=['user', 'all', 'doc'])
activity['perc'] = activity['doc'] / activity['all']
activity = activity.sort_values('perc', ascending=False)
activity = activity.set_index('user')
activity.to_csv('.user_totals.csv')
