import pandas as pd
import numpy as np
import datetime
from watchtower.handlers_ import GithubDatabase
from watchtower.commits_ import find_word_in_string

db = GithubDatabase(auth='GITHUB_API')
users = [ii for ii in db.users if len(ii) > 0]
# Times for inclusion
# end = pd.datetime.now()
# include_last_n_days = 4
# delta = datetime.timedelta(days=include_last_n_days + 1)
start = '2017-03-01'
end = '2017-03-11'
print('Calculating user activity from {} to {}'.format(start, end))

start, end = (pd.to_datetime(ii) for ii in [start, end])
exceptions = []
activity = []
for user in users:
    try:
        user_db = db.load(user)
        if len(user_db.PushEvent) == 0:
            activity.append((user, np.nan, np.nan))
            print('No commits for user: {}'.format(user))
            continue
        messages, dates = zip(*[(jj['message'], idate)
                              for idate, ii in user_db.PushEvent.iterrows()
                              for jj in ii['payload']['commits']])
        dates = np.array(dates)
        messages = np.array(messages)
        mask = (dates > start) * (dates <= end)
        messages = messages[mask]
        dates = dates[mask]
        for message, date in zip(messages, dates):
            search_queries = ['DOC', 'docs', 'docstring',
                              'documentation', 'docathon']
            is_doc = find_word_in_string(message, search_queries)
            activity.append((user, date, is_doc))

    except Exception as e:
        exceptions.append((user, e))
        activity.append((user, np.nan, np.nan))
        continue
print('Exceptions: ', '\n'.join([str(ii) for ii in exceptions]))
activity = pd.DataFrame(activity, columns=['user', 'date', 'is_doc'])
activity = activity.set_index('date')
activity.to_csv('.user_totals.csv')
